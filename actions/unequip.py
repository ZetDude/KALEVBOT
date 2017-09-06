import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
loader = importlib.machinery.SourceFileLoader('basic', sp + '\\basic.py')
handle = loader.load_module('basic')

def run(message, rpgPrefix, alias):
    cmdlen = len(rpgPrefix + alias)
    opstring = message.content[cmdlen:].strip().lower()
    possible = {"weapon": "weapon",
                "armor": "torso",
                "torso": "torso",
                "legs": "legs",
                "leggings": "legs",
                "ring": "ring1",
                "ring1": "ring1",
                "tongue": "tongue",
                "tounge": "tongue",
                "ring2": "ring2"}
    if opstring in possible:
        opstring = possible[opstring]
    else:
        return "m", [message.channel, message.author.mention + ", that isnt a slot"]
    targetID = message.author.id
    playerlist = handle.get_playerlist()
    targetEntity = playerlist[targetID]
    st, out = targetEntity.unequip(opstring)
    return "m", [message.channel, message.author.mention + ", \n```diff\n" + str(out) + "\n```"]

def help_use():
    return "Unequip an item"

def help_param():
    return "<INVENTORY SLOT*>: The inventory slot of the item to unequip."

def help_cmd(prefix):
    return prefix + "unequip <INVENTORY SLOT*>"

def help_perms():
    return 0

def help_list():
    return "Unequip an item."

def alias():
    return ['unequip']
