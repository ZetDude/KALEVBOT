import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader2.load_module('maincore')

def run(message, rpgPrefix, alias):
    playerlist = rpg.get_playerlist()
    selfEntity = playerlist[message.author.id]
    pMSG, lMSG = selfEntity.explore()
        
    return "p", [message.channel, message.author.mention + "!\n```diff\n" + pMSG + "\n```", message.author, "```diff\n" + lMSG + "\n```"]

def help_use():
    return "Further continue your adventure. This goes to your latest explored room and moves on by 1. You then must complete the action that might arise in that room"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "explore"

def help_perms():
    return 0

def help_list():
    return "Further continue your adventure"

def alias():
    return ['explore']
