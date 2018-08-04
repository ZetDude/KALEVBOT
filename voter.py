import asyncio  # needed for discord messaging
import datetime
import math

import discord  # Discord API
from lib import obot

import voter_locale as vl

client = discord.Client()
lastCheck = 999
lastCheckDay = 0

REFRESH_TIME = 55
VOTING_CHANNEL = 374313083054587905
AYE_REACTION = "✅"
NAY_REACTION = "❎"
MAYBE_REACTION = "🤔"
APPROVED_REACTION = "f1:374638758831718400"
APPROVED_REACTION_LONG = "<:" + APPROVED_REACTION + ">"
VOTING_PERIOD = 86400  # in seconds
PARTICIPANT_ROLE = "nomlang"

REMIND_TIME = [120, 60, 30, 10, 0]
NOTIF_TIME = [30, 0]
REMINDER_CHANNEL = 373593670508609537
CALL_TIMES = [None,    # monday
              None,    # tuesday
              None,    # wednesday
              None,    # thursday
              None,    # friday
              (18, 0),  # saturday
              (20, 0),  # sunday
              ]
PIDGIN_ROLE = "<@&374318541681197058>"

print("Launching bot, this might take a few seconds")


def time_in_all_locales(remaining):
    print(remaining)
    minutes = remaining % 60
    hours = remaining // 60
    print(minutes)
    print(hours)
    locales = vl.LOCALES
    backup_right_now = l("TIME_NOW")[1]
    connecting_and = l("TIME_AND")[1]
    if minutes == 1:
        minutes_in_locales = l("TIME_MINUTE_SG", minutes)[1]
    else:
        minutes_in_locales = l("TIME_MINUTE_PL", minutes)[1]
    if hours == 1:
        hours_in_locales = l("TIME_HOUR_SG", hours)[1]
    else:
        hours_in_locales = l("TIME_HOUR_PL", hours)[1]
    final_results = []
    for i, y in enumerate(locales):
        if minutes == 0 and hours == 0:
            final_results.append(backup_right_now[i])
        elif minutes == 0:
            final_results.append(hours_in_locales[i])
        elif hours == 0:
            final_results.append(minutes_in_locales[i])
        else:
            final_results.append((f"{hours_in_locales[i]} {connecting_and[i]} "
                                  f"{minutes_in_locales[i]}"))
    print(final_results)
    return ("\n".join(final_results), final_results)


def l(text, *args):
    locales = vl.LOCALES
    print([i[text] for i in locales])
    print(args)
    if not args:
        in_all_locales = [i[text] for i in locales]
    else:
        in_all_locales = [i[text].format(*args) for i in locales]
    return ("\n".join(in_all_locales), in_all_locales)


def l_join(text, locale_list):
    locales = vl.LOCALES
    final_results = []
    for y, i in enumerate(locales):
        final_results.append(i[text].format(locale_list[y]))
    return ("\n".join(final_results), final_results)


@asyncio.coroutine
def periodic():
    while True:
        #yield from check_old_vote_messages()
        #see you space cowboy
        yield from call_time_detect() # pylint:disable=E1133
        yield from asyncio.sleep(REFRESH_TIME)


async def fetch_perfect_vote_amount(message):
    """Caluclate the amount of votes for a vote, factoring in everything"""
    reactions = message.reactions
    participantRole = discord.utils.get(
        message.guild.roles, name=PARTICIPANT_ROLE)
    aye = 0
    nay = 0
    maybe = 0
    for r in reactions:
        if str(r) == AYE_REACTION:
            async for u in r.users():
                if u == message.author:
                    continue
                if participantRole not in u.roles:
                    continue
                if u == client.user:
                    continue
                aye += 1
        elif str(r) == NAY_REACTION:
            async for u in r.users():
                if u == message.author:
                    continue
                if participantRole not in u.roles:
                    continue
                if u == client.user:
                    continue
                nay += 1
        elif str(r) == MAYBE_REACTION:
            async for u in r.users():
                if u == message.author:
                    continue
                if participantRole not in u.roles:
                    continue
                if u == client.user:
                    continue
                maybe += 1
    return (aye, nay, maybe)


