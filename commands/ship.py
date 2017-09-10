import importlib.machinery
import os
import sys
import pickle

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')
shipfile = sp + "/important/shiplog.txt"

def run(message, prefix, alias):
    ships = message.mentions 
    if message.author in ships:
        return "m", [message.channel, message.author.mention + ", I don't think you can ship yourself with someone"]
    seen = set()
    seen_add = seen.add
    ships = [x for x in ships if not (x in seen or seen_add(x))]
    if not ships:
        return "m", [message.channel, message.author.mention + ", how does one ship nobody? Mention at least two people in the message"]
    elif len(ships) == 1:
        return "m", [message.channel, message.author.mention + ", they arent that lonely. Mention at least two people in the message"]
    ships_msg = [x.name for x in ships]
    shipsI = [x.id for x in ships]
    ship_message = ' and '.join(ships_msg)
    shipAdd = ':'.join(shipsI)
    with open(shipfile, "rb") as f:
        lines = pickle.loads(f.read())
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
        first_half = len(ships_msg[0]) // 2   # get the half of the first shipped person
        second_half = len(ships_msg[1]) // 2 # get the half of the second shipped person
        combine1 = ships_msg[0][:first_half]      # get the first half of the first person's nickname
        combine2 = ships_msg[1][-second_half:]   # get the second half of the second person's nickname
        final = combine1 + combine2                  # combine them
        final_msg += "\nI shall call it '*" + final + "*'" # add it to the final message
    
    return "m", [message.channel, final_msg] 

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
