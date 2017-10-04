import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, alias):
    return "m", core.cwiki(message, alias, "<http://", ".wiktionary.org/wiki/", ">", "_")


def help_use():
    return "Return the link for the wiktionary definiton page for the specified text"

def help_param():
    return "<TEXT*>: A string of characters to search for in wiktionary"

def help_cmd(prefix):
    return prefix + "wikti <TEXT*>"

def help_perms():
    return 0

def help_list():
    return "Show the wiktionary definiton for the specified subject"

def alias():
    return ['wikti', 'wiktionary']