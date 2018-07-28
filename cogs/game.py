"""Implements a miniRPG game using bot commands"""
import pickle
from datetime import datetime

import discord
from discord.ext import commands
from lib import entity, room, customconverter as cconv # , item

PLAYERDATA = "important/rpg/playerdata.pickle"
ROOMDATA = "important/rpg/roomdata.pickle"
DEFAULTROOM = room.Room({"desc": "The entrance to the dungeon. Enter if you dare.", "type": 0})

class UnknownPlayerException(Exception):
    "Raised when looking for a player but it wasn't found"
    pass

async def get_all_players(ctx=None) -> dict:
    """Get all players participating in the game currently

    Args:
        ctx (discord.Context, optional): Context parameter. Defaults to None. If given, sends error
            messages directly to the place whence the command was requested.

    Returns:
        dict {entity.Entity.id (int): entity.Entity}

    Raises:
        pickle.UnpicklingError: If unpickling fails

    """
    try:
        with open(PLAYERDATA, "rb") as opened_file:
            players = pickle.load(opened_file)
    except FileNotFoundError:
        # Default to an empty dictionary and create the file for next time.
        players = {}
        with open(PLAYERDATA, "wb") as opened_file:
            pickle.dump(players, opened_file, protocol=pickle.HIGHEST_PROTOCOL)
        # If possible, inform the player.
        if ctx is not None:
            await ctx.send(f"*~~NOTE: created new datafile {PLAYERDATA}~~*")
    # If pickle throws an error, try to report it the the user and then raise it again.
    except pickle.UnpicklingError:
        if ctx is not None:
            await ctx.send(f"ERROR: file {PLAYERDATA} is corrupt, cannot fetch data.")
        raise
    return players

async def get_all_rooms(ctx=None) -> list:
    """Get all rooms the players have explored so far

    Args:
        ctx (discord.Context, optional): Context parameter. Defaults to None. If given, sends error
            messages directly to the place whence the command was requested.

    Returns:
        list of room.Room

    Raises:
        pickle.UnpicklingError: If unpickling fails

    """
    try:
        with open(ROOMDATA, "rb") as opened_file:
            rooms = pickle.load(opened_file)
    except FileNotFoundError:
        # Default to an generating room 0 and then create the file for next time.
        rooms = [DEFAULTROOM]
        if ctx is not None:
            with open(ROOMDATA, "wb") as opened_file:
                pickle.dump(rooms, opened_file, protocol=pickle.HIGHEST_PROTOCOL)
        # If possible, inform the player.
        await ctx.send(f"*~~NOTE: created new datafile {ROOMDATA}~~*")
    # If pickle throws an error, try to report it the the user and then raise it again.
    except pickle.UnpicklingError:
        if ctx is not None:
            await ctx.send(f"ERROR: file {ROOMDATA} is corrupt, cannot fetch data.")
        raise
    return rooms

async def get_player(idnum, ctx=None, return_all=False) -> entity.Entity:
    """Get all rooms the players have explored so far

    Args:
        idnum (int): The ID of the player to get.
        ctx (discord.Context, optional): Context parameter. Defaults to None. If given, sends error
            messages directly to the place whence the command was requested.
        return_all (bool, optional): Whether to return all other players too. Defaults to False.

    Returns:
        entity.Entity (target player),
        (dict {entity.Entity.id (int): entity.Entity}) (all other players)

    Raises:
        UnknownPlayerException: If that player doesn't exist

    """
    players = await get_all_players(ctx)
    target = players.get(idnum)
    # If that player wasn't found
    if target is None:
        # Report back to the player, if possible, and then raise UnknownPlayerException
        if ctx is not None:
            if ctx.author.id == idnum:
                await ctx.send(f"ERROR: {ctx.author.name}, you haven't joined the game yet")
            else:
                await ctx.send(f"ERROR: {ctx.author.name}, target player hasn't joined the game")
        raise UnknownPlayerException(idnum)
    if return_all:
        return target, players
    return target

