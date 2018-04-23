import os
import sys
import pickle
from lib import shipname as improved_shipname
import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
help_info = {"use": "Ship someone with someone else.",
             "param": "{}ship [**MENTIONS]\n[**MENTIONS]: Any amount of mentions of users to ship",
             "perms": None,
             "list": "Ship someone with someone else. uwu"}
alias_list = ['ship']

shipfile = sp + "/important/shiplog.txt"

def run(message, prefix, alias_name):
    del prefix
    del alias_name
    ships = message.mentions
    if message.author in ships:
        core.send(message.channel,
                  message.author.mention + ", I don't think you can ship yourself with someone")
        return
    if message.author.id == 264102274358312961:
        core.send(message.channel,
                  message.author.mention + ", You cannot ship that person")
        return
    seen = set()
    seen_add = seen.add
    ships = [x for x in ships if not (x in seen or seen_add(x))]
    if not ships:
        core.send(message.channel,
                  message.author.mention + ", mention at least two people in the message")
        return
    elif len(ships) == 1:
        core.send(message.channel,
                  message.author.mention + ", mention at least two people in the message")
        return
    ships_msg = [x.name for x in ships]
    ships_id = [str(x.id) for x in ships]
    ship_message = ' and '.join(ships_msg)
    ship_add = ':'.join(ships_id)
    try:
        with open(shipfile, "rb") as file:
            lines = pickle.loads(file.read())
    except FileNotFoundError:
        print("making file")
        lines = {}

    occ = lines.get(ship_add, 0)

    times_message = " times "
    if occ == 1:
        times_message = " time "
    final_msg = (message.author.mention + " totally ships " + ship_message +
                 "\nThey have been shipped " + str(occ) + times_message + "before")

    occ += 1
    lines[ship_add] = occ
    with open(shipfile, 'wb') as file:
        pickle.dump(lines, file)

    if len(ships) == 2:
        first_half = ships_msg[0]
        second_half = ships_msg[-1]
        final = improved_shipname.shipname(first_half, second_half)
        final_msg += "\nI shall call it \"**" + final + "**\""

    core.send(message.channel, final_msg)
