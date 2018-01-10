import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')

def run(message, prefix, aliasName):
    helptext = rpg.get_helptext()
    if message.content.strip() == prefix + "help":
        return "m", [message.channel, helptext]
    else:
        cmdlen = len(prefix + aliasName)
        opstring = message.content[cmdlen:].strip()
        helptexta = "something bad happened"
        helptexta = rpg.compose_help(opstring)
        return "m", [message.channel, helptexta]

def help_use():
    return "Post all the commands in chat or show more specific help about a single command"

def help_param():
    return "<COMMAND>: Optional. The command to get more specific infomation about. When not given, display all the commands instead"

def help_cmd(prefix):
    return prefix + "help <COMMAND>"

def help_perms():
    return 0

def help_list():
    return "Get all the help or help about a specific command"

def aliasName():
    return ['help']
