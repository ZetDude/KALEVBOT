"""Fun commands that don't do anything really productive

night, thank, shipname, shipcount, ship, hug, pecan, fortune"""

# -*- coding: utf-8 -*-

import pickle
import random
import sqlite3 as lite
import subprocess

import discord
from discord.ext import commands
from lib import shipname_module as improved_shipname, customconverter as cconv, obot


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
        """Wish a good night to `target_user`, with a kaomoji emoticon in front.

        `target_user` is anything pertaining to the target user or member that
        lib.customconverter.HybridConverter can detect.
        `target_user` defaults to None and can be left blank.
        `target_user` can also be the argument "-list", in which case the bot returns all the
        kaomoji emoticons associated with this command.
        """

        # Define the list of kaomoji emoticons the bot will be using. Because of discord formatting
        # special characters are escaped with a \.
        kaomoji = [r"お(^o^)や(^O^)す(^｡^)みぃ(^-^)ﾉﾞ",
                   r" .｡.:\*･ﾟ☆Goodヾ(\*´Д｀(\*ﾟωﾟ\* )Night☆.｡.:\*･ﾟ",
                   r" – =͟͟͞ (¦3[▓▓])",
                   r" ｡･:\*:･ﾟ★,｡･=^∇^\*=,｡･:\*:･ﾟ☆",
                   r"☆~\*.(UωU\*)おやすみぃ…\*~☆",
                   r"|・ω・`）おやすみぃ♪", ]

        selected_kaomoji = random.choice(kaomoji)

        if target_user is None:  # If the user does not supply a target user...
            await ctx.send(f"{selected_kaomoji} Good night!") #  Return a generic response.
        elif target_user == "-list":  # -list flag...
            await ctx.send("\n".join(kaomoji))  # Join together all the kaomoji and send them.
        else:  # If the target user is actually given.
            try:
                target_user = await cconv.HybridConverter().convert(ctx, target_user)
                await ctx.send(f"{selected_kaomoji} Good night, {target_user.name}!")
            except commands.BadArgument:  # HybridConverter fails...
                # Fall back to just using the inputted string with no conversion.
                await ctx.send(f"{selected_kaomoji} Good night, {target_user}!")

    @commands.command(name='thank', aliases=['thanks', 'arigato', 'arigatou', 'arigatoo',
                                             'merci', 'arigatō', 'danke', 'aitah', 'aitäh',
                                             '\u3042\u308a\u304c\u3068\u3046'],
                      help=(r"Thank someone using a super cute kaomoji! ^_^"),
                      brief="Thank someone.")
    async def thank(self, ctx, *, target_user=None):
        """Thank `target_user`, with a kaomoji emoticon in front.

        `target_user` is anything pertaining to the target user or member that
        lib.customconverter.HybridConverter can detect.
        `target_user` defaults to None and can be left blank.
        `target_user` can also be the argument "-list", in which case the bot returns all the
        kaomoji emoticons associated with this command.
        """

        # The list of kaomoji emoticons the bot will be using. Because of discord formatting special
        # characters are escaped with a \.
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

        selected_kaomoji = random.choice(kaomoji)

        if target_user is None:  # If the user does not supply a target user.
            await ctx.send(f"{selected_kaomoji} Thank you!")  # Return a generic response.
        elif target_user == "-list":  # -list flag
            await ctx.send("\n".join(kaomoji))  # Join together all the kaomoji and send them.
        else:  # If the target user is actually given.
            try:
                target_user = await cconv.HybridConverter().convert(ctx, target_user)
                if target_user == ctx.bot.user:  # If the user's target is the bot itself...
                    # "u2764" is the black heart unicode character
                    await ctx.send(f"You're welcome, {ctx.author.name}! \\\u2764")
                elif target_user == ctx.author:  # If the user attempts to thank themself... sass.
                    await ctx.send(f"Why would I need to thank you, {ctx.author.name}?")
                else:  # If no special cases were found...
                    await ctx.send(f"{selected_kaomoji} Thank you, {target_user.name}!")
            except commands.BadArgument:  # HybridConverter fails...
                # Fall back to just using the inputted string with no conversion
                await ctx.send(f"{selected_kaomoji} Thank you, {target_user}!")

    @commands.command(name='shipname', aliases=['name'],
                      help="Create the shipname of two people.")
    async def shipname(self, ctx, name1, name2):
        """Uses pecan's shipname module to create the shipname of two names.

        `name1` is the first name.
        `name2` is the first name.
        """
        # Request a shipname from pecan's shipname module™ using names from arguments.
        names_shipname = improved_shipname.shipname(name1, name2)  # I don't know how it works.
        await ctx.send(f"{ctx.author.name}, I shall call it \"**{names_shipname}**\"!")

    @commands.command(name='shipcount', aliases=['count'],
                      help="Get amount of ships created between people",
                      usage="[users...] OR -top")
    async def shipcount(self, ctx, *ships_in):
        """Show all the people someone has been shipped with when given one person, or the amount
        of ships between certain people when given multiple.

        `ships_in` is the people/person to get info of.
        `ships_in` can also be the argument "-top", in which case only the top 10 most shipped pairs
        will be shown."""
        shipfile = obot.SHIPFILE  # File where all shipping information is stored.
        ships = []  # This list will contain the user(s) we want to get information about.
        for i in ships_in:  # Convert all the given member to actual users.
            if i == "-top":  # skip the -top flag.
                continue
            ships.append(await cconv.HybridConverter().convert(ctx, i))
        ships = remove_duplicates(ships)
        # Format the IDs into a format: 'id1:id2:id3...'.
        # This format is needed as this is how ship information is stored in the shipfile.
        ships_format = ':'.join([str(x.id) for x in ships])

        try:
            # Open the shipfile and unpickle it. The returning format is a dictionary.
            # -> {'id1:id2:id3...': count}
            with open(shipfile, "rb") as opened_file:
                lines = pickle.load(opened_file)
        except FileNotFoundError:
            await ctx.send(f"I couldn't find the shipping file ({shipfile})")
            return
        except pickle.UnpicklingError:
            await ctx.send("Shipping data file is corrupt, cannot fetch data.")
            return

        if not ships:  # No arguments... default to author.
            ships = [ctx.author]
        if len(ships) == 1:  # Find all the ships that user is contained in.
            return_message = ""
            if "-top" in ships_in:  # -top flag is given...
                # The data dict is turned into a list, and is sorted by the count, then reversed
                # so that the biggest are in the beginning, and then only the first 10 are fetched.
                mentions = list(reversed(sorted(list(lines.items()), key=lambda a: a[1])))[:10]
            else:  # no flag is given...
                # All the lines that contain the target are fetched
                mentions = search(lines, ships[0].id)
                mentions = reversed(sorted(mentions, key=lambda a: a[1]))
            for k, j in mentions:  # Iterate through all fetched lines.
                usern = []
                # take the 'id1:id2:id3...' format and split it into the IDs it is composed from.
                for i in k.split(":"):
                    try:
                        # Convert the ID which is stored into an user.
                        found_user = ctx.bot.get_user(int(i))
                        if found_user is None: # No server shared with target user.
                            # NOTE: The function get_user_info() works regardless of the target
                            # sharing servers with the bot, however, it is terribly slow.
                            found_user = await ctx.bot.get_user_info(i)
                        usern.append(found_user.name)
                    except discord.NotFound:  # User doesn't exist on discord...?
                        usern.append(i)  # Fall back to just showing the ID
                times_message = "time" if j == 1 else "times"
                return_message += f"{' x '.join(usern)}: shipped {j} {times_message}\n"
                # example -> "User1 x User2: shipped 3 times"
            if not return_message: # no results found...
                return_message = (f"{ships[0].name}, you haven't been shipped with anybody yet, "
                                  f"but I still love you!")
            await ctx.send(f"```\n{return_message}\n```")
            return

        else:  # The user gives multple users as arguments...
            # Find how many times those specific users have been shipped before.
            occ = lines.get(ships_format, 0)
            times_message = "time" if j == 1 else "times"

            await ctx.send(f"{ctx.author}, they have been shipped {occ} {times_message} before")

    @commands.command(name='ship', aliases=['otp'],
                      help="Ship someone with someone else.",
                      brief="Ship someone with someone else. uwu")
    async def ship(self, ctx, *ships: cconv.HybridConverter):
        shipfile = obot.SHIPFILE  # File where all the shipping information is stored.
        if ctx.message.author in ships:  # Uses attempts to ship themself
            await ctx.send((f"{ctx.message.author.name}, "
                            "I don't think you can ship yourself with someone"))
            return
        ships = remove_duplicates(ships)
        if len(ships) < 2:
            await ctx.send(f"{ctx.message.author.name}, mention at least two people in the message")
            return
        ships_names = [x.name for x in ships]
        # Format the IDs into a format: 'id1:id2:id3...'.
        # This format is needed as this is how ship information is stored in the shipfile.
        # The list is sorted by ID for consistency between runs.
        ships_format = ":".join(sorted([str(x.id) for x in ships], key=int))
        try:
            with open(shipfile, "rb") as opened_file:
                # Open the shipfile and unpickle it. The returning format is a dictionary.
                # -> {'id1:id2:id3...': count}
                lines = pickle.loads(opened_file.read())
        except FileNotFoundError:
            lines = {}
            with open(shipfile, 'w'):
                await ctx.send("Created new ship file")
        except pickle.UnpicklingError:
            await ctx.send("Ship file is corrupt, cannot fetch data.")
            return

        occ = lines.get(ships_format, 0)  # Times the target users have already been shipped.
        times_message = "time" + ("" if occ == 1 else "s")
        lines[ships_format] = occ + 1  # Increase count by one

        with open(shipfile, 'wb') as opened_file:  # Write the new data
            pickle.dump(lines, opened_file)

        shipname = ""

        if len(ships) == 2:  # If there are two names, we can make a shipname
            # Request a shipname from pecan's shipname module™
            final = improved_shipname.shipname(*ships_names)
            shipname = "I shall call it \"**" + final + "**\""

        await ctx.send((f"{ctx.message.author.name} totally ships {' and '.join(ships_names)}"
                        f"\nThey have been shipped {occ} {times_message} before"
                        f"\n{shipname}"))

    @commands.command(name='hug', aliases=['\U0001f917'],
                      help="Give someone a hug!")
    async def hug(self, ctx, *target_users):
        """Hug target user, and count how many times you have hugged people in total

        TODO: Make hugs server-based

        `target_users` are the users to hug (or just 1 user).
        `target_users` can also be the argument "-top <num>", in which case the top <num> people
        with the highest amount of hugs given will be returned.
        """
        target_users = list(target_users)
        con = lite.connect("important/data.db")  # Database where hug data is stored
        if target_users[0] == "-top":  # If the first argument given is the flag -top...
            try:  # The second argument is how many people to fetch.
                fetch_amount = int(target_users[1])
                if fetch_amount < 0:
                    await ctx.send(f"That's less than zero, {ctx.author}.")
            except ValueError:
                await ctx.send(f"That's not an integer, {ctx.author}.")
                return
            except IndexError:  # If an amount isn't given, default to 5
                fetch_amount = 5
            with con:
                try:
                    # Order all entries by amount, descending, then get the first `fetch_amount`
                    cur = con.cursor()
                    cur.execute("SELECT * FROM Hug ORDER BY Hugs DESC")
                    rows = cur.fetchall()[:fetch_amount]
                    combine = f"```\nTOP {fetch_amount} HUGGERS:\n---------\n"

                    for row in rows:
                        # Convert the ID to an user.
                        target_user = ctx.bot.get_user(row[0])
                        if target_user is None:  # No server shared with target.
                            try:
                                # NOTE: The function get_user_info() works regardless of the target
                                # sharing servers with the bot, however, it is terribly slow.
                                target_user = await ctx.bot.get_user_info(row[0])
                            except discord.NotFound:  # User doesn't exist on Discord.
                                target_user = None  # Give up and default to None.
                        combine += target_user.name if not None else row[0]
                        combine += " - " + str(row[1]) + "\n"
                    combine += "\n```"
                except lite.OperationalError as err:  # sql error...
                    if str(err) == "no such table: Hug":  # No table exists...
                        # Create a new one and inform the user
                        cur.execute("CREATE TABLE Hug(id INT NOT NULL UNIQUE, Hugs INT);")
                        await ctx.send("No hug data was recorded, created file now.")
        else:  # If actual users are given.
            targets = []
            for i in target_users:  # Go through all the targets...
                try:  # and try to convert them using HybridConverter...
                    converted_member = await cconv.HybridConverter().convert(ctx, i)
                except commands.BadArgument:  # but if that fails...
                    converted_member = "*" + i + "*"  # default to the string that the user gave.
                targets.append(converted_member)
            targets = remove_duplicates(targets)

            # If the list contains just the author or nobody
            if [ctx.author] == targets or not targets:
                await ctx.send(f"Who are you going to hug, {ctx.author.name}? Yourself?")
                return
            if ctx.author in targets:  # Remove the user from the list of targets.
                targets.remove(ctx.author)
            with con:
                try:  # Get the data of the author from the database
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
                times_message = "hug" + ("" if hugs == 1 else "s")
                # Create a second list which is just a copy of the targets
                mentions_without_bot = list(targets)
                for user in mentions_without_bot[::1]:
                    # Need to iterate backwards to not jump over anything when removing.
                    if isinstance(user, str):  # Get rid of everything that isn't an user.
                        mentions_without_bot.remove(user)
                    elif user.bot:  # Get rid of bots.
                        mentions_without_bot.remove(user)
                hugs += len(mentions_without_bot)  # Increase the hug tally of the author.
                # Update database.
                cur.execute("INSERT OR IGNORE INTO Hug VALUES(?, ?)", (ctx.author.id, hugs))
                cur.execute("UPDATE Hug SET Hugs=? WHERE id=?", (hugs, ctx.author.id))

            if ctx.bot.user.id in [x.id for x in targets if not isinstance(x, str)]:
                # If the bot itself is in the targets list.
                if len(targets) > 1:  # If other users are hugged alongside it.
                    # Join all other targets.
                    recievers_without_self = list(targets)
                    recievers_without_self.remove(ctx.bot.user)
                    recievers = " and ".join([x.name if not isinstance(
                        x, str) else x for x in recievers_without_self])

                    combine = (f"{ctx.author.name} gave {recievers} a hug, and I hug you back! "
                               f"\U0001f917 (+{len(mentions_without_bot)}; {hugs} "
                               f"{times_message} in total)")
                else:  # Only the bot is hugged.
                    combine = (f"I hug you back, {ctx.author.name}! "
                               f"\U0001f917 (+{len(mentions_without_bot)}; {hugs} "
                               f"{times_message} in total)")
            elif targets:
                # Join all targets.
                recievers = " and ".join(
                    [x.name if not isinstance(x, str) else x for x in targets])
                combine = (f"{ctx.author.name} gave {recievers} a hug! "
                           f"(+{len(mentions_without_bot)}; {hugs} "
                           f"{times_message} in total)")
            else:  # I don't know if this clause if ever executed but I'm too scared to remove it.
                combine = (f"{ctx.author.name}, you've hit the else clause on line 381 of fun.py, "
                           f"please report it to someone.")
        await ctx.send(combine)

    @commands.command(name='pecan', aliases=['p'],
                      help="Random quote from pecan.")
    async def pecan(self, ctx, *, input_text=None):
        """Get a random or certain line from the old IRC chat logs of pecan.

        `input_text` is the integer code of the line to fetch. Lookup is 1-indexed.
        `input_text` can also be left empty, in which case it defaults to None and just gives a
        random line.
        `input_text` can also be a string, in which case that string is searched for in the corpus,
        and a random line containing that string is returned.
        """
        try:
            with open(obot.PECAN_CORPUS, "r") as opened_file:
                data = opened_file.read().splitlines()  # Get all the lines of the file
                if input_text is None:  # No argument given
                    num = random.choice(range(len(data)))  # Get a random number.
                    quote = data[num]  # Get the quote corresponding to that number
                    await ctx.send(f"{num + 1}: `{quote}`")
                else:  # An argument is given
                    try:  # Test if is the number for a certain line
                        num = int(input_text)
                        num = num - 1
                        if num < 0:
                            await ctx.send("baka! number is negative!")
                            return
                        elif num == 0:
                            await ctx.send("baka! file is 1-indexed!")
                            return
                        quote = data[num]
                    except IndexError:
                        await ctx.send(f"baka! number is over {len(data)}!")
                        return
                    except ValueError:  # Not an int
                        # Find all entries where target string is included.
                        if input_text.startswith('"') and input_text.endswith('"'):
                            input_text = input_text[1:-1]
                        found_entries = []
                        for j, i in enumerate(data):
                            if input_text.lower() in i.lower():  # case-insensitive
                                found_entries.append((j, i))
                        if not found_entries:  # No entries found...
                            await ctx.send(f"{ctx.author.name}, nothing contains `{input_text}`")
                            return
                        response = random.choice(found_entries)  # pick a random valid entry.
                        await ctx.send((f"`{input_text}` (total {len(found_entries)}) - "
                                        f"{response[0]+1}: `{response[1]}`"))
                        # example -> `pecan` (total 40) - 1813: `I might meet the other pecan.`
        except FileNotFoundError:
            await ctx.send(f"{ctx.author.name}, no pecan corpus file is included or it is "
                           f"configured incorrectly. Download it at "
                           f"<http://97.107.129.215/pecan.txt>")

    @commands.command(name='fortune', aliases=['f'],
                      help="Unix fortune.")
    async def fortune(self, ctx):
        "Return a random unix fortune line."
        fortune_msg = subprocess.check_output("fortune").decode("utf-8")
        fortune_msg = fortune_msg[:1988] + "\u2026" if len(fortune_msg) > 1990 else fortune_msg
        await ctx.send("```\n" + fortune_msg + "\n```")

    @shipname.error
    async def shipname_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.name}, please use two names as arguments")

    @shipcount.error
    @ship.error
    async def ship_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.name}, {error.args[0]}")

def setup(bot):
    bot.add_cog(FunCog(bot))
