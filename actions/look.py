import importlib.machinery

loader = importlib.machinery.SourceFileLoader('basic', 'C:/Users/Administrator/Desktop/KALEVBOT/basic.py')
handle = loader.load_module('basic')

def run(message, rpgPrefix, alias):
    roomlist = handle.rooms
    playerlist = handle.playerlist
    selfClass = playerlist[message.author.id]
    sNow = selfClass.stats['location']
    ident = roomlist[sNow].get_desc()

    bothMSG = "You are in room " + str(sNow)
    publicMSG = message.author.mention + ", \n```diff\n" + bothMSG + "\n```"
    privateMSG = "```diff\n" + bothMSG + "\n" + ident + "\n```"
    return "p", [message.author, privateMSG, message.channel, publicMSG]

def help_use():
    return "Look at what the current room you are in looks like"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "look"

def help_perms():
    return 0

def help_list():
    return "Look at the current room"

def alias():
    return ['look']
