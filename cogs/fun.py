import os
import pickle
import sqlite3 as lite
import sys
import random

import discord
from discord.ext import commands
from lib import shipname as improved_shipname


def search(values, search_for):
    r = []
    for k in values:
        vs = str(values[k])
        if str(search_for) in str(k):
            r.append([k, str(vs)])
    return r

class FunCog():
    "fun fun fun fun fun fun"
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Fun Commands"

    @commands.command(name='night', aliases=['n', 'goodnight', 'nacht', 'öö', 'ööd', 'oyasumi',
    'おやすみ'],
                      help=(r"Wish someone a good night using a super cute kaomoji ^_^"),
                      brief="Wish someone a good night.")
    async def night(self, ctx, *, target_user=None):
        kaomoji = [r"お(^o^)や(^O^)す(^｡^)みぃ(^-^)ﾉﾞ",
                   r" .｡.:\*･ﾟ☆Goodヾ(\*´Д｀(\*ﾟωﾟ\* )Night☆.｡.:\*･ﾟ",
                   r" – =͟͟͞ (¦3[▓▓])",
                   r" ｡･:\*:･ﾟ★,｡･=^∇^\*=,｡･:\*:･ﾟ☆",
                   r"☆~\*.(UωU\*)おやすみぃ…\*~☆",
                   r"|・ω・`）おやすみぃ♪",]

        selected_kaomoji = random.choice(kaomoji)
        if target_user is None:
            await ctx.send(f"{selected_kaomoji} Good night!")
        elif target_user == "-list":
            combine = ""
            for i in kaomoji:
                combine = combine + i + "\n"
            await ctx.send(combine)
        else:
            try:
                target_user = await commands.MemberConverter().convert(ctx, target_user)
                await ctx.send(f"{selected_kaomoji} Good night, {target_user.name}!")
            except commands.BadArgument:
                await ctx.send(f"{selected_kaomoji} Good night, {target_user}!")

    @commands.command(name='developer', aliases=['dev'],
                      help="Try it!",
                      brief="Display the best developer of 2017")
    async def developer(self, ctx):
        await ctx.send("ZetDude best developer of 2017 and 2018 <:zetdev:357193244679077890>")

    @commands.command(name='shipname', aliases=['name'],
                      help="Create the shipname of two people.")
    async def shipname(self, ctx, name1, name2):
        names_shipname = improved_shipname.shipname(name1, name2)
        await ctx.send(f"{ctx.author.name}, I shall call it \"**{names_shipname}**\"!")

    @commands.command(name='shipcount', aliases=['count'],
                      help="Get amount of ships created between people")
    async def shipcount(self, ctx, *args: discord.Member):
        sp = os.path.dirname(os.path.realpath(sys.argv[0])) 
        # Get the folder the program is running from.
        shipfile = sp + "/important/shiplog.txt" 
        # Get the file where all shipping information is stored.

        # v  This part deals with removing duplicates in given users.
        seen = set()
        seen_add = seen.add
        ships = [x for x in args if not (x in seen or seen_add(x))]
        # ^  This part deals with removing duplicates in given users.
        # The list 'ships' contains the user(s) we want to get information about.

        ships_id = [str(x.id) for x in ships]
        # Create a duplicate of the 'ships' list but with IDs instead, 
        # as IDs are better to work around with internally.

        ship_add = ':'.join(ships_id)
        # Format the IDs into a format: 'id1:id2:id3...'
        # this format is needed as this is how ship information is stored in 'shiplog.txt'.

        with open(shipfile, "rb") as file:
            lines = pickle.loads(file.read())
            # Open 'shiplog.txt' and unpickle it.

        if not ships:
            ships = [ctx.author]
            # If the user gives no arguments with the command, 
            # assume the user wants information about themselves.

        if len(ships) == 1:
            return_message = ""
            mentions = search(lines, ships[0].id)
            # If the user gives only one user as an argument (or none, as shown above), 
            # find all the ships that user is contained in.

            ###mentions = sorted(mentions, key=lambda a: mentions[1])

            for k, j in mentions:
                inmsg = k.split(":")
                # take the 'id1:id2:id3...' format mentioned before and split it 
                # into the IDs it is composed from.

                usern = []
                for i in inmsg:
                    try:
                        i = await ctx.bot.get_user_info(i) 
                        # Convert the lower level ID into an username that people 
                        # actually can understand.
                        # Note that using 'await get_user_info' means that the bot 
                        # does not have to share any guilds with the target user!
                        usern.append(i.name)
                    except discord.NotFound:
                        usern.append(i)
                        # If somehow the target user does not exist on Discord, 
                        # fall back to just showing the ID

                formatted = " x ".join(usern)
                # Format the matching ship the user is in into the classic 'A x B' format
                times_message = "time" if j == 1 else "times"
                return_message += f"{formatted}: shipped {j} {times_message}\n"
                # Append the ship, with how many times it has been shipped, to a string, 
                # as we might need to cycle many times when the user is found in many ships.

            ctx.send(f"```\n{return_message}\n```")
            # Send out the whole list of matching ships.
            return

        else:
            occ = lines.get(ship_add, 0)
            # Else, if the user gives multple users as arguments, 
            # find how many times those specific users have been shipped before.

            times_message = "time" if j == 1 else "times"
            final_message = (f"{ctx.author}, they have been shipped {occ} {times_message} before")
            # Format it with the amount

            ctx.send(final_message)

    @shipname.error
    async def shipname_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.name}, please use two names as arguments")

    @commands.command(name='hug', aliases=['\U0001f917'],
                      help="Give someone a hug!")
    async def hug(self, ctx, *, target_users):
        mentions = list(ctx.message.mentions)
        sp = os.path.dirname(os.path.realpath(sys.argv[0]))
        message_split = target_users.split()
        if target_users == "" or [ctx.author] == mentions:
            combine = f"Who are you going to hug, {ctx.author.name}? Yourself?"
        else:
            con = lite.connect(sp + "/important/userdata.db")
            if message_split[0] == "-top":
                try:
                    fetch_amount = int(message_split[1])
                except ValueError:
                    ctx.send(f"That's not an integer, {ctx.author}")
                    return
                except IndexError:
                    fetch_amount = 5
                with con:
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Hug ORDER BY Hugs DESC LIMIT ?", (fetch_amount, ))
                    rows = cur.fetchall()
                    combine = "```\nTOP HUGGERS:\n---------\n"
                    for row in rows:
                        target_user = ctx.bot.get_user(row[0])
                        if target_user is None:
                            break
                        combine += target_user.name if not None else row[0]
                        combine += " - " + str(row[1]) + "\n"
                    combine += "\n```"
            else:
                if ctx.author in mentions:
                    mentions.remove(ctx.author)
                try:
                    converted_member = await commands.MemberConverter().convert(ctx, target_users)
                    mentions.append(converted_member)
                except commands.BadArgument:
                    pass
                with con:
                    cur = con.cursor()
                    cur.execute("SELECT COALESCE(Hugs, 0) FROM Hug WHERE id = ?", (ctx.author.id, ))
                    row = cur.fetchone()
                    hugs = 0 if row is None else row[0]
                    mentions_without_bot = list(mentions)
                    for u in mentions_without_bot[::1]: 
                        #need to iterate backwards to not jump over anything when removing
                        if u.bot:
                            mentions_without_bot.remove(u)
                    hugs += len(mentions_without_bot)
                    cur.execute("INSERT OR IGNORE INTO Hug VALUES(?, ?)", (ctx.author.id, hugs))
                    cur.execute("UPDATE Hug SET Hugs=? WHERE id=?", (hugs, ctx.author.id))

                if ctx.bot.id in [x.id for x in mentions]:
                    if len(mentions) > 1:
                        recievers_without_self = list(mentions)
                        recievers_without_self.remove(ctx.bot.user)
                        recievers = " and ".join([x.name for x in recievers_without_self])
                        combine = "{} gave {} a hug, and I hug you back! \U0001f917 (You've given {} hug(s) in total)".format(ctx.author, recievers, hugs)
                    else:
                        combine = "I hug you back, {}! \U0001f917 (You've given {} hug(s) in total)".format(ctx.author, hugs)
                elif len(mentions) > 0:
                    recievers = " and ".join([x.name for x in mentions])
                    combine = "{} gave {} a hug! (You've given {} hug(s) in total)".format(ctx.author, recievers, hugs)
                else:
                    combine = "{} gave {} a hug! (You've given {} hug(s) in total)".format(ctx.author, target_users, hugs)
        ctx.send(combine)

def setup(bot):
    bot.add_cog(FunCog(bot))
