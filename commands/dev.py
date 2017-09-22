import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

def run(message, prefix, alias):
    core.send(message.channel, "ZetDude best developer 2017 <:zetdev:357193244679077890>")

def help_use():
    return "Try it!"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "dev"

def help_perms():
    return 0

def help_list():
    return "Display the best developer of 2017"

def alias():
    return ['dev', 'developer']