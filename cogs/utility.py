import os
import re
import sqlite3 as lite
import time
import calendar
from datetime import datetime

import arrow
import discord
from discord.ext import commands
from lib import customconverter as cconv

import parsedatetime

QUOTES_REGEX = '(["].{0,1000}["])'

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
            # this code provided by xithiox
            emotes = sorted(ctx.bot.emojis, key=lambda a: a.name)
            output = ''
            for i in emotes:
                output += str(i)
                if len(output) + 33 >= 2000:
                    await ctx.author.send(output)
                    output = ''
            await ctx.author.send(output)
            await ctx.send(f"{ctx.author.name}, I've privately sent you all {len(ctx.bot.emojis)} emotes that I know")
        else:
            emote_lookup = emote_lookup.split()
            detail = False
            if "-n" in emote_lookup:
                emote_lookup.remove("-n")
                detail = True
            if len(emote_lookup) == 1:
                if detail:
                    matching = [f"{str(x)} from {x.guild} by {x.guild.owner}\n" 
                            for x in ctx.bot.emojis if x.name.lower() == emote_lookup[0].lower()]
                else:
                    matching = [str(x) for x in ctx.bot.emojis if 
                            x.name.lower() == emote_lookup[0].lower()]
                if not matching:
                    await ctx.send(f"{ctx.author.name}, I don't know such an emote")
                else:
                    await ctx.send("".join(matching))
            else:
                replaced_emotes = []
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
            text="and I'm on the guild, which is the best part!"
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
            name=f"Present in {len(ctx.bot.guilds)} guilds",
            value=f"serving {len(ctx.bot.users)} users",
            inline=True
        )

        await ctx.send(embed=embed)

    @commands.command(name='avatar', aliases=['pfp', 'profile', 'profilepicture'],
                      help="Display your or someone else's profile picture",
                      brief="Display your avatar")
    async def avatar(self, ctx, *, target_user=None):
        if target_user is None:
            target_user = ctx.author
        else:
            target_user = await cconv.HybridConverter().convert(ctx, target_user)
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
                      usage="<when> \"message\" OR -list OR -delete <reminder_number>")
    async def remind(self, ctx, *, input_text="1 day"):
        # If the user gives a multi-line input, only read the first one.
        input_text = input_text.split("\n")[0]
        # Split all words to delect flags in them.
        flags = input_text.split()
        # Make a sqlite3 connection to the database where reminders are stored.
        con = lite.connect("important/data.db")

        # flag detection
        if "-list" in flags:
            with con:
                # Get all database entries requested by the author
                cur = con.cursor()
                cur.execute("SELECT * FROM Reminders WHERE requester = ?", (ctx.author.id, ))
                matching = cur.fetchall()

                if not matching:
                    await ctx.send(f"{ctx.author.name}, you do not have any reminders!")
                    return

                return_message = "All reminders you have set:\n"
                # Sort by creation date for consistency
                matching.sort(key=lambda tup: arrow.get(str(tup[4])))
                for y, i in enumerate(matching):
                    arrow_time = arrow.get(str(i[2]), "YYYYMMDDHHmmss")
                    formatted_time = arrow_time.format("YYYY-MM-DD HH:mm:ss")
                    humanized_time = arrow_time.humanize()
                    # Format example: `4`: in 3 days (2018-07-02 00:18:23) - 1 year since the relay
                    return_message += f"`{y+1}`: {humanized_time} ({formatted_time}) - {i[0]}\n"
                await ctx.send(return_message)
        elif "-delete" in flags:
            # Make sure we don't read the actual flag as the value
            flags.remove('-delete')
            delete_number = flags[0]
            if delete_number == "all":
                with con:
                    # Count all the entires then delete them all
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Reminders WHERE requester = ?", (ctx.author.id, ))
                    entry_amount = len(cur.fetchall())
                    cur.execute("DELETE FROM Reminders WHERE requester = ?", (ctx.author.id, ))
                    await ctx.send(f"{ctx.author.name}, deleted all {entry_amount} reminders!")
            else:
                try:
                    # Since the external list is 1-indexed but the internal list is 0-indexed
                    delete_number = int(delete_number) - 1
                except ValueError:
                    await ctx.send(f"{ctx.author.name}, integers please")
                    return
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM Reminders WHERE requester = ?", (ctx.author.id, ))
                matching = cur.fetchall()
                # Sort by creation date for consistency
                matching.sort(key=lambda tup: arrow.get(str(tup[4])))
                try:
                    target_entry = matching[delete_number]
                except IndexError:
                    await ctx.send(f"{ctx.author.name}, reminder number out of range")
                    return
                await ctx.send((f"{ctx.author.name}, deleted entry"
                                f"`{delete_number + 1}`: {target_entry[0]}"))
                # This might delete more than one, actually, if you managed to make two reminders
                # at the exact same second somehow. This is such an edge case though,
                # so I don't worry about it.
                cur.execute(
                    "DELETE FROM Reminders WHERE request_time = ? AND requester = ?",
                    (target_entry[4], target_entry[3]))
        else:
            # If the user doesn't supply a message this one will be used
            included_message = "This is a default message"
            # parsedatetime module functionality
            cal = parsedatetime.Calendar()

            # Detect and get the message included which will need to be in quotes
            input_text_regex = re.search(QUOTES_REGEX, input_text)
            if input_text_regex:
                included_message = input_text_regex.group().strip('"')

            # Get rid of the message in the quotes and then parse the remainder with parsedatetime
            # parsedatetime returns a tuple (parsed_time, status_code)
            remind_time = re.sub(QUOTES_REGEX, '', input_text)
            remind_time = cal.parse(remind_time, datetime.utcnow())

            # Things that could go wrong
            error_message = ""
            # If parsedatetime returns status_code 0, something went wrong. This is non-fatal
            if remind_time[1] == 0:
                remind_time = cal.parse("1 day", datetime.utcnow())
                error_message = "Couldn't parse time, defaulting to 1 day\n"
            remind_time = time.gmtime(calendar.timegm((*remind_time[0][:8], time.gmtime()[8])))
            if remind_time < time.gmtime():
                await ctx.send(f"{ctx.author.name}, time is in the past.")
                return
            elif remind_time == time.gmtime():
                await ctx.send(f"{ctx.author.name}, I don't think you needed a reminder for that")
                return
            # remind_date needs to be formatted in this way for it to be comparable with other times
            # like an int.
            remind_date = time.strftime('%Y%m%d%H%M%S', remind_time)
            request_date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
            time_format = time.strftime('%Y-%m-%d %H:%M:%S', remind_time)
            arrow_time = arrow.get(time_format)#.replace(tzinfo="+00:00")
            if int(remind_date) > 99991231235959:
                await ctx.send((f"sorry, time traveller {ctx.author.name}, "
                                f"but I had to set the limit to 9999-12-31 23:59:59"))
                remind_date = "99991231235959"
                time_format = "9999-12-31 23:59:59"
            await ctx.send((f"{error_message}"
                            f"{ctx.author.name}, reminding you at "
                            f"{time_format} ({arrow_time.humanize()})"))
            message_link = ctx.message.jump_url
            requester = ctx.author.id
            with con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO Reminders VALUES(?, ?, ?, ?, ?)",
                    (included_message, message_link, remind_date, requester, request_date))

    @commands.command(name='user', alias=['profile'],
                      help="Get info about yourself or an user")
    async def user(self, ctx, target_user: discord.Member = None):
        target_user = target_user or ctx.author
        shared = [x.get_member(target_user.id).nick for x in ctx.bot.guilds if
                  x.get_member(target_user.id) is not None]
        known_as = [y for y in shared if y is not None]
        known_as = ", ".join([f'"{x}"' for x in known_as])
        activity = target_user.activity
        activity_type = target_user.activity.type
        if activity_type == discord.ActivityType.playing:
            activity_message = f"and playing __{activity.name}__"
        elif activity_type == discord.ActivityType.streaming:
            if activity.details:
                activity_message = f"and streaming __{activity.details}__ on twitch"
            else:
                activity_message = "and streaming on twitch"
            activity_message += f"\n[watch {activity.name}](activity.url)"
        elif activity_type == discord.ActivityType.listening:
            activity_message = (f"and listening to __{activity.title}__ by "
                                f"__{activity.artist}__ on Spotify")
        elif activity_type == discord.ActivityType.watching:
            activity_message = f"and watching __{activity}__"
        elif activity_type == discord.ActivityType.unknown:
            activity_message = f"and breaking Discord completely"
        else:
            activity_message = f"and doing something, somewhere, probably"


        embed = discord.Embed(
            title=str(target_user),
            colour=target_user.color,
            description=f"Also known as {known_as}",
            timestamp=datetime.utcnow())

        embed.set_thumbnail(
            url=target_user.avatar_url_as(static_format="png"))
        embed.set_footer(
            text=target_user.id,
            icon_url=target_user.default_avatar_url)

        embed.add_field(
            name=f"currently __{target_user.status}__",
            value=activity_message,
            inline=True)

        embed.add_field(
            name="Shared servers",
            value=f"__{len(shared)}__",
            inline=True)

        embed.add_field(
            name="Amount of roles",
            value=(f"__{len(target_user.roles)}__,"
                   "with the top one being __{target_user.top_role}__"),
            inline=True)

        embed.add_field(
            name=f"Joined __{ctx.guild}__ on {target_user.joined_at}",
            value=f"about {arrow.get(target_user.joined_at).humanize()}",
            inline=True)

        embed.add_field(
            name=f"Joined Discord on on {target_user.created_at}",
            value=f"about {arrow.get(target_user.created_at).humanize()}",
            inline=True)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UtilityCog(bot))
