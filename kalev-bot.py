"""This is the main instance that does all the hard work.
Please run this file to run the actual bot itself"""
# pylint: disable=no-member
import os
import sys
import errno
import logging
import asyncio #needed for discord messaging
import discord #Discord API
import maincore as dc
import basic as rpg
import obot
import psutil
import time

os.system('CLS')

client = discord.Client()
ll = ""
newColorValue = 0
driveClient = None


sp = os.path.dirname(os.path.realpath(sys.argv[0]))
print(sp)
print(sp + "/kalev-bot.py")
print("Now running main bot instance")

print("Launching bot, this might take a few seconds")
bStart = time.time()

dirMake = ["actions", "important", "commands", "important/lucky"]
for i in dirMake:
    try:
        os.makedirs(i)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """

    try:
        p = psutil.Process(os.getpid())
        for handler in p.get_open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)

@asyncio.coroutine
def periodic():
    """Every two hours, send a message to a channel, marking that the bot is still online"""
    while True:
        yield from asyncio.sleep(7200)
        logChannel = client.get_channel(obot.logchannel)
        os.system('CLS')
        difference = dc.get_timer()
        diskspace = dc.get_free_space_mb("C:")
        diskspaceg = diskspace / 1024 / 1024 / 1024
        p_working = "It's working! I have been running for " + str(difference)
        p_space = str("\nApproximate disk space left for bot: " +
                      str(diskspaceg) + " GB (" + str(diskspace) + " bytes)")
        p_guild = "\nI am present in " + str(len(dc.cl.guilds)) + " guilds."
        dc.send(logChannel, p_working + p_space + p_guild)

def is_me(m):
    """Return if given user is the bot. Needed for deleting the bot's messages"""
    zaAnswer = m.author == client.user
    return zaAnswer

@client.event
async def on_ready():
    bEnd = time.time()
    print("Launching of bot took {} seconds".format(bEnd - bStart))
    dc.ready(client, driveClient)
    rpg.ready()
    await client.user.edit(username=obot.name)
    s = await client.change_presence(game=discord.Game(type=obot.gametype, name=obot.game), status=discord.Status.online)
    print(s)
    if obot.logchannel is not None:
        asyncio.Task(periodic())
        #asyncio.get_event_loop()

@client.event
async def on_message(message):
    calc = None #backwards compatibility or something
    #TODO: ^ delete this bullshit
    if client.user in message.mentions:
        allEmoji = client.emojis
        pingEmoji = discord.utils.get(allEmoji, id=362665760260227073)
        await message.add_reaction(pingEmoji)
    if message.guild is None:
        fse = str(message.channel)
    else:
        fse = message.channel.name
    both = False
    if message.author.bot:
        return
    elif message.content.startswith(obot.botPrefix):
        both = True
        async with message.channel.typing():
            await dc.main(message)
        print("bot command detected\n-----------------")
    elif message.content.startswith(obot.rpgPrefix):
        both = True
        async with message.channel.typing():
            calc = rpg.run(message)
        print("rpg message detected\n-----------------")

    #await client.send_typing(message.channel)
    if both:
        tolog1 = ">>" + message.author.name + " in " + fse + ">>"
        tolog2 = "||" + message.content + "||"
        tolog1 = ''.join(c for c in tolog1 if c <= '\uFFFF')
        tolog2 = ''.join(c for c in tolog2 if c <= '\uFFFF')
        print(tolog1)
        print(tolog2)
        if calc != False and calc != None:
            actionMode, givenData = calc
            if actionMode == "d":
                print("Deleting " + str(givenData))
                await message.channel.purge(limit=givenData,
                                            check=is_me,
                                            bulk=False)
                await message.author.send("Deleted " + str(givenData) + " messages")

            elif actionMode == "r":
                await givenData[0].send("Attempting to restart all systems")
                await client.change_presence(game=discord.Game(name="relaunch in progress"),
                                             status=discord.Status.dnd)
                restart_program()


client.run(obot.token) #bot
