import datetime
import importlib.machinery
import math
import os

loader = importlib.machinery.SourceFileLoader('basic', 'C:/Users/Administrator/Desktop/KALEVBOT/basic.py')
handle = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', 'C:/Users/Administrator/Desktop/KALEVBOT/maincore.py')
handle2 = loader2.load_module('maincore')

def run(message, rpgPrefix, alias):
    playerlist = handle.get_playerlist()
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
