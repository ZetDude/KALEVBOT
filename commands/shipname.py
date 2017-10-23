import importlib.machinery
import os
import sys
from lib import shipname

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

def run(message, prefix, alias):
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()
    ships_msg = opstring.split()
    try:
        ship = shipname.shipname(ships_msg[0], ships_msg[-1])
        final_msg = "\nI shall call it \"**" + ship + "**\"" # add it to the final message
    except IndexError:
        core.send(message.channel, message.author.mention + ", not enough parameters")
        return

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
