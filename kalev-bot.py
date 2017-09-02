import discord #Discord API
import asyncio #needed for discord messaging
import datetime #time module
from easyread import eread, ewrite #my own module to save space
import sys
import maincore as dc
import basic as rpg

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
    tolog1 = ''.join(c for c in tolog1 if c <= '\uFFFF')
    tolog2 = ''.join(c for c in tolog2 if c <= '\uFFFF')
    print(tolog1)
    print(tolog2)
    both = False
    if dc.check_if_prefix(message):
        both = True
        calc = dc.main(message)
        print("command detected")
    elif message.content.startswith("%"):
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

    colorRole = discord.utils.get(message.server.roles, name='party')

    if message.server.id == "333421004942475266":
        if colorRole in message.author.roles:
            global state
            global r
            global g
            global b
            print(state)
            print(r)
            print(g)
            print(b)
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

##            length = random.randint(1, 32)
##            newName = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
##            newName = ''.join("a" for i in range(length))
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



##    elif message.server.id == "327495595235213312" or message.server.id == "333421004942475266":
##        #if message.author.id == "215171991227990017" or message.author.id == "249717738581393409":
##            #message = None
##        if message.content.startswith('navy!'):
##            await client.send_message(message.channel, "What the fuck did you just fucking say about me, you little bitch? I’ll have you know I graduated top of my class in the Navy Seals, and I’ve been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I’m the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You’re fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that’s just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You’re fucking dead, kiddo.")
##        elif message.content.startswith('thighs!'):
##            await client.send_message(message.channel, "no, pecan >:G")
##        elif message.content.startswith('kalev! stop') or message.content.startswith('k!!!'):
##            if message.author.id in allowed() or str(message.author.top_role) == "mod":
##                await client.send_message(message.channel, "ITS ME GOODBYE! <https://youtu.be/y_hWeN249fs?t=25s>")
##                sys.exit()
##
##        elif message.content.startswith('google! hentai') or message.content.startswith('google!hentai'):
##            await client.send_message(message.channel, "no >:G")
##
##        elif message.content.startswith('google! anime legs') or message.content.startswith('google! animelegs'):
##            await client.send_message(message.channel, "no, pecan >:G")
##
##
##        elif message.content.startswith('kalev! del') or message.content.startswith('kalev! delete') or message.content.startswith('kddd'):
##            if message.author.id in allowed() or str(message.author.top_role) == "mod":
##                iid = eread("discordLast.txt")
##                iidf = eread("discordLastFrom.txt")
##
##                await client.delete_message(await client.get_message(client.get_channel(iidf), iid))
##
##        elif message.content.startswith('night!'):
##            userino = None
##            userino = message.mentions
##            print(userino)
##            if not userino:
##                await client.send_message(message.channel, "Good night!")
##            else:
##                part = ''
##                for i in range(len(userino)):
##                    print(userino[i].mention)
##                    part = part + userino[i].mention + ", "
##                part = part[:-2]
##                await client.send_message(message.channel, "Good night, " + part + "!")
##
##        elif message.content.startswith("identify add"):
##            print(message.content)
##            if message.content.find("!") != -1:
##                subnumb = [i for i, letter in enumerate(message.content) if letter == "!"]
##                numb = subnumb[-1] + 1
##                toadd = message.content[numb:].strip()
##                userino = None
##                userino = message.mentions
##                if not userino:
##                    userino = message.author
##                else:
##                    userino = message.mentions[0]
##                filename = "id00" + userino.id + ".txt"
##                if not os.path.exists(filename):
##                    open(filename, 'w').close()
##                with open(filename, 'r') as f:
##                    lines = [line.rstrip('\n') for line in f]
##                lines.append(toadd)
##                with open(filename, 'w') as f:
##                    for s in lines:
##                        f.write(str(s) + "\n")
##                    f.close()
##
##
##        elif message.content.startswith("identify!"):
##            userino = None
##            userino = message.mentions
##            if not userino:
##                userino = message.author
##            else:
##                userino = message.mentions[0]
##            filename = "id00" + userino.id + ".txt"
##            with open(filename, 'r') as f:
##                lines = [line.rstrip('\n') for line in f]
##
##
##            part = ''
##            for i in lines:
##                part = part + i + ". "
##
##            part = part[:-2]
##
##            await client.send_message(message.channel, "Identification: " + part)
##
##        elif message.content.startswith("kalev! trello"):
##            await client.send_message(message.channel, "<https://trello.com/b/OvW6oyqH/kalevbot>")
##
##
##        elif message.content.startswith('timer!'):
##            await client.send_message(message.channel, "Hm? What was that? You used an empty command. Try `kalev! help` or `kalev! pm` for help")
##
##        elif message.content.startswith('kalev!'):
##            await client.send_message(message.channel, "Hm? What was that? You used an empty command. Try `kalev! help` or `kalev! pm` for help")
##
##        elif message.content.startswith('dev!'):
##            await client.send_message(message.channel, "ZetDude best developer 2017 :sunglasses:")
##
##        elif message.content.startswith('gravity!'):
##            await client.send_message(message.channel, "<")
##
##        elif message.content.startswith("something!"):
##            if message.author.id == "104626896360189952":
##                for server in client.servers:
##                    for channel in server.channels:
##                        print(server.name + ":" + channel.name + "-" + channel.id)
##                perms = client.get_channel("328467442131140608").permissions_for(client.get_server("327495595235213312").get_member("223944789437972490"))
##                for i in iter(perms):
##                    print(i)
##
##        elif message.channel.id == "328467442131140608":
##            print(str(datetime.utcnow()) + ";;" + message.author.name + ":" + message.content)
##
##        else:
##            wascommand = 0
##
##
##        if message.author.id == "342125773307510784":
##            ewrite("discordLast.txt", message.id)
##            ewrite("discordLastFrom.txt", message.channel.id)
##
##
##        if wascommand == 1:
##            counter = int(eread("discordCount.txt"))
##            counter = counter + 1
##            ewrite("discordCount.txt", counter)
##            with open('discordLog.txt', 'r') as f:
##                lines = [line.rstrip('\n') for line in f]
##            tolog = ("at " + str(datetime.datetime.utcnow() + datetime.timedelta(hours=3)) + " in " + message.server.name + " in " + message.channel.name + "- " + message.author.name + " said: '" + message.content).encode(sys.stdout.encoding, errors='replace')
##            print(tolog)
##            lines.append(tolog)
##            with open('discordLog.txt', 'w') as f:
##                for s in lines:
##                    f.write(str(s) + "\n")
##            f.close()
##
##
##    else:
##        if message.content.startswith('timer!'):
##            await client.send_message(message.channel, "Kalev Bot was not designed to work on this server, therefore I cannot help you here.")
##
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




client.run('MzQyMTI1NzczMzA3NTEwNzg0.DGLE_g.jarfFFlmUbzFQtKZga0pJE33QDo') #bot
