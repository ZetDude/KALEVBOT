import importlib.machinery
import os
import sys
import pickle

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
shipfile = sp + "\\important\\shiplog.txt"

def run(message, prefix, alias):
    ships = message.mentions    
    shipsI = [x.id for x in ships]
    shipAdd = ':'.join(shipsI)
    with open(shipfile, "rb") as f:
        lines = pickle.loads(f.read())
    occ = lines.get(shipAdd, 0)
    
    timeS = " times "
    if occ == 1:
        timeS = " time "
    finalMSG = message.author.mention + ", they have been shipped " + str(occ) + timeS + "before"
    
    return "m", [message.channel, finalMSG] 

def help_use():
    return "Ship someone with someone else"

def help_param():
    return "<MENTION>: The mention for the users you want to ship"

def help_cmd(prefix):
    return prefix + "help <MENTION1> <MENTION2>"

def help_perms():
    return 0

def help_list():
    return "Ship someone with someone else uwu"

def alias():
    return ['shipcount']