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
    return "Get amount of ships created between people"

def help_param():
    return "<MENTION**>: Any amount of mentions of the users you want to get the ship amount of"

def help_cmd(prefix):
    return prefix + "shipcount <MENTION**>"

def help_perms():
    return 0

def help_list():
    return "Ship someone with someone else uwu"

def alias():
    return ['shipcount']