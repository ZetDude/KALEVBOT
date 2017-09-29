import discord #Discord API
import asyncio #needed for discord messaging
import datetime #time module
import sys
import random
import os
import maincore as dc
import basic as rpg
import obot
import errno
import psutil
import logging

os.system('CLS')

client = discord.Client()
ll = ""
newColorValue = 0

print("Launching bot, this might take a few seconds")

dirMake = ["actions", "important", "commands"]
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
    while True:
        yield from asyncio.sleep(7200)
        logChannel = client.get_channel(obot.logchannel)
        os.system('CLS')
        difference = dc.get_timer()
        diskspace = dc.get_free_space_mb("C:")
        diskspaceg = diskspace / 1024 / 1024 / 1024
        p_working = "It's working! I have been running for " + str(difference)
        p_space = "\nApproximate disk space left for bot: " + str(diskspaceg) + " GB (" + str(diskspace) + " bytes)" 
        p_server = "\nI am present in " + str(len(dc.cl.servers)) + " servers."
        p_count = "\nI have been used " + str(dc.get_count()) + " time(s)"
        dc.send(logChannel, p_working + p_space + p_server + p_count)

def is_me(m):
    zaAnswer = m.author == client.user
    return zaAnswer
    
@client.event
async def on_ready():
    
    dc.ready(client)
    rpg.ready()
    await client.edit_profile(username=obot.name)
    await client.change_presence(game=discord.Game(name=obot.game), status=discord.Status.online)

    if obot.logchannel is not None:
        task = asyncio.Task(periodic())
        loop = asyncio.get_event_loop()

@client .event
async def on_message(message):
    if message.server is None:
        fse = str(message.channel)
        if message.author != client:
            await client.send_message(client.get_channel(obot.logchannel), ">>" + message.author.name + " in " + fse + ">>\n||" + message.content + "||")
    else:
        fse = message.channel.name
    both = False
    if message.author.bot:
        both = False
    elif message.content.startswith(obot.botPrefix):
        both = True
        calc = dc.main(message)
        print("bot command detected\n-----------------")
    elif message.content.startswith(obot.rpgPrefix):
        both = True
        calc = rpg.run(message)
        print("rpg message detected\n-----------------")

    #await client.send_typing(message.channel)
    if both:
        await client.send_typing(message.channel)
        tolog1 = ">>" + message.author.name + " in " + fse + ">>"
        tolog2 = "||" + message.content + "||"
        tolog1 = ''.join(c for c in tolog1 if c <= '\uFFFF')
        tolog2 = ''.join(c for c in tolog2 if c <= '\uFFFF')
        print(tolog1)
        print(tolog2)

    if both:
        if calc != False and calc != None:
            rty, p = calc
            if rty == "m":
                if message.server is None:
                    fse = str(p[0])

                else:
                    fse = p[0].name
                print("Responding ||\n{}\n|| to channel >>{}>>".format(p[1], p[0]))
                await client.send_message(p[0], p[1])

            elif rty == "p":
                if message.server is None:
                    fse = str(p[0])

                else:
                    fse = p[0].name
                print("Responding ||\n{}\n|| to channel >>{}>>".format(p[1], p[0]))
                print("Responding ||\n{}\n|| to channel >>{}>>".format(p[3], p[2]))
                await client.send_message(p[0], p[1])
                await client.send_message(p[2], p[3])
                
            elif rty == "c":
                #print("----------------")
                await client.send_message(message.channel, "ITS ME GOODBYE! <https://youtu.be/y_hWeN249fs?t=25s>")
                dc.crash()
                sys.exit()
            elif rty == "d":
                print("Deleting " + str(p))
                totaldel = 0
                iterat = 1
                fianlc = 0
                deleted = []
                while p > totaldel:
                    try:
                        deleted = await client.purge_from(message.channel, limit=iterat, check=is_me)
                    except:
                        pass
                    iterat = iterat + 1 - len(deleted)
                    fianlc = fianlc + 1
                    if iterat > 52:
                        break
                    totaldel = totaldel + len(deleted)
                    deleted = []
                #print("----------------")
                await client.send_message(message.author, "Deleted " + str(totaldel) + " messages using " + str(fianlc) + " tries")

            elif rty == "r":
                await client.send_message(p[0], "Attempting to restart all systems")
                await client.change_presence(game=discord.Game(name="relaunch in progress"), status=discord.Status.dnd)
                restart_program()

    
client.run(obot.token) #bot
