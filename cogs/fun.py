# -*- coding: utf-8 -*-

import pickle
import random
import sqlite3 as lite
import subprocess

import discord
from discord.ext import commands
from lib import shipname_module as improved_shipname


def search(values, search_for):
    "Finds all the values in dict `values` where `search_for` is somewhere in the key"
    found_values = []  # Initialize an empty list that will be the final list.
    for k in values:  # Iterate through every key in the given dictionary.
        value_string = str(values[k])  # The corresponding value for the key we are currently on.
        if str(search_for) in str(k):  # If the string we are looking for is in the key.
            found_values.append([k, value_string])
            # Append the value and the key to the final list.
    return found_values  # Return the final list.


def remove_duplicates(values):
    "Return the list `values` with duplicates removed"
    # I'm going to be honest, I just found this on StackOverflow so I have no idea how it works.
    seen = set()
    seen_add = seen.add
    values = [x for x in values if not (x in seen or seen_add(x))]
    return values


class FunCog():
    "fun fun fun fun fun fun"

    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Fun"

    @commands.command(name='night', aliases=['n', 'goodnight', 'nacht', 'öö', 'ööd', 'oyasumi',
                                             '\u304a\u3084\u3059\u307f'],
                      help=(r"Wish someone a good night using a super cute kaomoji! ^_^"),
                      brief="Wish someone a good night.")
    async def night(self, ctx, *, target_user=None):
        """
        `target_user` is the target's nickname, username, or ID. The converting to the user object
        is handled by discord.ext.commands.MemberConverter(). That user is wished a good night by
        the bot, with a kaomoji emoticon in front. `target_user` can also be the argument "-list",
        in which case the bot returns all the kaomoji emoticons associated with this command
        """
        kaomoji = [r"お(^o^)や(^O^)す(^｡^)みぃ(^-^)ﾉﾞ",
                   r" .｡.:\*･ﾟ☆Goodヾ(\*´Д｀(\*ﾟωﾟ\* )Night☆.｡.:\*･ﾟ",
                   r" – =͟͟͞ (¦3[▓▓])",
                   r" ｡･:\*:･ﾟ★,｡･=^∇^\*=,｡･:\*:･ﾟ☆",
                   r"☆~\*.(UωU\*)おやすみぃ…\*~☆",
                   r"|・ω・`）おやすみぃ♪", ]
        # Define the list of kaomoji emoticons the bot will be using. Because of discord formatting
        # most special characters are escaped with a \, however to stop python formatting,
        # r-strings are used (r"").

        selected_kaomoji = random.choice(kaomoji)
        # Choose a random kaomoji that we'll use for this use of the command.

        if target_user is None:  # If the user does not supply a target user.
            await ctx.send(f"{selected_kaomoji} Good night!") #  Return a generic response.
        elif target_user == "-list":  # If the user uses the argument "-list".
            await ctx.send("\n".join(kaomoji))  # Join together all the kaomoji and send them.
        else:  # If the target user is actually given.
            try:
                target_user = await commands.MemberConverter().convert(ctx, target_user)
                # Try to convert the string to an user using discord.ext.commands.MemberConverter().
                await ctx.send(f"{selected_kaomoji} Good night, {target_user.name}!")
                # Wish them a good night using their username.

            except commands.BadArgument:  # If there wasn't an user with that name.
                await ctx.send(f"{selected_kaomoji} Good night, {target_user}!")
                # Fall back to just using the inputted string with no conversion.

    @commands.command(name='thank', aliases=['thanks', 'arigato', 'arigatou', 'arigatoo',
                                             'merci', 'arigatō', 'danke', 'aitah', 'aitäh',
                                             '\u3042\u308a\u304c\u3068\u3046'],
                      help=(r"Thank someone using a super cute kaomoji! ^_^"),
                      brief="Thank someone.")
    async def thank(self, ctx, *, target_user=None):
        """
        `target_user` is the target's nickname, username, or ID. The converting to the user object
        is handled by discord.ext.commands.MemberConverter(). That user is thanked by the bot, with
        a kaomoji emoticon in front. `target_user` can also be the argument "-list", in which case
        the bot returns all the kaomoji emoticons associated with this command
        """
        kaomoji = [r"♪(･ω･)ﾉ",
                   r"(\*ゝω・)ﾉ",
                   r"ﾟ･:,｡★＼(^-^ )♪ありがとう♪( ^-^)/★,｡･:･ﾟ",
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
        # Define the list of kaomoji emoticons the bot will be using. Because of discord formatting
        # most special characters are escaped with a \, however to stop python formatting,
        # r-strings are used (r"").

        selected_kaomoji = random.choice(kaomoji)
        # Choose a random kaomoji that we'll use for this use of the command.

        if target_user is None:  # If the user does not supply a target user.
            await ctx.send(f"{selected_kaomoji} Thank you!")  #  Return a generic response.
        elif target_user == "-list":  # If the user uses the argument "-list".
            await ctx.send("\n".join(kaomoji))  # Join together all the kaomoji and send them.
        else:  # If the target user is actually given.
            try:
                target_user = await commands.MemberConverter().convert(ctx, target_user)
                # Try to convert the string to an user using discord.ext.commands.MemberConverter().
                # Then, run through some special cases.
                if target_user == ctx.bot.user:  # If the user's target is the bot itself.
                    await ctx.send(f"You're welcome, {ctx.author.name}! \\\u2764")
                    # Return a "You're welcome" message.
                    # "u2764" is the black heart unicode character, a "\" is needed to turn it
                    # into the actual character, however we also need to escape it on discord's
                    # side so it stays as an emoticon and not as an emoji, so an additional "\\"
                    # is needed.
                elif target_user == ctx.author:  # If the user attempts to thank themself.
                    await ctx.send(f"Why would I need to thank you, {ctx.author.name}?")
                    # sass
                else:  # If no special cases were found.
                    await ctx.send(f"{selected_kaomoji} Thank you, {target_user.name}!")
                    # Simply thank the target user.
            except commands.BadArgument:  # If there wasn't an user with that name.
                await ctx.send(f"{selected_kaomoji} Thank you, {target_user}!")
                # Fall back to just using the inputted string with no conversion.

    @commands.command(name='developer', aliases=['dev'],
                      help="Try it!",
                      brief="Display the best developer of 2017")
    async def developer(self, ctx):
        "Takes no arguments. Simply writes a message to the channel whence it was invoked"
        await ctx.send("zetty best developer of 2017 and 2018 <:developer:352469145989939200>")

    @commands.command(name='shipname', aliases=['name'],
                      help="Create the shipname of two people.")
    async def shipname(self, ctx, name1, name2):
        "Uses pecan's shipname module to create a shipname"
        names_shipname = improved_shipname.shipname(name1, name2)
        # Request a shipname from pecan's shipname module™ using names from arguments.
        # I don't know how it works.
        await ctx.send(f"{ctx.author.name}, I shall call it \"**{names_shipname}**\"!")

    @commands.command(name='shipcount', aliases=['count'],
                      help="Get amount of ships created between people")
    async def shipcount(self, ctx, *ships_in):
        # Get the file where all shipping information is stored.
        shipfile = "important/shiplog.pickle"
        # The list 'ships' contains the user(s) we want to get information about.
        ships = []
        for i in ships_in:
            if i == "-top":
                continue
            ships.append(await commands.MemberConverter().convert(ctx, i))
        ships = remove_duplicates(ships)
        # Format the IDs into a format: 'id1:id2:id3...'
        # this format is needed as this is how ship information is stored in 'shiplog.txt'.
        ships_format = ':'.join([str(x.id) for x in ships])

        try:
            with open(shipfile, "rb") as opened_file:
                # Open the shipfile and unpickle it.
                # The returning format is a dictionary
                # {'id1:id2:id3...': count}
                lines = pickle.load(opened_file)
        except FileNotFoundError:
            await ctx.send(f"I couldn't find the shipping file ({shipfile})")
            return
        except pickle.UnpicklingError:
            await ctx.send("Shipping data file is corrupt, cannot fetch data.")
            return

        if not ships:
            # If the user gives no arguments with the command,
            # assume the user wants information about themselves.
            ships = [ctx.author]
        print(lines)
        if len(ships) == 1:
            # If the user gives only one user as an argument (or none, as shown above),
            # find all the ships that user is contained in.
            return_message = ""
            if "-top" in ships_in:
                mentions = list(reversed(sorted(lines, key=lambda a: a[1])))[:10]
            else:
                mentions = search(lines, ships[0].id)
                mentions = reversed(sorted(mentions, key=lambda a: a[1]))
            print(mentions)
            for k, j in mentions:
                usern = []
                # take the 'id1:id2:id3...' format mentioned before and split it
                # into the IDs it is composed from.
                for i in k.split(":"):
                    try:
                        # Convert the lower level ID into an username that people
                        # can actually understand. The function get_user() only works if the target
                        # shares a server with the bot. Returns None if user is not found.
                        found_user = ctx.bot.get_user(int(i))
                        if found_user is None:
                            # If the search fails, assume the user doesn't share a server with the
                            # bot, and use another function instead.
                            # NOTE: The function get_user_info() works regardless of the target
                            # sharing servers with the bot, however, it is terribly slow.
                            found_user = await ctx.bot.get_user_info(i)
                        usern.append(found_user.name)
                    except discord.NotFound:
                        # If somehow the target user does not exist on Discord, fall back to just
                        # showing the ID
                        usern.append(i)
                times_message = "time" if j == 1 else "times"
                return_message += f"{' x '.join(usern)}: shipped {j} {times_message}\n"

            await ctx.send(f"```\n{return_message}\n```")
            return

        else:
            occ = lines.get(ships_format, 0)
            # The user gives multple users as arguments, find how many times those specific users
            # have been shipped before.

            times_message = "time" if j == 1 else "times"

            await ctx.send(f"{ctx.author}, they have been shipped {occ} {times_message} before")

    @commands.command(name='ship', aliases=['otp'],
                      help="Ship someone with someone else.",
                      brief="Ship someone with someone else. uwu")
    async def ship(self, ctx, *ships: discord.Member):
        shipfile = "important/shiplog.pickle"
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
        else:
            await ctx.send(f"{error} {error.args[0].lower()}")

    @commands.command(name='hug', aliases=['\U0001f917'],
                      help="Give someone a hug!")
    async def hug(self, ctx, *target_users):
        target_users = list(target_users)
        con = lite.connect("important/userdata.db")
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
                                   ctx.author.name, recievers, hugs))
                else:
                    combine = ("I hug you back, {}! "
                               "\U0001f917 (You've given {} hug(s) in total)".format(
                                   ctx.author.name, hugs))
            elif targets:
                recievers = " and ".join(
                    [x.name if not isinstance(x, str) else x for x in targets])
                combine = "{} gave {} a hug! (You've given {} hug(s) in total)".format(
                    ctx.author.name, recievers, hugs)
            else:
                combine = "{} gave {} a hug! (You've given {} hug(s) in total)".format(
                    ctx.author.name, target_users, hugs)
        await ctx.send(combine)

    @commands.command(name='pecan', aliases=['p'],
                      help="Random quote from pecan.")
    async def pecan(self, ctx, *, input_text=None):
        with open("pecan.txt", "r") as opened_file:
            data = opened_file.read().splitlines()
            if input_text is None:
                num = random.choice(range(len(data)))
                quote = data[num]
            else:
                try:
                    num = int(input_text)
                    num = num - 1
                    quote = data[num]
                except IndexError:
                    await ctx.send("baka!")
                    return
                except ValueError:
                    found_entries = []
                    for y, i in enumerate(data):
                        if input_text in i:
                            found_entries.append((y, i))
                    if not found_entries:
                        await ctx.send(f"{ctx.author.name}, nothing contains `{input_text}`")
                        return
                    q = random.choice(found_entries)
                    await ctx.send(f"`{input_text}` (total {len(found_entries)}) - {q[0]}: `{q[1]}`")
                    return
            await ctx.send(f"{num + 1}: `{quote}`")

    @pecan.error
    async def pecan_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.name}, integer please")

    @commands.command(name='fortune', aliases=['f'],
                      help="Unix fortune.")
    async def fortune(self, ctx):
        await ctx.send("```\n" + subprocess.check_output("fortune").decode("utf-8") + "\n```")

def setup(bot):
    bot.add_cog(FunCog(bot))
