import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

def run(message, prefix, alias):
    myServer = message.server
    finalMsg = ""
    finalMsg += "You are in \"**{}**\", a server owned by **{}**\n".format(myServer.name, myServer.owner.name)
    memberList = myServer.members
    finalMsg += "It has __{}__ members,\n".format(myServer.member_count)
    humans = 0
    bots = 0
    for i in memberList:
        if i.bot:
            bots += 1
        else:
            humans += 1
    finalMsg += "__{}__ of which are humans, and __{}__ are bots\n".format(humans, bots)
    finalMsg += "and i'm on the server, which is the best part!"
    core.send(message.channel, finalMsg)
    

def help_use():
    return "Analyze the current server"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "server"

def help_perms():
    return 0

def help_list():
    return "Analyze the current server"

def alias():
    return ['server', 'analyze']