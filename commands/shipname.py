import importlib.machinery
import os
import sys
from lib import shipname as improved_shipname

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, alias):
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()
    ships_msg = opstring.split()
    first_half = ships_msg[0]
    second_half = ships_msg[-1]
    final = improved_shipname.shipname(first_half, second_half)
    final_msg = "\nI shall call it \"**" + final + "**\""

    core.send(message.channel, message.author.mention + final_msg)

def help_use():
    return "Create the shipname of two people."

def help_param():
    return "<NAMES**>: Names of people to ship."

def help_cmd(prefix):
    return prefix + "drop <NAMES**>"

def help_perms():
    return 0

def help_list():
    return "Create the shipname of two people."

def alias():
    return ['shipname']
