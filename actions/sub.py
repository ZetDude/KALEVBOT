import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')

def run(message, rpgPrefix, alias):
    return "m", [message.channel, rpg.sub(message.author, True)]

def help_use():
    return "Subscribe to the RPG announcement notify list"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "sub"

def help_perms():
    return 0

def help_list():
    return "Subscribe to the RPG announcement notify list"

def alias():
    return ['sub']
