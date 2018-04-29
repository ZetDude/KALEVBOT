import os
import sys
from random import randint

import sqlite3 as lite
from discord.ext import commands
from lib import shipname as improved_shipname


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
                   r"|・ω・`）おやすみぃ♪",
                   ]

        selected_kaomoji = kaomoji[randint(0, len(kaomoji) - 1)]
        if target_user is None:
            combine = selected_kaomoji + " Good night!"
        elif target_user == "-list":
            combine = ""
            for i in kaomoji:
                combine = combine + i + "\n"
        else:
            try:
                target_user = await commands.MemberConverter(ctx, target_user)
                combine = selected_kaomoji + " Good night, " + target_user.name + "!"
            except:
                combine = selected_kaomoji + " Thank you, " + target_user + "!"

        await ctx.send(combine)

    @commands.command(name='developer', aliases=['dev'],
                      help="Try it!",
                      brief="Display the best developer of 2017")
    async def developer(self, ctx):
        await ctx.send("ZetDude best developer of 2017 and 2018 <:zetdev:357193244679077890>")

    @commands.command(name='shipname', aliases=['name'],
                      help="Create the shipname of two people.")
    async def shipname(self, ctx, name1, name2):
        names_shipname = improved_shipname.shipname(name1, name2)
        await ctx.send(f"{ctx.author}, I shall call it \"**{names_shipname}**\"!")
"""
    @commands.command(name='shipcount', aliases=['count'],
                      help="Get amount of ships created between people")
    async def shipcount(self, ctx, *args: discord.Member):
            ships = message.mentions
            seen = set()
            seen_add = seen.add
            ships = [x for x in ships if not (x in seen or seen_add(x))]
            ships_id = [str(x.id) for x in ships]
            ship_add = ':'.join(ships_id)
            with open(shipfile, "rb") as file:
                lines = pickle.loads(file.read())
            if not ships:
                ships = [message.author]
            if len(ships) < 2:
                return_message = ""
                mentions = search(lines, ships[0].id)
                print(mentions)
        #        mentions = sorted(mentions, key=lambda a: mentions[1])
                print(mentions)
                for k, j in mentions:
                    inmsg = k.split(":")
                    usern = []
                    for i in inmsg:
                        try:
                            usern.append(core.cl.get_user(int(i)).name)
                        except:
                            usern.append(str(i))
                    formatted = " x ".join(usern)
                    time_string = "times_message"
                    if j == 1:
                        time_string = "time"
                    return_message += "{}: shipped {} {}\n".format(formatted, j, time_string)
                core.send(message.channel, message.author.mention + ",\n```\n" + return_message + "\n```")
                return

            occ = lines.get(ship_add, 0)

            times_message = " times_message "
            if occ == 1:
                times_message = " time "
            final_message = (message.author.mention + ", they have been shipped " +
                        str(occ) + times_message + "before")

            core.send(message.channel, final_message)"""

    @shipname.error
    async def shipname_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author}, please use two names as arguments")

    #TODO: lucky command? is there a point?

    @commands.command(name='hug', aliases=['\U0001f917'],
                      help="Give someone a hug!")
    async def hug(self, ctx, *, target_users):
        mentions = list(ctx.message.mentions)
        sp = os.path.dirname(os.path.realpath(sys.argv[0]))
        message_split = target_users.split()
        if target_users == "" or [ctx.author] == mentions:
            combine = "Who are you going to hug, {}? Yourself?".format(ctx.author)
        else:
            con = lite.connect(sp + "/important/userdata.db")
            if message_split[0] == "-top":
                try:
                    fetch_amount = int(message_split[1])
                except ValueError:
                    ctx.send(f"That's not an integer, {message.author}")
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
                    mentions.remove(message.author)
                try:
                    converted_member = await commands.MemberConverter.convert(ctx, target_users)
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

                if core.cl.user.id in [x.id for x in mentions]:
                    if len(mentions) > 1:
                        recievers_without_self = list(mentions)
                        recievers_without_self.remove(core.cl.user)
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
