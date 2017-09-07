import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
handle = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
handle2 = loader2.load_module('maincore')

def run(message, rpgPrefix, alias):
    authorID = message.author.id
    playerlist = handle.get_playerlist()
    if authorID in playerlist:
        welcome1 = "You remove your existence from the universe...\n"
        welcome2 = "That was easy."
        playerlist.pop(authorID)
        handle.save_playerlist()
        return "m", [message.channel, message.author.mention + "!\n```diff\n" + welcome1 + welcome2 + "\n```"]
    else:
        return "m", [message.author, message.author.mention + "!\n```diff\n" + "Can't leave when you never joined!" + "\n```"]

def help_use():
    return "Delete your Entity from the files"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "leave"

def help_perms():
    return 0

def help_list():
    return "Leave the fun"

def alias():
    return ['leave', 'escape', 'quit', 'exit']
