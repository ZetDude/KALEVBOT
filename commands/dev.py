import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, aliasName):
    del prefix
    del aliasName
    core.send(message.channel, "ZetDude best developer of 2017 and 2018 <:zetdev:357193244679077890>")

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

def aliasName():
    return ['dev', 'developer']
