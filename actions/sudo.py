import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
import pickle

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader2.load_module('maincore')
loader3 = importlib.machinery.SourceFileLoader('item', sp + '/item.py')
item = loader3.load_module('item')

def run(message, rpgPrefix, aliasName):
    cmdlen = len(rpgPrefix + aliasName)
    opstring = message.content[cmdlen:].strip()
    param = opstring.split()
    rm = ""
    if param[0] == "player":
        if param[1] == "delete":
            if param[2] == "all":
                rpg.new_playerlist({})
            elif param[2] == "self":
                pList = rpg.get_playerlist()
                ded = pList.pop(message.author.id)
                rm += "! Deleted " + ded.name
                rpg.save_playerlist()
            else:
                pList = rpg.get_playerlist()
                ded = pList.pop(param[2])
                rm += "! Deleted " + ded.name
                rpg.save_playerlist()
        elif param[1] == "get":
            if param[2] == "all":
                pList = rpg.get_playerlist()
                for p in list(pList.values()):
                    rm += p.name + ", "
        elif param[1] == "add":
            if param[2] == "self":
                defaultStats = rpg.default_stats()
                playerlist = rpg.get_playerlist()
                playertemplate = {'name': message.author.name,
                                  'id': message.author.id,
                                  'stats': defaultStats,
                                  'inv': [None] * 10,
                                  'prop': {}}
                rpg.add_playerlist(message.author.id, playertemplate)
                rm += "! Added " + message.author.name
            else:
                t = message.guild.get_member(param[2])
                defaultStats = rpg.default_stats()
                playerlist = rpg.get_playerlist()
                playertemplate = {'name': t.name,
                                  'id': t.id,
                                  'stats': defaultStats,
                                  'inv': [None] * 10}
                rpg.add_playerlist(t.id, playertemplate)
                rm += "! Added " + t.name

    elif param[0] == "item":
        if param[1] == "add":
            if param[2] == "self":
                target = message.author.id
            else:
                target = param[2]
            playerlist = rpg.get_playerlist()
            items = rpg.return_itemlist()
            itemName = param[3].replace("_", " ")
            gItem = items[itemName]
            newItem = item.Item(gItem)
            targetP = playerlist[target]
            sts, cm = targetP.add_item(newItem)
            rm += "! Added " + newItem.name + " to " + targetP.name
            rm += "\n" + cm

    elif param[0] == "room":
        rooms = rpg.rooms
        tRoom = rooms[int(param[1])]
        if param[2] == "set":
            if param[3] == "desc":
                tRoom.desc = param[4].replace("_", " ")
                rm += "! Set description to <{}>\n".format(tRoom.desc)
            with open('important/rooms.txt', 'wb') as f:
                pickle.dump(roomlist, f)

    if rm == "":
        rm = "- Action complete. No response recieved"

    return "m", [message.channel, "```diff\n" + rm + "\n```"]



def help_use():
    return "Do almost anything with this command"

def help_param():
    return "<ARGUMENTS**>: Varies."

def help_cmd(prefix):
    return prefix + "sudo <ARGUMENTS**>"

def help_perms():
    return 10

def help_list():
    return "Do almost anything with this command"

def aliasName():
    return ['sudo']