async def check_old_vote_messages():
    """Checks old votes to see if they are expired, and acts accordingly"""
    targetChannel = client.get_channel(VOTING_CHANNEL)
    currentTime = datetime.datetime.utcnow()
    participants = len(discord.utils.get(
        targetChannel.guild.roles, name=PARTICIPANT_ROLE).members)
    async for message in targetChannel.history():
        if message.content.upper().startswith("VOTE"):
            reactionsStr = [str(x) for x in message.reactions]
            if APPROVED_REACTION_LONG in reactionsStr:
                continue
            age = currentTime - message.created_at
            aye, nay, maybe = await fetch_perfect_vote_amount(message)
            votes = aye - nay
            data = message.content
            info = (data[:75] + '...') if len(data) > 75 else data
            if age.total_seconds() > VOTING_PERIOD:

                await message.add_reaction(APPROVED_REACTION)
                # possibly remove the -1 part
                minimum = math.ceil((participants - 1) / 2)
                if votes >= minimum:
                    await message.channel.send("""A vote has **__expired__** and has **__passed__** {}:
{}
gained {} votes ({} aye, {} nay, {} counter), {} being the minimum needed""".format(AYE_REACTION, info, votes, aye, nay, maybe, minimum))
                else:
                    await message.channel.send("""A vote has **__expired__** and has **__failed__** {}:
{}
gained {} votes ({} aye, {} nay, {} counter), {} being the minimum needed""".format(NAY_REACTION, info, votes, aye, nay, maybe, minimum))
            elif (votes / (participants - 1) * 100) >= 75:
                await message.add_reaction(APPROVED_REACTION)
                await message.channel.send("""A vote has **__passed__** due to **__overwhelming support__** {}:
{}
gained {} votes ({} aye, {} nay, {} counter)""".format(AYE_REACTION, info, votes, aye, nay, maybe))


def cal_delta_to(hours, minutes):
    global lastCheck
    now = datetime.datetime.utcnow()
    target = datetime.datetime(*now.timetuple()[0:3], hour=hours, minute=minutes)
    if now > target:
        diff = now - target
        return -(diff.seconds // 60)
    else:
        diff = target - now
        return diff.seconds // 60


async def call_time_detect():
    global lastCheck
    global lastCheckDay
    remaining = get_minutes_remaining()
    if remaining == "mada":
        return
    if lastCheckDay != datetime.datetime.today().weekday():
        lastCheckDay = datetime.datetime.today().weekday()
        lastCheck = 999
    for i in REMIND_TIME:
        if remaining <= i and lastCheck > i and remaining > -1:
            lastCheck = remaining
            starts_in = time_in_all_locales(remaining)[1]

            if remaining == 0:
                await client.get_channel(REMINDER_CHANNEL).send(l("REMINDER_NOW")[0])
            else:
                await client.get_channel(REMINDER_CHANNEL).send(l_join("REMINDER_REMIND", starts_in)[0])

            if remaining in NOTIF_TIME:
                await client.get_channel(REMINDER_CHANNEL).send(f"Boop! {PIDGIN_ROLE}")
            break


def get_minutes_remaining():
    d = datetime.datetime.utcnow().date()
    today_call = CALL_TIMES[d.weekday()]
    if today_call is None:
        return "mada"
    else:
        return cal_delta_to(*(today_call))


@client.event
async def on_ready():
    """When the bot is initialized"""
    print("")
    print("Success! The bot is online!")
    print("My name is " + client.user.name)
    print("My ID is " + str(client.user.id))
    print("I am present in " + str(len(client.guilds)) + " guilds.")
    asyncio.Task(periodic())


@client.event
async def on_message(message):
    """
    if message.channel.id == VOTING_CHANNEL:
        if message.content.upper().startswith("VOTE"):
            await message.add_reaction(AYE_REACTION)
            await message.add_reaction(NAY_REACTION)
            await message.add_reaction(MAYBE_REACTION)
    """
    if message.content.startswith("k!call"):
        remaining = get_minutes_remaining()
        if remaining == "mada":
            await message.channel.send(l("CHECK_NONE")[0])
            return
        remaining_o = remaining
        remaining = abs(remaining)
        starts_in = time_in_all_locales(remaining)[1]
        if remaining_o == 0:
            await message.channel.send(l("REMINDER_NOW")[0])
        elif remaining_o < 0:
            await message.channel.send(l_join("CHECK_PASSED", starts_in)[0])
        else:
            await message.channel.send(l_join("REMINDER_REMIND", starts_in)[0])

client.run(obot.BOT_TOKEN)  # bot
