import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, alias):
    return "r", [message.channel]
    

def help_use():
    return "Re-launch the bot from scratch"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "relaunch"

def help_perms():
    return 10

def help_list():
    return "Re-launch the bot from scratch"

def alias():
    return ['relaunch']