async def get_players_in_room(players, room_num, player) -> str:
    """Return a message about the amount of players in target room.

    Args:
        players (dict {entity.Entity.id (int): entity.Entity}): All the players to check through
        room_num (int): The index of the room to get info about
        player (entity.Entity, optional): The player to exclude. Defaults to None.

    Returns:
        str

    """
    other_players = 0
    for i in players.values():
        if i.stats["loc"]["room"] == room_num:
            if player is None:
                other_players += 1
            elif i.idnum != player.idnum:
                other_players += 1
    return ("* You are the only player in this room" if other_players == 0 else
            "* There is 1 other player in this room" if other_players == 1 else
            f"* There are {other_players} other players in this room")

async def write_data(players):
    """Save all the data about the players

    Args:
        players (dict {entity.Entity.id (int): entity.Entity}): All the players to write to file

    """
    with open(PLAYERDATA, 'wb') as opened_file:
        pickle.dump(players, opened_file, protocol=pickle.HIGHEST_PROTOCOL)

async def write_rooms(rooms):
    """Save all the data about the rooms

    Args:
        rooms (list of room.Room): All the rooms to write to file

    """
    with open(ROOMDATA, 'wb') as opened_file:
        pickle.dump(rooms, opened_file, protocol=pickle.HIGHEST_PROTOCOL)

async def error_handler(err, ctx):
    """Informs the user about a game error.

    Args:
        err (entity.EntityError): the exception to analyze.
        ctx (discord.Context): the context object to get the target channel from.

    Raises:
        SyntaxError: if the error handler fails to handle an error

    """
    try:
        await ctx.send(
            f"ERROR {err.args[0]}, {ctx.author.name}: {err.emsg[err.args[0]].format(*err.args[1])}")
    except LookupError:
        await ctx.send(f"Error while handling error {repr(err)}")

