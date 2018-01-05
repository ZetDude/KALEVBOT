import os
import sys
import pickle

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
shipfile = sp + "/important/shiplog.txt"

import maincore as core

def search(values, searchFor):
    r = []
    for k in values:
        vs = str(values[k])
        if str(searchFor) in str(k):
            r.append([k, str(vs)])
    return r

def run(message, prefix, aliasName):
    ships = message.mentions
    seen = set()
    seen_add = seen.add
    ships = [x for x in ships if not (x in seen or seen_add(x))]
    shipsI = [str(x.id) for x in ships]
    shipAdd = ':'.join(shipsI)
    with open(shipfile, "rb") as f:
        lines = pickle.loads(f.read())
    if len(ships) == 0:
        ships = [message.author]
    if len(ships) < 2:
        returnMSG = ""
        mentions = search(lines, ships[0].id)
        mentions = sorted(mentions, key=lambda a: mentions[1])
        for k, j in mentions:
            inmsg = k.split(":")
            usern = []
            for i in inmsg:
                try:
                    usern.append(core.cl.get_user(int(i)).name)
                except:
                    usern.append(str(i))
            formatted = " x ".join(usern)
            timeString = "times"
            if j == 1:
                timeString = "time"
            returnMSG += "{}: shipped {} {}\n".format(formatted, j, timeString)
        core.send(message.channel, message.author.mention + ",\n```\n" + returnMSG + "\n```")
        return

    occ = lines.get(shipAdd, 0)

    timeS = " times "
    if occ == 1:
        timeS = " time "
    finalMSG = message.author.mention + ", they have been shipped " + str(occ) + timeS + "before"

    core.send(message.channel, finalMSG)

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

def aliasName():
    return ['shipcount', 'shiplist']
