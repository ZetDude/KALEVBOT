import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
import math

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')

def run(message, rpgPrefix, alias):
    mul = 1
    compileMSG = ""
    cmdlen = len(rpgPrefix + alias)
    opstring = message.content[cmdlen:].strip()
    spaceloc = opstring.find(" ")
    if spaceloc == -1:
        return "m", [message.channel, message.author.mention + ", expected 2 arguments"]
    else:
        stat = opstring[:spaceloc].strip().lower()
        amount = opstring[spaceloc:].strip()
    try:
        amount = int(amount)
    except:
        return "m", [message.channel, message.author.mention + ", not a number amount"]

    if amount < 0:
        return "m", [message.channel, message.author.mention + ", cannot downgrade"]

    targetID = message.author.id
    playerlist = rpg.get_playerlist()
    if targetID not in playerlist:
        return "m", [message.channel, message.author.mention + ", that person hasn't joined the game. %join to join the game!"]
    targetEntity = playerlist[targetID]
    returnMSG = targetEntity.rawstats
    statPoints = returnMSG['statpoints']
    
    
    if stat == "health":
        ti = 'maxhealth'
        mul = 2
    elif stat == "attack":
        ti = stat
    elif stat == "speed":
        ti = stat
    elif stat == "defense":
        ti = stat
    elif stat == "luck":
        ti = stat
    else:
        return "m", [message.channel, message.author.mention + ", unknown stat"]

    if amount > statPoints:
        return "m", [message.channel, message.author.mention + ", can't upgrade more than the points you have"]

    addPoints = int(math.floor(amount * mul))
    wasPoints = returnMSG[ti]
    returnMSG[ti] = returnMSG[ti] + addPoints
    newRemaining = statPoints - amount
    wasStatPoints = returnMSG['statpoints']
    returnMSG['statpoints'] = newRemaining
    if ti == 'maxhealth':
        returnMSG['health'] = returnMSG['health'] + addPoints
    compileMSG = compileMSG + "Upgraded stat " + stat + " to " + str(returnMSG[ti]) + " points (was " + str(wasPoints) + ")\n"
    compileMSG = compileMSG + "You now have " + str(newRemaining) + " points (had " + str(wasStatPoints) + ")\n"
    compileMSG = compileMSG + "(Spent " + str(amount) + " points and upgraded stat by " + str(addPoints) + ")\n"
    targetEntity.rawstats = returnMSG
    targetEntity.stats = targetEntity.calculate_stats()
    rpg.save_playerlist()
    return "m", [message.channel, message.author.mention + ", \n```diff\n" + str(compileMSG) + "\n```"]

def help_use():
    return "Imporve a stat by investing stat points into it"

def help_param():
    return """<STAT*>: The stat to upgrade. This is one of:
"Health", "Attack", "Speed", "Defense", "Luck", "Lewdness". Capitalization doesn't matter
<AMOUNT>: A number of how many points to allocate."""

def help_cmd(prefix):
    return prefix + "upgrade <STAT*> <AMOUNT*>"

def help_perms():
    return 0

def help_list():
    return "Improve a stat"

def alias():
    return ['upgrade']
