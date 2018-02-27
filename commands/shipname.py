import importlib.machinery
import os
import sys
from lib import shipname as improved_shipname

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, aliasName):
    cmdlen = len(prefix + aliasName)
    opstring = message.content[cmdlen:].strip()
    ships_msg = opstring.split()
    first_half = ships_msg[0]
    second_half = ships_msg[-1]
    overflowWarning = "\n**More than 2 names given, only taking the first and last ones**" if len(ships_msg) > 2 else ""
    final = improved_shipname.shipname(first_half, second_half)
    final_msg = overflowWarning + "\nI shall call it \"**" + final + "**\""

    core.send(message.channel, message.author.mention + final_msg)

def help_use():
    return "Create the shipname of two people."

def help_param():
    return "<NAMES**>: Names of people to ship."

def help_cmd(prefix):
    return prefix + "shipname <NAMES**>"

def help_perms():
    return 0

def help_list():
    return "Create the shipname of two people."

def aliasName():
    return ['shipname']
