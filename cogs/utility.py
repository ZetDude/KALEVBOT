import os
import re
import sqlite3 as lite
import time
from datetime import datetime

import arrow
import discord
from discord.ext import commands

import parsedatetime

QUOTES_REGEX = '(["].{0,2000}["])'

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def get_free_space_mb(dirname):
    """Return folder/drive free space (in megabytes)."""
    st = os.statvfs(dirname) # pylint: disable=no-member
    return st.f_bavail * st.f_frsize

class UtilityCog():
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Utility"

    @commands.command(name='emote', aliases=['e'],
                      help="Get all the emotes the bot can use or a specific emote.",
                      brief="Get an emote or all of them.")
    async def emote(self, ctx, *, emote_lookup=None):
        if emote_lookup is None:
            # this code provide by xithiox
            emotes = ctx.bot.emojis
            output = ''
            for i in emotes:
                output += str(i)
                if len(output) + 33 >= 2000:
                    await ctx.send(output)
                    output = ''
            await ctx.send(output)
        else:
            emote_lookup = emote_lookup.split()
            replaced_emotes = []
            detail = False
            if "-n" in emote_lookup:
                emote_lookup.remove("-n")
                detail = True
            for emote in emote_lookup:
                emote = emote.strip(':')
                pos = discord.utils.get(ctx.bot.emojis, name=emote)
                if pos is None:
                    replaced_emotes.append(emote)
                    continue
                if detail:
                    replaced_emotes.append(f"{str(pos)} from {pos.guild} by {pos.guild.owner}")
                else:
                    replaced_emotes.append(str(pos))
            await ctx.send("".join(replaced_emotes))

    @commands.command(name='ipa', aliases=[],
                      help="Display multiple options for getting the IPA chart and/or keyboard.",
                      brief="Get the link for the IPA chart.")
    async def ipa(self, ctx):
        await ctx.send("""The IPA (International Phonetic Alphabet) chart in various forms:

<http://www.ipachart.com/> Simple version of the graph with sounds
<http://westonruter.github.io/ipa-chart/keyboard/> A keyboard site for writing all things IPA using the on-screen buttons
<https://web.uvic.ca/ling/resources/ipa/charts/IPAlab/IPAlab.htm> A more detailed version of the alphabet with interactive buttons
""")

    @commands.command(name='server', aliases=['guild', 'analyze'],
                      help="Analyze the current guild",
                      brief="Analyze the current guild")
    async def server(self, ctx):
        member_list = ctx.guild.members
        humans = 0
        bots = 0
        for i in member_list:
            if i.bot:
                bots += 1
            else:
                humans += 1
        embed = discord.Embed(
            colour=0xb8e986,
            description=f"owned by {ctx.guild.owner}"
            )
        embed.set_thumbnail(
            url=ctx.guild.icon_url
            )
        embed.set_author(
            name=ctx.guild.name,
            url=ctx.guild.icon_url
            )
        embed.set_footer(
            text="and i'm on the guild, which is the best part!"
            )
        embed.add_field(
            name=f"__{ctx.guild.member_count}__ members",
            value=f"of which __{humans}__ are humans and __{bots}__ are bots"
            )
        await ctx.send(embed=embed)

    #@commands.command(name='tag', aliases=['faq', 't'],
    #                  help="Answer FAQ",
    #                  brief="Answer FAQ")
    #async def tag(self, ctx):

    @commands.command(name='status', aliases=['test'],
                      help=("Check the status and information of the bot, "
                            "such as run time and disk space."),
                      brief="Show if the bot is still working.")
    async def status(self, ctx):
        delta_uptime = datetime.utcnow() - ctx.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        diskspace = get_free_space_mb("/")
        diskspaceg = diskspace / 1024 / 1024 / 1024
        embed = discord.Embed(
            title="It's working!",
            colour=0x1,
            timestamp=datetime.utcnow())
        embed.add_field(
            name="Uptime",
            value=f"{days}d, {hours}h, {minutes}m, {seconds}s",
            inline=True
            )
        embed.add_field(
            name="Latency",
            value=f"{int(ctx.bot.latency*1000)}ms",
            inline=True
            )
        embed.add_field(
            name="Remaining disk space",
            value=f"{diskspaceg:.2f} GB ({diskspace} bytes)",
            inline=True
            )
        embed.add_field(
            name="Present in 10 guilds",
            value="serving 680 users",
            inline=True
        )

        await ctx.send(embed=embed)

    @commands.command(name='avatar', aliases=['pfp', 'profile', 'profilepicture'],
                      help="Display your or someone else's profile picture",
                      brief="Display your avatar")
    async def avatar(self, ctx, *, target_user = None):
        if target_user is None:
            target_user = ctx.author
        else:
            target_user = await commands.MemberConverter().convert(ctx, target_user)
        avatar_url = target_user.avatar_url

        embed = discord.Embed()
        embed.set_image(
            url=avatar_url
            )
        embed.set_author(
            name=target_user.name,
            url=avatar_url
            )

        await ctx.send(embed=embed)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.name}, {error.args[0].lower()}")

    @commands.command(name='remind', aliases=['remindme', 'r', 'reminder'],
                      help="Adds a reminder",
                      usage="<when> \"message\" (or) -list (or) -delete <reminder_number>")
    async def remind(self, ctx, *, input_text="1 day"):
        input_text = input_text.split("\n")[0]
        flags = input_text.split()
        con = lite.connect("important/data.db")
        if "-list" in flags:
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Reminders WHERE requester = ?", (ctx.author.id, ))
                matching = cur.fetchall()
                return_message = "All reminders you have set:\n"
                matching.sort(key=lambda tup: arrow.get(str(tup[4])))
                for y, i in enumerate(matching):
                    arrow_time = arrow.get(str(i[2]), "YYYYMMDDHHmmss")
                    formatted_time = arrow_time.format("YYYY-MM-DD HH:mm:ss")
                    humanized_time = arrow_time.humanize()
                    return_message += f"`{y+1}`: {humanized_time} ({formatted_time}) - {i[0]}\n"
                await ctx.send(return_message)
                return
        if "-delete" in flags:
            flags.remove('-delete')
            delete_number = flags[0]
            if delete_number == "all":
                with con:
                    cur = con.curson()
                    cur.execute("DELETE FROM Reminders WHERE requester = ?", (ctx.author.id, ))
                    await ctx.send(f"{ctx.author.name}, deleted all!")
            else:
                try:
                    delete_number = int(delete_number) - 1
                except ValueError:
                    await ctx.send(f"{ctx.author.name}, integers please")
                    return
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Reminders WHERE requester = ?", (ctx.author.id, ))
                matching = cur.fetchall()
                matching.sort(key=lambda tup: arrow.get(str(tup[4])))
                try:
                    target_entry = matching[delete_number]
                except IndexError:
                    await ctx.send(f"{ctx.author.name}, reminder number out of range")
                    return
                await ctx.send(f"{ctx.author.name}, deleted entry `{delete_number}`: {i[0]}")
                cur.execute(
                    "DELETE FROM Reminders WHERE request_time = ? AND requester = ?",
                    (target_entry[4], target_entry[3]))
                return
        included_message = "This is a default message"
        cal = parsedatetime.Calendar()
        input_text_regex = re.search(QUOTES_REGEX, input_text)
        if input_text_regex:
            included_message = input_text_regex.group().strip('"')
        remind_time = re.sub(QUOTES_REGEX, '', input_text)
        remind_time = cal.parse(remind_time, datetime.utcnow())
        error_message = ""
        if remind_time[1] == 0:
            remind_time = cal.parse("1 day", datetime.utcnow())
            error_message = "Couldn't parse time, defaulting to 1 day\n"
        if remind_time[0] < time.gmtime():
            await ctx.send(f"{ctx.author.name}, time is in the past.")
            return
        time_format = time.strftime('%Y-%m-%d %H:%M:%S', remind_time[0])
        await ctx.send((f"{error_message}"
                        f"{ctx.author.name}, reminding you at "
                        f"{time_format} ({arrow.get(time_format).humanize()})"))
        remind_date = time.strftime('%Y%m%d%H%M%S', remind_time[0])
        request_date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        message_link = ctx.message.jump_to_url.replace('?jump=', '/')
        requester = ctx.author.id
        with con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO Reminders VALUES(?, ?, ?, ?, ?)", 
                (included_message, message_link, remind_date, requester, request_date))

def setup(bot):
    bot.add_cog(UtilityCog(bot))
