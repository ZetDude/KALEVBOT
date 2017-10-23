import importlib.machinery
import os
import sys
import pickle
from lib import shipname as improved_shipname

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core
shipfile = sp + "/important/shiplog.txt"

def run(message, prefix, alias):
    ships = message.mentions 
    if message.author in ships:
        core.send(message.channel, message.author.mention + ", I don't think you can ship yourself with someone")
        return
    if message.author.id == 264102274358312961:
        core.send(message.channel, message.author.mention + ", You cannot ship that person")
        return
    seen = set()
    seen_add = seen.add
    ships = [x for x in ships if not (x in seen or seen_add(x))]
    if not ships:
        core.send(message.channel, message.author.mention + ", how does one ship nobody? Mention at least two people in the message")
        return
    elif len(ships) == 1:
        core.send(message.channel, message.author.mention + ", they arent that lonely. Mention at least two people in the message")
        return
    ships_msg = [x.name for x in ships]
    shipsI = [str(x.id) for x in ships]
    ship_message = ' and '.join(ships_msg)
    shipAdd = ':'.join(shipsI)
    try:
        with open(shipfile, "rb") as f:
            lines = pickle.loads(f.read())
    except Exception as e:
        print(e)
        print("making file")
        lines = {}

    occ = lines.get(shipAdd, 0)
    
    timeS = " times "
    if occ == 1:
        timeS = " time "
    final_msg = message.author.mention + " totally ships " + ship_message + "\nThey have been shipped " + str(occ) + timeS + "before"
    
    occ += 1
    lines[shipAdd] = occ
    with open(shipfile, 'wb') as f: 
        pickle.dump(lines, f)
        
    if len(ships) == 2:
        first_half = ships_msg[0]
        second_half = ships_msg[-1]
        final = improved_shipname.shipname(first_half, second_half)
        final_msg += "\nI shall call it \"**" + final + "**\""
    
    core.send(message.channel, final_msg)

def help_use():
    return "Ship someone with someone else."

def help_param():
    return "<MENTION**>: Any amount of mentions for the users you want to ship."

def help_cmd(prefix):
    return prefix + "ship <MENTION**>"

def help_perms():
    return 0

def help_list():
    return "Ship someone with someone else. uwu"

def alias():
    return ['ship']