class GameCog():
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "RPG"

    @commands.command(name='join', aliases=['enter', 'play'],
                      help="Join the RPG!",
                      brief="Creates a player for you so you could participate in the RPG")
    async def join(self, ctx):
        players = await get_all_players(ctx)
        if players.get(ctx.author.id, False):
            await ctx.send(f"ERROR: {ctx.author.name}, you have already joined!")
            return
        author_data = {
            "name": ctx.author.name,
            "id": ctx.author.id,
            "invsize": 10,
        }
        new_player = entity.Entity(author_data)
        players[ctx.author.id] = new_player
        await write_data(players)
        embed = discord.Embed(
            title="**Welcome to the game!** <:xithioxrpg:352254056842002433>",
            colour=0x417505,
            description=(f"What next? Read everything below here, "
                         f"and then start your adventure with {ctx.prefix}explore"),
            timestamp=datetime.utcnow(),
            )

        embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url,
            )
        embed.set_footer(
            text="Good luck!",
            icon_url="https://cdn.discordapp.com/emojis/367392970409771008.png?v=1",
            )

        embed.add_field(
            name="Currently, your attributes are weak",
            value="I advise you upgrade them right away",
            )
        embed.add_field(
            name="How to upgrade",
            value=(f"use {ctx.prefix}upgrade <attrib> <amount>. "
                   f"You have been given 10 points for that.")
            )
        embed.add_field(
            name="List of attributes",
            value=("```\nVIT - Vitality\nSTR - Strength\n"
                   "DEX - Dexterity\nDEF - Defense\nLCK - Luck```"),
            inline=True
            )
        embed.add_field(
            name="Effects of these attributes",
            value=("```\nHigher maximum health\nStronger attacks\nHigher chance to dodge\n"
                   "Less health lost\nBetter chances to crit```"),
            inline=True
            )

        await ctx.author.send(embed=embed)
        if ctx.message.guild is not None:
            await ctx.send(f"Welcome to the game, {ctx.author.name}!")

    @commands.command(name='stats', aliases=[],
                      help="Get your RPG stats.")
    async def stats(self, ctx, *, target_player=None):
        if target_player is None:
            target_player = ctx.author
        else:
            try:
                target_player = await cconv.HybridConverter().convert(ctx, target_player)
            except commands.BadArgument:
                await ctx.send(f"ERROR: {ctx.author.name}, an user with that name wasn't found.")

        player = await get_player(target_player.id, ctx)

        stats = player.stats
        attrib = stats["attrib"]
        eqpinv = player.eqp.inv

        ratio = stats['hp'] / stats['maxhp']
        display_points = int(ratio*100//2.5)
        full_points = display_points // 4
        leftover = display_points % 4
        block_characters = ["", "\u2591", "\u2592", "\u2593", "\u2588"]
        healthbar = block_characters[4] * full_points + block_characters[leftover]
        healthbar += (10 - len(healthbar)) * "\u2500"
        if ratio > 0.5:
            color = (int(255 * (1 - ratio)) * 2, 255, 40)
        else:
            color = (255, int(255 * ratio * 2), 40)
        embed = discord.Embed(
            title=f"`HP: {stats['hp']}/{stats['maxhp']}`",
            colour=discord.Colour.from_rgb(*color),
            description=f"[ {healthbar} ]",
            timestamp=datetime.utcnow()
            )
        embed.set_footer(
            text=f"ID: {target_player.id}"
            )
        embed.set_author(
            name=target_player.name,
            icon_url=target_player.avatar_url
            )

        # TODO: Equipment bonuses
        embed.add_field(
            name="Attributes",
            value=(f"```py\n"
                   f"STR {attrib['str']:02d} + 00\n"
                   f"DEF {attrib['def']:02d} + 00\n"
                   f"VIT {attrib['vit']:02d} + 00\n"
                   f"DEX {attrib['dex']:02d} + 00\n"
                   f"LCK {attrib['lck']:02d} + 00\n"
                   f"\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n"
                   f"CP: {stats['points']}```"),
            inline=True
            )
        embed.add_field(
            name="Equipment",
            value=(f"<:sword:472189428362772501> `{eqpinv['weapon']}`\n"
                   f"<:chestplate:472189428098531358> `{eqpinv['torso']}`\n"
                   f"<:leggings:472189428597784579> `{eqpinv['legs']}`\n"
                   f"<:ring1:472189428610105344> `{eqpinv['ring1']}`\n"
                   f"<:ring2:472189428375486469> `{eqpinv['ring2']}`"),
            inline=True
            )
        embed.add_field(
            name=f"{target_player.name} is in room {stats['loc']['room']}",
            value=f"The furthest {target_player.name} has been is room {stats['loc']['max']}",
            inline=True
            )

        await ctx.send(embed=embed)

    @commands.command(name='upgrade', aliases=[],
                      help="Upgrade one of your stats.")
    async def upgrade(self, ctx, attrib, amount: int = 1):
        aliases = {"atk": "str", "attack": "str", "strength": "str", "str": "str",
                   "defense": "def", "defence": "def", "def": "def",
                   "vitality": "vit", "health": "vit", "constitution": "vit",
                   "vit": "vit", "hp": "vit", "con": "vit", "dexterity": "dex",
                   "speed": "dex", "spd": "dex", "dex": "dex", "agility": "dex",
                   "luck": "lck", "lck": "lck", "luk": "lck", "chance": "lck", "fortune": "lck",
                  }
        player, players = await get_player(ctx.author.id, ctx, True)
        attrib = aliases.get(attrib.lower())
        if attrib is None:
            await ctx.send(f"ERROR: {ctx.author.name}, that is not a valid attribute to upgrade.")
            return
        elif amount > player.stats["points"]:
            await ctx.send((f"ERROR: {ctx.author.name}, not enough points."
                            f"(you have {player.stats['points']})"))
            return
        elif player.stats["attrib"][attrib] + amount > 99:
            await ctx.send(f"ERROR: {ctx.author.name}, max attribute amount is 99.")
            return
        elif amount < 0:
            if player.stats["loc"]["max"] == 0:
                if player.stats["attrib"][attrib] + amount < 1:
                    await ctx.send(f"ERROR: {ctx.author.name}, min attribute amount is 01.")
                    return
            else:
                await ctx.send(f"ERROR: {ctx.author.name}, cannot downgrade after starting.")
                return
        elif amount < 1:
            await ctx.send(f"ERROR: {ctx.author.name}, must spend at least one point.")
            return
        player.stats["attrib"][attrib] += amount
        player.stats["points"] -= amount
        new_amount = player.stats["attrib"][attrib]
        new_points = player.stats["points"]
        await write_data(players)

        amount_upgraded = f"{amount} points" if amount != 1 else "1 point"
        remaining = ("and there is 1 point remaining" if new_points == 1 else
                     f"and there are {new_points} points remaining" if new_points != 0 else
                     "and there are no points remaining")
        upgrade = "upgraded" if amount > 0 else "downgraded"
        amount = abs(amount)
        await ctx.send((f"{ctx.author.name}, {upgrade} {attrib.upper()} by {amount_upgraded} "
                        f"({attrib.upper()} is now {new_amount}, {remaining})"))

    @commands.command(name='explore', aliases=[],
                      help="Move to your next unexplored room")
    async def explore(self, ctx):
        player, players = await get_player(ctx.author.id, ctx, True)
        rooms = await get_all_rooms(ctx)
        loc = player.stats["loc"]
        if loc["room"] != loc["max"]:
            await ctx.send((f"ERROR: {ctx.author.name}, must move to your last known room before "
                            f"exploring further (room {loc['max']})"))
            return
        start_room = player.stats["loc"]["room"]
        end_room = start_room + 1
        player.stats["loc"]["max"] += 1
        player.stats["loc"]["room"] = player.stats["loc"]["max"]
        await write_data(players)
        players_message = await get_players_in_room(players, end_room, player)
        is_new = "* Someone has already been here before"
        try:
            target_room = rooms[end_room]
        except IndexError:
            is_new = "* You are the first person to enter this room"
            target_room = room.Room({})
            rooms.append(target_room)
            await write_rooms(rooms)
        embed = discord.Embed(
            title=f"Moved from room {start_room} to room {end_room}",
            colour=0x7ed321,
            description=target_room.desc,
            timestamp=datetime.utcnow())
        embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Contents",
            value=f"```asciidoc\n{target_room.typedesc}\n{is_new}\n{players_message}```")

        await ctx.author.send(embed=embed)
        if ctx.message.guild is not None:
            await ctx.send(f"{ctx.author.name}, explored from room {start_room} to room {end_room}")

    @commands.command(name='look', aliases=[],
                      help="Look at the room you're currently in.")
    async def look(self, ctx):
        player, players = await get_player(ctx.author.id, ctx, True)
        rooms = await get_all_rooms(ctx)
        room_num = player.stats["loc"]["room"]
        room_obj = rooms[room_num]
        players_message = await get_players_in_room(players, room_num, player)
        embed = discord.Embed(
            title=f"You are in room {room_num}",
            colour=0x7ed321,
            description=room_obj.desc,
            timestamp=datetime.utcnow()
            )

        embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url
            )

        embed.add_field(
            name="Contents",
            value=f"```asciidoc\n{room_obj.typedesc}\n{players_message}```")

        await ctx.author.send(embed=embed)
        if ctx.message.guild is not None:
            await ctx.send(f"{ctx.author.name}, you are in room {room_num}")

    @commands.command(name='move', aliases=['go', 'goto'],
                      help="Move to an already explored room")
    async def move(self, ctx, target_room: int = 0):
        player, players = await get_player(ctx.author.id, ctx, True)
        rooms = await get_all_rooms(ctx)

        try:
            player.moveto(target_room)
        except entity.EntityError as error:
            await error_handler(error, ctx)
        except entity.ActionSuccesful as error:
            start_room, target_room, _ = error.args[1]

        room_obj = rooms[target_room]
        players_message = await get_players_in_room(players, target_room, player)
        await write_data(players)

        embed = discord.Embed(
            title=f"Moved from room {start_room} to room {target_room}",
            colour=0x7ed321,
            description=room_obj.desc,
            timestamp=datetime.utcnow())
        embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Contents",
            value=f"```asciidoc\n{room_obj.typedesc}\n{players_message}```")

        await ctx.author.send(embed=embed)
        if ctx.message.guild is not None:
            await ctx.send(f"{ctx.author.name}, moved from room {start_room} to room {target_room}")

    @commands.command(name='attack', aliases=['atk'],
                      help="Attack another player!")
    async def attack(self, ctx, target_player: cconv.HybridConverter):
        attacker, players = await get_player(ctx.author.id, ctx, True)
        defender = await get_player(target_player.id, ctx, False)


def setup(bot):
    bot.add_cog(GameCog(bot))
