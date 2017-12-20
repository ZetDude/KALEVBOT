import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, aliasName):
    helptext = core.get_helptext()
    return "m", [message.channel, helptext]

def help_use():
    return "Post all the commands in chat, but watch out, it takes up a lot of room in chat"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "chathelp"

def help_perms():
    return 3

def help_list():
    return "Post the help in chat"


def aliasName():
    return ['chathelp', 'chelp', 'ch', 'chath']
