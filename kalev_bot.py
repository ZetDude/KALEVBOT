"""This is the main instance that does all the hard work.
Please run this file to run the actual bot itself"""
# pylint: disable=no-member
import os
import sys
import errno
import time
import discord #Discord API
import maincore as dc
import basic as rpg
from lib import obot
from lib import logger

client = discord.Client()

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
print(sp)
print(sp + "/kalev_bot.py")
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

@client.event
async def on_ready():
    bEnd = time.time()
    print("Launching of bot took {} seconds".format(bEnd - bStart))
    dc.ready(client)
    rpg.ready()
    await client.user.edit(username=obot.name)
    s = await client.change_presence(game=discord.Game(type=obot.gametype, name=obot.game),
                                     status=discord.Status.online)
    print(s)

@client.event
async def on_message(message):
    if client.user in message.mentions:
        allEmoji = client.emojis
        pingEmoji = discord.utils.get(allEmoji, id=362665760260227073)
        await message.add_reaction(pingEmoji)
    if message.guild is None:
        fse = str(message.channel)
    else:
        fse = message.channel.name + " in " + message.guild.name
    if message.author.bot:
        return
    if message.content.startswith(obot.bot_prefix):
        tolog1 = ">>" + message.author.name + " in " + fse + ">>"
        tolog2 = "||" + message.content + "||"
        logger.log(tolog1)
        logger.log(tolog2)

        await dc.main(message)
    #elif message.content.startswith(obot.game_prefix):
        #async with message.channel.typing():
            #rpg.run(message)
        #print("rpg message detected\n-----------------")

    #await client.send_typing(message.channel)

client.run(obot.token)
