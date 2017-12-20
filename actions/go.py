import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')

def run(message, rpgPrefix, aliasName):
    cmdlen = len(rpgPrefix + aliasName)
    opstring = message.content[cmdlen:].strip()
    if message.content == rpgPrefix + aliasName:
        roomlist = rpg.rooms
        amount = str(len(roomlist))
        return "m", [message.channel, message.author.mention + ", a total of " + amount + " rooms have been found."]
    try:
        opstring = int(opstring)
    except:
        return "m", [message.channel, message.author.mention + ", that isnt a number"]
    if opstring < 0:
        return "m", [message.channel, message.author.mention + ", cannot break spacetime and travel outside the positive space"]
    playerlist = rpg.get_playerlist()
    selfEntity = playerlist[message.author.id]
    err, out = selfEntity.jump_to(opstring)
    if not err:
        return "m", [message.channel, message.author.mention + ", " + str(out)]

    return "m", [message.channel, message.author.mention + ", \n```diff\n" + str(out) + "\n```"]

def help_use():
    return "Move to an already explored room. You must not complete the actions in it, you can do this action indefinitely, without a turn passing"

def help_param():
    return "<ROOM NUMBER*>: The number of the room to go to."

def help_cmd(prefix):
    return prefix + "go <ROOM NUMBER*>"

def help_perms():
    return 0

def help_list():
    return "Move to an already explored room."

def aliasName():
    return ['go', 'goto']
