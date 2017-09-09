import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

def run(message, prefix, alias):
    return "m", core.clink(message, alias, "<http://www.urbandictionary.com/define.php?term=", ">", "+")


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

def alias():
    return ['urban', 'urbandictionary', 'ud']