import os
import sys
import pickle
import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
shipfile = sp + "/important/shiplog.txt"
help_info = {"use": "Get amount of ships created between people",
             "param": "{}shipcount [**MENTIONS]\n[**MENTIONS]: Mention of the user to check for",
             "perms": None,
             "list": "Get amount of ships created between people"}
alias_list = ['shipcount', 'shipnumber']

def search(values, search_for):
    r = []
    for k in values:
        vs = str(values[k])
        if str(search_for) in str(k):
            r.append([k, str(vs)])
    return r

def run(message, prefix, alias_name):
    del prefix
    del alias_name
    ships = message.mentions
    seen = set()
    seen_add = seen.add
    ships = [x for x in ships if not (x in seen or seen_add(x))]
    ships_id = [str(x.id) for x in ships]
    ship_add = ':'.join(ships_id)
    with open(shipfile, "rb") as file:
        lines = pickle.loads(file.read())
    if not ships:
        ships = [message.author]
    if len(ships) < 2:
        return_message = ""
        mentions = search(lines, ships[0].id)
        print(mentions)
#        mentions = sorted(mentions, key=lambda a: mentions[1])
        print(mentions)
        for k, j in mentions:
            inmsg = k.split(":")
            usern = []
            for i in inmsg:
                try:
                    usern.append(core.cl.get_user(int(i)).name)
                except:
                    usern.append(str(i))
            formatted = " x ".join(usern)
            time_string = "times_message"
            if j == 1:
                time_string = "time"
            return_message += "{}: shipped {} {}\n".format(formatted, j, time_string)
        core.send(message.channel, message.author.mention + ",\n```\n" + return_message + "\n```")
        return

    occ = lines.get(ship_add, 0)

    times_message = " times_message "
    if occ == 1:
        times_message = " time "
    final_message = (message.author.mention + ", they have been shipped " +
                str(occ) + times_message + "before")

    core.send(message.channel, final_message)
