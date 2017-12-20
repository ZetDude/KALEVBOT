import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')

def run(message, rpgPrefix, aliasName):
    roomlist = rpg.rooms
    playerlist = rpg.playerlist
    selfClass = playerlist[message.author.id]
    sNow = selfClass.rawstats['location']
    ident = roomlist[sNow].get_desc()

    bothMSG = "You are in room " + str(sNow)
    publicMSG = message.author.mention + ", \n```diff\n" + bothMSG + "\n```"
    privateMSG = "```diff\n" + bothMSG + "\n" + ident + "\n```"
    return "p", [message.author, privateMSG, message.channel, publicMSG]

def help_use():
    return "Look at what the current room you are in looks like"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "look"

def help_perms():
    return 0

def help_list():
    return "Look at the current room"

def aliasName():
    return ['look']
