import pickle
from datetime import datetime

import discord
from discord.ext import commands
from lib import entity, room # , item

PLAYERDATA = "important/rpg/playerdata.pickle"
ROOMDATA = "important/rpg/roomdata.pickle"
DEFAULTROOM = room.Room({"desc": "The entrance to the dungeon. Enter if you dare.", "type": 0})

class UnknownPlayerException(Exception):
    pass

async def get_all_players(ctx=None):
    try:
        with open(PLAYERDATA, "rb") as opened_file:
            players = pickle.load(opened_file)
    except FileNotFoundError:
        players = {}
        if ctx is not None:
            await ctx.send(f"*~~NOTE: created new datafile {PLAYERDATA}~~*")
            with open(PLAYERDATA, "wb") as opened_file:
                pickle.dump(players, opened_file, protocol=pickle.HIGHEST_PROTOCOL)
    except pickle.UnpicklingError:
        if ctx is not None:
            await ctx.send(f"ERROR: file {PLAYERDATA} is corrupt, cannot fetch data.")
        raise
    return players

async def get_all_rooms(ctx=None):
    try:
        with open(ROOMDATA, "rb") as opened_file:
            rooms = pickle.load(opened_file)
    except FileNotFoundError:
        rooms = [DEFAULTROOM]
        if ctx is not None:
            await ctx.send(f"*~~NOTE: created new datafile {ROOMDATA}~~*")
            with open(ROOMDATA, "wb") as opened_file:
                pickle.dump(rooms, opened_file, protocol=pickle.HIGHEST_PROTOCOL)
    except pickle.UnpicklingError:
        if ctx is not None:
            await ctx.send(f"ERROR: file {ROOMDATA} is corrupt, cannot fetch data.")
        raise
    return rooms

async def get_player(idnum, ctx=None, return_all=False):
    players = await get_all_players(ctx)
    target = players.get(idnum)
    if target is None:
        if ctx is not None:
            if ctx.author.id == idnum:
                await ctx.send(f"ERROR: {ctx.author.name}, you haven't joined the game yet")
            else:
                await ctx.send(f"ERROR: {ctx.author.name}, target player hasn't joined the game")
        raise UnknownPlayerException(idnum)
    if return_all:
        return target, players
    return target

async def write_data(players):
    with open(PLAYERDATA, 'wb') as opened_file:
        pickle.dump(players, opened_file, protocol=pickle.HIGHEST_PROTOCOL)

async def write_rooms(rooms):
    with open(ROOMDATA, 'wb') as opened_file:
        pickle.dump(rooms, opened_file, protocol=pickle.HIGHEST_PROTOCOL)

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
        await ctx.send(f"Welcome to the game, {ctx.author.name}!")

    @commands.command(name='stats', aliases=[],
                      help="Get your RPG stats.")
    async def stats(self, ctx):
        player = await get_player(ctx.author.id, ctx)

        stats = player.stats
        attrib = stats["attrib"]
        equipment = player.eqp
        eqpinv = equipment.inv

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
            text=f"ID: {ctx.author.id}"
            )
        embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url
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
            value=(f"<:sword:463364131836264469> `{eqpinv['weapon']}`\n"
                   f"<:chestplate:463366339025829901> `{eqpinv['torso']}`\n"
                   f"<:leggings:463367024844734465> `{eqpinv['legs']}`\n"
                   f"<:ring1:463377259445616651> `{eqpinv['ring1']}`\n"
                   f"<:ring2:463377935425077248> `{eqpinv['ring2']}`"),
            inline=True
            )
        embed.add_field(
            name=f"You are in room {stats['loc']['room']}",
            value=f"The furthest you've been is room {stats['loc']['max']}",
            inline=True
            )

        await ctx.send(embed=embed)

    @commands.command(name='upgrade', aliases=[],
                      help="Upgrade one of your stats.")
    async def upgrade(self, ctx, attrib, amount: int):
        aliases = {"atk": "str", "attack": "str", "strength": "str", "str": "str",
                   "defense": "def", "defence": "def", "def": "def",
                   "vitality": "vit", "health": "vit", "constitution": "vit",
                   "vit": "vit", "hp": "vit", "con": "vit",
                   "dexterity": "dex", "speed": "dex", "spd": "dex", "dex": "dex",
                   "luck": "lck", "lck": "lck", "luk": "lck", "chance": "lck",
                  }
        player, players = await get_player(ctx.author.id, ctx, True)
        attrib = aliases.get(attrib)
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

        amount_upgraded = f"{amount} points" if amount != 1 else "1 point"
        remaining = (f"points remaining is now {new_points}" if new_points != 0
                     else "no points remaining")
        upgrade = "upgraded" if amount > 0 else "downgraded"
        amount = abs(amount)
        await ctx.send((f"{ctx.author.name}, {upgrade} {attrib.upper()} by {amount_upgraded} "
                        f"({attrib.upper()} is now {new_amount}, {remaining})"))

        await write_data(players)

    @commands.command(name='explore', aliases=[],
                      help="Move to your next unexplored room")
    async def explore(self, ctx):
        player, players = await get_player(ctx.author.id, ctx, True)
        rooms = await get_all_rooms(ctx)
        loc = player.stats["loc"]
        if loc["room"] != loc["max"]:
            await ctx.send((f"ERROR: {ctx.author.name}, must move to your last known room before "
                            f"exploring further (room {loc['max']})"))
        start_room = player.stats["loc"]["room"]
        end_room = start_room + 1
        player.stats["loc"]["max"] += 1
        player.stats["loc"]["room"] = player.stats["loc"]["max"]
        try:
            target_room = rooms[end_room]
        except IndexError:
            target_room = room.Room({})
            rooms.append(target_room)
        await write_data(players)
        await write_rooms(rooms)
        embed = discord.Embed(
            title=f"Moved from room {start_room} to room {end_room}",
            colour=0x7ed321,
            description=target_room.desc,
            timestamp=datetime.utcnow()
            )

        embed.set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar_url
            )

        embed.add_field(
            name="Contents",
            value="```asciidoc\n= The room is empty (for now) =```")

        await ctx.author.send(embed=embed)
        await ctx.send(f"{ctx.author.name}, moved from room {start_room} to room {end_room}")

    @commands.command(name='look', aliases=[],
                      help="Look at the room you're currently in.")
    async def look(self, ctx):
        player, players = await get_player(ctx.author.id, ctx, True)
        rooms = await get_all_rooms(ctx)
        room_num = player.stats["loc"]["room"]
        room_obj = rooms[room_num]
        other_players = 0
        for i in players.values():
            if i.stats["loc"]["room"] == room_num:
                if i.idnum != player.idnum:
                    other_players += 1
        players_message = ("* You are the only player in this room" if other_players == 0 else
                           "* There is 1 other player in this room" if other_players == 1 else
                           f"* There are {other_players} other players in this room")
        room_contents = ["= This room contains everybody who haven't entered the dungeon yet =",
                         "= The room is empty = "]
        room_contents = room_contents[room_obj.type]
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
            value=f"```asciidoc\n{room_contents}\n{players_message}```")

        await ctx.author.send(embed=embed)
        await ctx.send(f"{ctx.author.name}, you are in room {room_num}")


def setup(bot):
    bot.add_cog(GameCog(bot))
