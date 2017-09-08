import discord #Discord API
import asyncio #needed for discord messaging
import relaytimegeneratorbot as rbot #my own thing that calculates deadlines
import datetime #time module
import time #another time module
import sys
import pytz
import random
import os
import maincore as dc
import string
import basic as rpg
import colorsys
import obot
import errno
import psutil
import logging

try:
    import delcauto
except:
    print("failed importing delcauto, dont worry about this")

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

r = 255
g = 0
b = 0
state = 0

try:
    with open('discordCount.txt', 'r') as f:
        count = int(f.readlines(0)[0])
        count += 1
except:
    print("discordCount.txt didn't exist, creating")
    count = 1

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
        logChannel = client.get_channel("333421973462056961")
        difference = dc.get_timer()
        diskspace = dc.get_free_space_mb("C:")
        diskspaceg = diskspace / 1024 / 1024 / 1024
        p_working = "It's working! I have been running for " + str(difference)
        p_space = "\nApproximate disk space left for bot: " + str(diskspaceg) + " GB (" + str(diskspace) + " bytes)" 
        p_server = "\nI am present in " + str(len(dc.cl.servers)) + " servers."
        p_count = "\nI have been used " + str(dc.get_count()) + " time(s)"
        yield from client.send_message(logChannel, p_working + p_space + p_server + p_count)
        

def stop():
    task.cancel()

def is_me(m):
    zaAnswer = m.author == client.user
    return zaAnswer
    
@client.event
async def on_ready():
    dc.ready(client)
    rpg.ready()
    await client.change_presence(game=discord.Game(name=obot.game))
    await client.edit_profile(username=obot.name)
    task = asyncio.Task(periodic())
    loop = asyncio.get_event_loop()

@client.event
async def on_message(message):
    if message.server == None:
        fse = str(message.channel)
        if message.author != client:
            await client.send_message(client.get_channel("333421973462056961"), ">>" + message.author.name + " in " + fse + ">>\n||" + message.content + "||")
    else:
        fse = message.channel.name
    tolog1 = ">>" + message.author.name + " in " + fse + ">>"
    tolog2 = "||" + message.content + "||"
    tolog3 = ""
    tolog4 = ""
    tolog1 = ''.join(c for c in tolog1 if c <= '\uFFFF')
    tolog2 = ''.join(c for c in tolog2 if c <= '\uFFFF')
    both = False
    if message.author.bot:
        both = False
    elif message.content.startswith(obot.botPrefix):
        wascommand = 1
        both = True
        calc = dc.main(message)
        print("bot command detected")
    elif message.content.startswith(obot.rpgPrefix):
        wascommand = 1
        both = True
        calc = rpg.run(message)
        print("rpg message detected")

    #await client.send_typing(message.channel)
    if both:
        print(tolog1)
        print(tolog2)
        await client.send_typing(message.channel)

    if message.server != None:
        if message.server.id == "333421004942475266":

            colorRole = discord.utils.get(message.server.roles, name='party')
            if colorRole in message.author.roles: 
                global r
                global g
                global b
                global state
                ##newColorValue = random.randint(0, 16777215)
                sV = 32
                if state == 0:
                    g += sV
                    if g > 255 or g < 0:
                        state = 1

                if state == 1:
                    r -= sV
                    if r > 255 or r < 0:
                        state = 2
                
                if state == 2:
                    b += sV
                    if b > 255 or b < 0:
                        state = 3
                
                if state == 3:
                    g -= sV
                    if g > 255 or g < 0:
                        state = 4
                
                if state == 4:
                    r += sV
                    if r > 255 or r < 0:
                        state = 5
                
                if state == 5:
                    b -= sV
                    if b > 255 or b < 0:
                        state = 0

                if g < 0:
                    g = 0
                if r < 0:
                    r = 0
                if b < 0:
                    b = 0

                if g > 255:
                    g = 255
                if r > 255:
                    r = 255
                if b > 255:
                    b = 255

                length = random.randint(1, 32)
                #newName = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
                #newName = ''.join("a" for i in range(length))
    ##            newName = "Chaos"
    ##            try:
    ##                await client.change_nickname(message.author, newName)
    ##            except:
    ##                print("ded")
                newColorValue = (r<<16) + (g<<8) + b
                newColor = discord.Colour(newColorValue)
                await client.edit_role(message.server, colorRole, color=newColor)
    
    if both:
        if calc != False and calc != None:
            rty, p = calc
            if rty == "m":
                if message.server == None:
                    fse = str(p[0])

                else:
                    fse = p[0].name
                print("Responding ||{}|| to channel >>{}>>".format(p[1], p[0]))
                await client.send_message(p[0], p[1])

            elif rty == "p":
                if message.server == None:
                    fse = str(p[0])

                else:
                    fse = p[0].name
                print("Responding ||{}|| to channel >>{}>>".format(p[1], p[0]))
                print("Responding ||{}|| to channel >>{}>>".format(p[3], p[2]))
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
                        a = True
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
                restart_program()
        try:
            with open('discordCount.txt', 'r') as f:
                count = int(f.readlines(0)[0])
            count += 1
        except:
            print("discordCount.txt didn't exist, creating")
            count = 1
        with open('discordCount.txt', 'w') as f:
            f.write(str(count))
        print("Bot has been used {} time(s)".format(count))

allowedChannel = obot.allowedChannel
allowedServer = obot.allowedServer
delMsg = obot.delMsg
cooldown = obot.cooldown
@client.event
async def on_message_delete(message):
    if message.author != client:
        time1 = message.timestamp
        time2 = datetime.datetime.utcnow()
        c = time2 - time1
        dis = divmod(c.days * 86400 + c.seconds, 60)
        part1, part2, part3 = delcauto.run(message, client, dis[1])
        await client.send_message(part1, part2)
        await client.send_message(part1, part3)
        if dis[1] < 6:
            if message.channel.id in allowedChannel or message.server.id in allowedServer:
                joke = await client.send_message(message.channel, delMsg)
                await asyncio.sleep(cooldown)
                await client.delete_message(joke)



    
client.run(obot.token) #bot
