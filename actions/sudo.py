import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
import pickle

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
handle = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
handle2 = loader2.load_module('maincore')
loader3 = importlib.machinery.SourceFileLoader('item', sp + '/item.py')
handle3 = loader3.load_module('item')

def run(message, rpgPrefix, alias):
    cmdlen = len(rpgPrefix + alias)
    opstring = message.content[cmdlen:].strip()
    param = opstring.split()
    rm = ""
    if param[0] == "player":
        if param[1] == "delete":
            if param[2] == "all":
                handle.new_playerlist({})
            elif param[2] == "self":
                pList = handle.get_playerlist()
                ded = pList.pop(message.author.id)
                rm += "! Deleted " + ded.name
                handle.save_playerlist()
            else:
                pList = handle.get_playerlist()
                ded = pList.pop(param[2])
                rm += "! Deleted " + ded.name
                handle.save_playerlist()
        elif param[1] == "get":
            if param[2] == "all":
                pList = handle.get_playerlist()
                for p in list(pList.values()):
                    rm += p.name + ", "
        elif param[1] == "add":
            if param[2] == "self":
                defaultStats = handle.default_stats()
                authorID = message.author.id
                playerlist = handle.get_playerlist()
                playertemplate = {'name': message.author.name,
                                  'id': message.author.id,
                                  'stats': defaultStats,
                                  'inv': [None] * 10,
                                  'prop': {}}
                handle.add_playerlist(message.author.id, playertemplate)
                rm += "! Added " + message.author.name
            else:
                t = message.server.get_member(param[2])
                defaultStats = handle.default_stats()
                playerlist = handle.get_playerlist()
                playertemplate = {'name': t.name,
                                  'id': t.id,
                                  'stats': defaultStats,
                                  'inv': [None] * 10}
                handle.add_playerlist(t.id, playertemplate)
                rm += "! Added " + t.name

    elif param[0] == "item":
        if param[1] == "add":
            if param[2] == "self":
                target = message.author.id
            else:
                target = param[2]
            playerlist = handle.get_playerlist()
            items = handle.return_itemlist()
            itemName = param[3].replace("_", " ")
            gItem = items[itemName]
            newItem = handle3.Item(gItem)
            targetP = playerlist[target]
            sts, cm = targetP.add_item(newItem)
            rm += "! Added " + newItem.name + " to " + targetP.name
            rm += "\n" + cm
            
    elif param[0] == "room":
        rooms = handle.rooms
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

def alias():
    return ['sudo']
