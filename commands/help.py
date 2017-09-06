import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '\\maincore.py')
handle = loader.load_module('maincore')

def run(message, prefix, alias):
    helptext = handle.get_helptext()
    if message.content.strip() == prefix + alias:
        return "p", [message.author, helptext, message.channel, "Alright " + message.author.mention + ", check your DMs"]
    else:
        cmdlen = len(prefix + alias)
        opstring = message.content[cmdlen:].strip()
        helptexta = "something bad happened"
        helptexta = handle.compose_help(opstring)
        return "m", [message.channel, helptexta]

def help_use():
    return "PM all the commands to the user or show more specific help about a single command"

def help_param():
    return "<COMMAND>: Optional. The command to get more specific infomation about. When not given, PM all the commands instead"

def help_cmd(prefix):
    return prefix + "help <COMMAND>"

def help_perms():
    return 0

def help_list():
    return "Get all the help or help about a specific command"

def alias():
    return ['help', 'halp', 'h', 'commands', 'command']