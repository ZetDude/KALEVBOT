# -*- coding: utf-8 -*-

import os
import pickle
import random
import sqlite3 as lite
import sys

import discord
from discord.ext import commands
from lib import shipname_module as improved_shipname


def search(values, search_for):
    "Finds all the values in a list where a target string is present"
    found_values = []
    for k in values:
        value_string = str(values[k])
        if str(search_for) in str(k):
            found_values.append([k, str(value_string)])
    return found_values


def remove_duplicates(values):
    seen = set()
    seen_add = seen.add
    values = [x for x in values if not (x in seen or seen_add(x))]
    return values


class FunCog():
    "fun fun fun fun fun fun"

    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Fun Commands"

    @commands.command(name='night', aliases=['n', 'goodnight', 'nacht', 'öö', 'ööd', 'oyasumi',
                                             '\u304a\u3084\u3059\u307f'],
                      help=(
                          r"Wish someone a good night using a super cute kaomoji! ^_^"),
                      brief="Wish someone a good night.")
    async def night(self, ctx, *, target_user=None):
        kaomoji = [r"お(^o^)や(^O^)す(^｡^)みぃ(^-^)ﾉﾞ",
                   r" .｡.:\*･ﾟ☆Goodヾ(\*´Д｀(\*ﾟωﾟ\* )Night☆.｡.:\*･ﾟ",
                   r" – =͟͟͞ (¦3[▓▓])",
                   r" ｡･:\*:･ﾟ★,｡･=^∇^\*=,｡･:\*:･ﾟ☆",
                   r"☆~\*.(UωU\*)おやすみぃ…\*~☆",
                   r"|・ω・`）おやすみぃ♪", ]

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

    @commands.command(name='thank', aliases=['thanks', 'arigato', 'arigatou', 'arigatoo',
                                             'merci', 'arigatō', 'danke', 'aitah', 'aitäh',
                                             '\u3042\u308a\u304c\u3068\u3046'],
                      help=(r"Thank someone using a super cute kaomoji! ^_^"),
                      brief="Thank someone.")
    async def thank(self, ctx, *, target_user=None):
        kaomoji = [r"♪(･ω･)ﾉ",
                   r"(\*ゝω・)ﾉ",
                   r"ﾟ･:,｡★＼(^-^ )♪ありがと♪( ^-^)/★,｡･:･ﾟ",
                   r"(★^O^★)",
                   r"☆\*:.｡. o(≧▽≦)o .｡.:\*☆",
                   r"(ノ^_^)ノ",
                   r"(ﾉﾟ▽ﾟ)ﾉ",
                   r"(ﾉ´ヮ´)ﾉ\*:･ﾟ✧",
                   r"(\*^3^)/\~☆",
                   r"<(\_ \_\*)> ｱﾘｶﾞﾄｫ",
                   r"ありがとぅございますっっヽ(●´∀\`)人(´∀\`●)ﾉ",
                   r"ありがとうございましたm(\*-ω-)m",
                   r"+｡:.ﾟヽ(\*´∀)ﾉﾟ.:｡+ﾟｧﾘｶﾞﾄｩ"
                   ]

        selected_kaomoji = random.choice(kaomoji)
        if target_user is None:
            await ctx.send(f"{selected_kaomoji} Thank you!")
        elif target_user == "-list":
            combine = ""
            for i in kaomoji:
                combine = combine + i + "\n"
            await ctx.send(combine)
        else:
            try:
                target_user = await commands.MemberConverter().convert(ctx, target_user)
                if target_user == ctx.bot.user:
                    await ctx.send(f"You're welcome, {ctx.author.name}! \\\u2764")
                elif target_user == ctx.author:
                    await ctx.send(f"Why would I need to thank you, {ctx.author.name}?")
                else:
                    await ctx.send(f"{selected_kaomoji} Thank you, {target_user.name}!")
            except commands.BadArgument:
                await ctx.send(f"{selected_kaomoji} Thank you, {target_user}!")

    @commands.command(name='developer', aliases=['dev'],
                      help="Try it!",
                      brief="Display the best developer of 2017")
    async def developer(self, ctx):
        await ctx.send("ZetDude best developer of 2017 and 2018 <:developer:352469145989939200>")

    @commands.command(name='shipname', aliases=['name'],
                      help="Create the shipname of two people.")
    async def shipname(self, ctx, name1, name2):
        names_shipname = improved_shipname.shipname(name1, name2)
        await ctx.send(f"{ctx.author.name}, I shall call it \"**{names_shipname}**\"!")

    @commands.command(name='shipcount', aliases=['count'],
                      help="Get amount of ships created between people")
    async def shipcount(self, ctx, *ships: discord.Member):
        running_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        # Get the folder the program is running from.
        shipfile = running_path + "/important/shiplog.pickle"
        # Get the file where all shipping information is stored.

        ships = remove_duplicates(ships)
        # The list 'ships' contains the user(s) we want to get information about.

        ships_format = ':'.join([str(x.id) for x in ships])
        # Format the IDs into a format: 'id1:id2:id3...'
        # this format is needed as this is how ship information is stored in 'shiplog.txt'.

        try:
            with open(shipfile, "rb") as opened_file:
                lines = pickle.loads(opened_file.read())
                # Open 'shiplog.txt' and unpickle it.
        except FileNotFoundError:
            await ctx.send(f"I couldn't find the shipping file ({shipfile})")
            return
            # If shiplog isn't found
        except pickle.UnpicklingError:
            await ctx.send("Shipping data file is corrupt, cannot fetch data.")
            return
            # If pickle is a bitc-... If something goes wrong with unpickling

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
                usern = []
                for i in k.split(":"):
                    # take the 'id1:id2:id3...' format mentioned before and split it
                    # into the IDs it is composed from.
                    try:
                        found_user = ctx.bot.get_user(int(i))
                        # Convert the lower level ID into an username that people
                        # actually can understand.
                        # The function get_user() only works if the target shares
                        # a server with the bot.
                        # Returns None if user is not found.
                        if found_user is None:
                            found_user = ctx.bot.get_user_info(i)
                            # If the search fails, assume the user doesn't share a
                            # server with the bot, and use another function instead.
                            # The function get_user_info() works regardless of
                            # the target sharing servers with the bot, however, it is
                            # terribly slow, therefore we use get_user() as much as we can.
                        usern.append(found_user.name)
                    except discord.NotFound:
                        usern.append(i)
                        # If somehow the target user does not exist on Discord,
                        # fall back to just showing the ID
                times_message = "time" if j == 1 else "times"
                return_message += f"{' x '.join(usern)}: shipped {j} {times_message}\n"
                # Format the matching ship the user is in into the classic 'A x B' format.
                # Append the ship, with how many times it has been shipped, to a string,
                # as we might need to cycle many times when the user is found in many ships.

            await ctx.send(f"```\n{return_message}\n```")
            # Send out the whole list of matching ships.
            return

        else:
            occ = lines.get(ships_format, 0)
            # Else, if the user gives multple users as arguments,
            # find how many times those specific users have been shipped before.

            times_message = "time" if j == 1 else "times"

            await ctx.send(f"{ctx.author}, they have been shipped {occ} {times_message} before")
            # Format and send it with the amount

    @commands.command(name='ship', aliases=['otp'],
                      help="Ship someone with someone else.",
                      brief="Ship someone with someone else. uwu")
    async def ship(self, ctx, *ships: discord.Member):
        running_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        shipfile = running_path + "/important/shiplog.pickle"
        if ctx.message.author in ships:
            await ctx.send((f"{ctx.message.author.name}, "
                            "I don't think you can ship yourself with someone"))
            return
        ships = remove_duplicates(ships)
        if len(ships) < 2:
            await ctx.send(f"{ctx.message.author.name}, mention at least two people in the message")
            return
        ships_names = [x.name for x in ships]
        ships_format = ":".join(sorted([str(x.id) for x in ships], key=int))
        try:
            with open(shipfile, "rb") as opened_file:
                lines = pickle.loads(opened_file.read())
        except FileNotFoundError:
            lines = {}
            with open(shipfile, 'w'):
                pass
        except pickle.UnpicklingError:
            await ctx.send("Hugs file is corrupt, cannot fetch data.")
            return
        occ = lines.get(ships_format, 0)

        times_message = "time" + ("" if occ == 1 else "s")

        lines[ships_format] = occ + 1

        with open(shipfile, 'wb') as opened_file:
            pickle.dump(lines, opened_file)

        shipname = ""

        if len(ships) == 2:
            first_half = ships_names[0]
            second_half = ships_names[-1]
            final = improved_shipname.shipname(first_half, second_half)
            shipname = "I shall call it \"**" + final + "**\""

        await ctx.send((f"{ctx.message.author.name} totally ships {' and '.join(ships_names)}"
                        f"\nThey have been shipped {occ} {times_message} before"
                        f"\n{shipname}"))

    @shipname.error
    async def shipname_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.name}, please use two names as arguments")

    @shipcount.error
    @ship.error
    async def ship_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.name}, {error.args[0].lower()}")

    @commands.command(name='hug', aliases=['\U0001f917'],
                      help="Give someone a hug!")
    async def hug(self, ctx, *target_users):
        target_users = list(target_users)
        running_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        con = lite.connect(running_path + "/important/userdata.db")
        if target_users[0] == "-top":
            try:
                fetch_amount = int(target_users[1])
            except ValueError:
                await ctx.send(f"That's not an integer, {ctx.author}")
                return
            except IndexError:
                fetch_amount = 5
            with con:
                try:
                    cur = con.cursor()
                    cur.execute(
                        "SELECT * FROM Hug ORDER BY Hugs DESC LIMIT ?", (fetch_amount, ))
                    rows = cur.fetchall()
                    combine = "```\nTOP HUGGERS:\n---------\n"
                    for row in rows:
                        target_user = ctx.bot.get_user(row[0])
                        if target_user is None:
                            break
                        combine += target_user.name if not None else row[0]
                        combine += " - " + str(row[1]) + "\n"
                    combine += "\n```"
                except lite.OperationalError as err:
                    if str(err) == "no such table: Hug":
                        cur.execute(
                            "CREATE TABLE Hug(id INT NOT NULL UNIQUE, Hugs INT);")
                        await ctx.send("No hug data was recorded, created file now.")
        else:
            targets = []
            for i in target_users:
                try:
                    converted_member = await commands.MemberConverter().convert(ctx, i)
                except commands.BadArgument:
                    converted_member = i
                targets.append(converted_member)
            targets = remove_duplicates(targets)
            if [ctx.author] == targets:
                await ctx.send(f"Who are you going to hug, {ctx.author.name}? Yourself?")
                return
            if ctx.author in targets:
                targets.remove(ctx.author)
            with con:
                try:
                    cur = con.cursor()
                    cur.execute(
                        "SELECT COALESCE(Hugs, 0) FROM Hug WHERE id = ?", (ctx.author.id, ))
                    row = cur.fetchone()
                    hugs = 0 if row is None else row[0]
                except lite.OperationalError as err:
                    if str(err) == "no such table: Hug":
                        cur.execute(
                            "CREATE TABLE Hug(id INT NOT NULL UNIQUE, Hugs INT);")
                        await ctx.send("Created new hugs database table.")
                        hugs = 0
                mentions_without_bot = list(targets)
                for user in mentions_without_bot[::1]:
                    # Need to iterate backwards to not jump over anything when removing.
                    if isinstance(user, str):
                        mentions_without_bot.remove(user)
                    elif user.bot:
                        mentions_without_bot.remove(user)
                hugs += len(mentions_without_bot)
                cur.execute("INSERT OR IGNORE INTO Hug VALUES(?, ?)",
                            (ctx.author.id, hugs))
                cur.execute("UPDATE Hug SET Hugs=? WHERE id=?",
                            (hugs, ctx.author.id))

            if ctx.bot.user.id in [x.id for x in targets if not isinstance(x, str)]:
                if len(targets) > 1:
                    recievers_without_self = list(targets)
                    recievers_without_self.remove(ctx.bot.user)
                    recievers = " and ".join([x.name if not isinstance(
                        x, str) else x for x in recievers_without_self])
                    combine = ("{} gave {} a hug, and I hug you back! "
                               "\U0001f917 (You've given {} hug(s) in total)".format(
                                   ctx.author, recievers, hugs))
                else:
                    combine = ("I hug you back, {}! "
                               "\U0001f917 (You've given {} hug(s) in total)".format(
                                   ctx.author, hugs))
            elif targets:
                recievers = " and ".join(
                    [x.name if not isinstance(x, str) else x for x in targets])
                combine = "{} gave {} a hug! (You've given {} hug(s) in total)".format(
                    ctx.author, recievers, hugs)
            else:
                combine = "{} gave {} a hug! (You've given {} hug(s) in total)".format(
                    ctx.author, target_users, hugs)
        await ctx.send(combine)


def setup(bot):
    bot.add_cog(FunCog(bot))
