import pickle
from datetime import datetime

import discord
from discord.ext import commands
from lib import entity # , item

PLAYERDATA = "important/playerdata.pickle"

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
                pickle.dump({}, opened_file, protocol=pickle.HIGHEST_PROTOCOL)
    except pickle.UnpicklingError:
        if ctx is not None:
            await ctx.send(f"ERROR: file {PLAYERDATA} is corrupt, cannot fetch data.")
        raise
    return players

async def get_player(idnum, ctx=None):
    players = await get_all_players(ctx)
    target = players.get(idnum)
    if target is None:
        if ctx is not None:
            if ctx.author.id == idnum:
                await ctx.send(f"ERROR: {ctx.author.name}, you haven't joined the game yet")
            else:
                await ctx.send(f"ERROR: {ctx.author.name}, target player hasn't joined the game yet")
        raise UnknownPlayerException(idnum)
    return target

async def write_data(players):
    with open(PLAYERDATA, 'wb') as opened_file:
        pickle.dump(players, opened_file, protocol=pickle.HIGHEST_PROTOCOL)

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
            value=(f"use {ctx.prefix}upgrade <atrib> <amount>. "
                   f"You have been given 10 points for that.")
            )
        embed.add_field(
            name="List of attributes",
            value="```\nVIT - Vitality\nSTR - Strength\nDEX - Dexterity\nDEF - Defense\nLCK - Luck```",
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
        atrib = stats["atrib"]
        hp = stats['hp']
        loc = stats['loc']
        maxhp = stats['maxhp']
        equipment = player.eqp
        eqpinv = equipment.inv

        ratio = hp / maxhp
        display_points = int(ratio*100//2.5)
        full_points = display_points // 4
        leftover = display_points % 4
        block_characters = ["", "░", "▒", "▓", "█"]
        healthbar = block_characters[4] * full_points + block_characters[leftover]
        padding = 10 - len(healthbar)
        healthbar += padding * "─"
        if ratio > 0.5:
            g = 255
            r = int(255 * (1 - ratio) * 2)
        else:
            r = 255
            g = int(255 * ratio * 2)
        b = 40
        embed = discord.Embed(
            title=f"`HP: {hp}/{maxhp}`",
            colour=discord.Colour.from_rgb(r, g, b),
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
            value=("```py\n"
                   f"STR {atrib['str']:02d} + 00\n"
                   f"DEF {atrib['def']:02d} + 00\n"
                   f"VIT {atrib['vit']:02d} + 00\n"
                   f"DEX {atrib['dex']:02d} + 00\n"
                   f"LCK {atrib['str']:02d} + 00\n"
                   "───────────\n"
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
            name=f"You are in room {loc['room']}",
            value=f"The furthest you've been is room {loc['max']}",
            inline=True
            )
        
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(GameCog(bot))
