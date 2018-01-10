import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, aliasName):
    core.send(message.channel, core.clink(message, aliasName, "<http://www.urbandictionary.com/define.php?term=", ">", "+"))


def help_use():
    return "Return the link for the urban dictionary definiton page for the specified text"

def help_param():
    return "<TEXT*>: A string of character to search for in urban dictionary"

def help_cmd(prefix):
    return prefix + "urban <TEXT*>"

def help_perms():
    return 0

def help_list():
    return "Show the urban dictionary definiton for the specified subject"

def aliasName():
    return ['urban', 'urbandictionary', 'ud']
