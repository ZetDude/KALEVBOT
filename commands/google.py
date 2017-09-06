import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
loader = importlib.machinery.SourceFileLoader('maincore', sp + '\\maincore.py')
handle = loader.load_module('maincore')

def run(message, prefix, alias):
    return "m", handle.clink(message, alias, "<https://www.google.com/search?q=", ">", "+")


def help_use():
    return "Return the link for the google search page for the specified text"

def help_param():
    return "<TEXT*>: A string of character to search for in google"

def help_cmd(prefix):
    return prefix + "google <TEXT*>"

def help_perms():
    return 0

def help_list():
    return "Google the specified subject"

def alias():
    return ['google', 'g']