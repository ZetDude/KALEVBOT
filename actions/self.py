import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
import math

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader2.load_module('maincore')

def run(message, game_prefix, aliasName):
    targetID = ""
    if len(message.mentions) == 1:
        mentiont = message.mentions[0]
        targetID = mentiont.id
    else:
        cmdlen = len(game_prefix + aliasName)
        opstring = message.content[cmdlen:].strip()
        gotuser = core.userget(opstring, message.guild.id)
        if gotuser is None:
            targetID = message.author.id
        else:
            targetID = gotuser.id
    playerlist = rpg.get_playerlist()
    if targetID not in playerlist:
        return "m", [message.channel, message.author.mention + ", that person hasn't joined the game. %join to join the game!"]
    targetEntity = playerlist[targetID]
    targetStats = targetEntity.stats
    targetrStats = targetEntity.rawstats
    targetiStats = targetEntity.invstats
    targetName = targetEntity.name
    targetID = targetEntity.id
    targetInv = targetEntity.inv
    targetInvList = []
    for i in targetInv:
        if i is None:
            targetInvList.append(None)
            continue
        targetInvList.append(i.name)
    compileMSG = str("Entity: " + str(targetEntity) +
                     "\nStats: " + str(targetStats) +
                     "\nRaw stats: " + str(targetrStats) +
                     "\nEquip stats: " + str(targetiStats) +
                     "\nName: " + str(targetName) +
                     "\nID: " + str(targetID) +
                     "\nInventory: " + str(targetInv) +
                     "\nInventory Items: " + str(targetInvList)
    )
    return "m", [message.channel, message.author.mention + ", \n```\n" + str(compileMSG) + "\n```"]

def help_use():
    return "Fetch someone's Entity class and everything related to it"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "self"

def help_perms():
    return 2

def help_list():
    return "Fetch someone's Entity class"

def aliasName():
    return ['self']
