import importlib.machinery
import os
import sys
import pickle

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

shipfile = sp + "\\important\\shiplog.txt"

def run(message, prefix, alias):
    ships = message.mentions 
    if message.author in ships:
        return "m", [message.channel, message.author.mention + ", I don't think you can ship yourself with someone"]
    seen = set()
    seen_add = seen.add
    ships = [x for x in ships if not (x in seen or seen_add(x))]
    if len(ships) == 0:
        return "m", [message.channel, message.author.mention + ", how does one ship nobody? Mention at least two people in the message"]
    elif len(ships) == 1:
        return "m", [message.channel, message.author.mention + ", they arent that lonely. Mention at least two people in the message"]
    shipsM = [x.mention for x in ships]
    shipsI = [x.id for x in ships]
    shipMsg = ' and '.join(shipsM)
    shipAdd = ':'.join(shipsI)
    with open(shipfile, "rb") as f:
        lines = pickle.loads(f.read())
    occ = lines.get(shipAdd, 0)
    
    timeS = " times "
    if occ == 1:
        timeS = " time "
    finalMSG = message.author.mention + " totally ships " + shipMsg + "\nThey have been shipped " + str(occ) + timeS + "before"
    
    occ += 1
    lines[shipAdd] = occ
    with open(shipfile, 'wb') as f: 
        pickle.dump(lines, f)
    
    return "m", [message.channel, finalMSG] 

def help_use():
    return "Ship someone with someone else"

def help_param():
    return "<MENTION>: The mention for the users you want to ship"

def help_cmd(prefix):
    return prefix + "ship <MENTION1> <MENTION2>"

def help_perms():
    return 0

def help_list():
    return "Ship someone with someone else uwu"

def alias():
    return ['ship']