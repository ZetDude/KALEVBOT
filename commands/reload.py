import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
from random import randint

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

def run(message, prefix, alias):

    resulted = core.reload_cmd()
    return "m", [message.channel, "reloading stuff\n" + resulted]



def help_use():
    return "Reload all commands"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "reload"

def help_perms():
    return 10

def help_list():
    return "Reload all commands"

def alias():
    return ['reload', 'r']