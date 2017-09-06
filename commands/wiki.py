import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '\\maincore.py')
handle = loader.load_module('maincore')

def run(message, prefix, alias):
    return "m", handle.cwiki(message, "wiki", "<http://", ".wikipedia.org/wiki/", ">", "_")


def help_use():
    return "Return the link for the wikipedia definiton page for the specified text"

def help_param():
    return "<TEXT*>: A string of character to search for in wikipedia"

def help_cmd(prefix):
    return prefix + "wiki <TEXT*>"

def help_perms():
    return 0

def help_list():
    return "Show the wikipedia definiton for the specified subject"

def alias():
    return ['wiki', 'wikipedia']