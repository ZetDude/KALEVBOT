import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, alias):
    myguild = message.guild
    finalMsg = ""
    finalMsg += "You are in \"**{}**\", a guild owned by **{}**\n".format(myguild.name, myguild.owner.name)
    memberList = myguild.members
    finalMsg += "It has __{}__ members,\n".format(myguild.member_count)
    humans = 0
    bots = 0
    for i in memberList:
        if i.bot:
            bots += 1
        else:
            humans += 1
    finalMsg += "__{}__ of which are humans, and __{}__ are bots\n".format(humans, bots)
    finalMsg += "and i'm on the guild, which is the best part!"
    core.send(message.channel, finalMsg)


def help_use():
    return "Analyze the current guild"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "guild"

def help_perms():
    return 0

def help_list():
    return "Analyze the current guild"

def alias():
    return ['guild', 'analyze', 'server']
