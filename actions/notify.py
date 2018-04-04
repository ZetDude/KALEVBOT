import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')

def run(message, game_prefix, aliasName):
    return "m", [message.channel, rpg.ping()]

def help_use():
    return "Ping the users subscribed to the RPG announcement notify list."

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "notify"

def help_perms():
    return 7

def help_list():
    return "Ping the users subscribed to the RPG announcement notify list"

def aliasName():
    return ['notify']
