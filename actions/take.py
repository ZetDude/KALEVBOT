import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')

def run(message, game_prefix, aliasName):
    cmdlen = len(game_prefix + aliasName)
    opstring = message.content[cmdlen:].strip()
    try:
        opstring = int(opstring)
    except:
        return "m", [message.channel, message.author.mention + ", that isnt a number"]
    if opstring < 1:
        return "m", [message.channel, message.author.mention + ", that isnt a valid slot"]
    targetID = message.author.id
    playerlist = rpg.get_playerlist()
    targetEntity = playerlist[targetID]
    sts, out = targetEntity.take_room(opstring)
    return "m", [message.channel, message.author.mention + ", \n```diff\n" + str(out) + "\n```"]

def help_use():
    return "Take an item from the current room"

def help_param():
    return "<ROOM SLOT*>: The space in the room of the item to drop."

def help_cmd(prefix):
    return prefix + "drop <ROOM SLOT*>"

def help_perms():
    return 0

def help_list():
    return "Take an item."

def aliasName():
    return ['take', 'pick', 'pickup']
