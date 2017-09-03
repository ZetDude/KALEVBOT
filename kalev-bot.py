import discord #Discord API
import asyncio #needed for discord messaging
import relaytimegeneratorbot as rbot #my own thing that calculates deadlines
import datetime #time module
import time #another time module
from easyread import eread, ewrite #my own module to save space
import sys
import pytz
import random
import os
import maincore as dc
import string
import basic as rpg
import colorsys
import obot

client = discord.Client()
ll = ""
newColorValue = 0

r = 255
g = 0
b = 0
state = 0

@asyncio.coroutine
def periodic():
    while True:
        yield from asyncio.sleep(7200)
        logChannel = client.get_channel("333421973462056961")
        yield from client.send_message(logChannel, "Bi-hourly reminder that I am still functional")
        difference = dc.get_timer()
        p_working = "I have been running for " + str(difference)
        yield from client.send_message(logChannel, p_working)
        

def stop():
    task.cancel()

async def getlingo(uid):
    return client.get_user_info("97128312651935744")

def is_me(m):
    zaAnswer = m.author == client.user
    print(zaAnswer)
    return zaAnswer
    
@client.event
async def on_ready():
    dc.ready(client)
    rpg.ready()
    await client.change_presence(game=discord.Game(name=dc.fetch_game()))
    task = asyncio.Task(periodic())
    loop = asyncio.get_event_loop()

@client.event
async def on_message(message):
    if message.server == None:
        fse = str(message.channel)
        if message.author.id != "342125773307510784":
            await client.send_message(client.get_channel("333421973462056961"), ">>" + message.author.name + " in " + fse + ">>\n||" + message.content + "||")
    else:
        fse = message.channel.name
    tolog1 = message.author.name + " in " + fse + ">>"
    tolog2 = message.content
    tolog3 = ""
    tolog4 = ""
    tolog1 = ''.join(c for c in tolog1 if c <= '\uFFFF')
    tolog2 = ''.join(c for c in tolog2 if c <= '\uFFFF')
    print(tolog1)
    print(tolog2)
    both = False
    if message.author.bot:
        both = False
    elif dc.check_if_prefix(message):
        wascommand = 1
        both = True
        calc = dc.main(message)
        print("command detected")
    elif message.content.startswith("%"):
        wascommand = 1
        both = True
        calc = rpg.run(message)
        print("rpg message detected")

    #await client.send_typing(message.channel)
    if both:
        await client.send_typing(message.channel)
        #if message.author.name == "mareck (✿◠‿◠)":
            #await client.send_message(message.channel, "You said you didn't need me")
            #both = False

    sp = message.content.split()
    botChannel = client.get_channel(sp[0])
    if message.channel.id == "352001441046593538":
        if message.author.id == "104626896360189952":
            say = ""
            for m in sp[1:]:
                say += m + " "
            await client.send_message(botChannel, say)

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
                print(newColorValue)
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
                await client.send_message(p[0], p[1])

            elif rty == "p":
                if message.server == None:
                    fse = str(p[0])

                else:
                    fse = p[0].name
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
                        print("-", end="")
                    iterat = iterat + 1 - len(deleted)
                    fianlc = fianlc + 1
                    if iterat > 52:
                        break
                    totaldel = totaldel + len(deleted)
                    if len(deleted) > 0:
                        print(str(totaldel) + "/" + str(p) + " ; " + str(fianlc))
                    deleted = []
                #print("----------------")
                await client.send_message(message.author, "Deleted " + str(totaldel) + " messages using " + str(fianlc) + " tries")


        counter = int(eread("discordCount.txt"))
        counter = counter + 1
        ewrite("discordCount.txt", counter)
        with open('discordLog.txt', 'r') as f:
            lines = [line.rstrip('\n') for line in f]
            #tolog1 = str(list(filter(lambda x: x in string.printable, tolog1.encode(sys.stdout.encoding, errors='replace'))))
            #tolog2 = str(list(filter(lambda x: x in string.printable, tolog2.encode(sys.stdout.encoding, errors='replace'))))
            #tolog3 = str(list(filter(lambda x: x in string.printable, tolog3.encode(sys.stdout.encoding, errors='replace'))))
            #tolog4 = str(list(filter(lambda x: x in string.printable, tolog4.encode(sys.stdout.encoding, errors='replace'))))
            lines.append(tolog1)
            lines.append(tolog2)
            lines.append("-------")
        with open('discordLog.txt', 'w') as f:
           for s in lines:
                cs = ''.join(c for c in s if c <= '\u2000')
                f.write(str(cs) + "\n")         

normal = ["341368223716868097", "328642054055788565"]
shortfuse = ["327495595235213312", "335947662916583424", "328465541045944320", "331493330456150016", "328642054055788565"]
banned = ["328635358223007744", "330043707485323265", "334425754265714690", "328466576473063424", "328464281106645003", "328465486398619648"]
@client.event
async def on_message_delete(message):
    if message.author.id != "342125773307510784":
        time1 = message.timestamp
        time2 = datetime.datetime.utcnow()
        c = time2 - time1
        dis = divmod(c.days * 86400 + c.seconds, 60)
        print("Message deleted " + str(dis[1]) + " seconds ago")
        if dis[1] < 6:
            if message.channel.id in normal:
                joke = await client.send_message(message.channel, "<:instadel:328651110799900672>")
                await asyncio.sleep(180)
                await client.delete_message(joke)
            elif message.channel.id in shortfuse:
                print("slorany is evil")
            else:
                print("mareck is evil")



    
client.run(obot.token) #bot
