import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
loader = importlib.machinery.SourceFileLoader('basic', sp + '\\basic.py')
handle = loader.load_module('basic')

def run(message, rpgPrefix, alias):
    cmdlen = len(rpgPrefix + alias)
    opstring = message.content[cmdlen:].strip()
    try:
        opstring = int(opstring)
    except:
        return "m", [message.channel, message.author.mention + ", that isnt a number"]
    targetID = message.author.id
    playerlist = handle.get_playerlist()
    targetEntity = playerlist[targetID]
    out = targetEntity.equip_slot(opstring)
    return "m", [message.channel, message.author.mention + ", \n```diff\n" + str(out) + "\n```"]

def help_use():
    return "Equip an item"

def help_param():
    return "<INVENTORY SLOT*>: The inventory slot of the item to equip."

def help_cmd(prefix):
    return prefix + "equip <INVENTORY SLOT*>"

def help_perms():
    return 0

def help_list():
    return "Equip an item."

def alias():
    return ['equip']
