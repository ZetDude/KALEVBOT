import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

def run(message, prefix, alias):
    helptext = core.get_helptext()
    return "m", [message.channel, helptext]

def help_use():
    return "Post all the commands in chat, but watch out, it takes up a lot of room in chat"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "chathelp"

def help_perms():
    return ["MANAGE MESSAGES"]

def help_list():
    return "Post the help in chat"


def alias():
    return ['chathelp', 'chelp', 'ch', 'chath']
    
