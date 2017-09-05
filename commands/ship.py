import importlib.machinery

loader = importlib.machinery.SourceFileLoader('maincore', 'C:/Users/Administrator/Desktop/KALEVBOT/maincore.py')
handle = loader.load_module('maincore')

def run(message, prefix, alias):
    ships = message.mentions    
    seen = set()
    seen_add = seen.add
    ships = [x for x in ships if not (x in seen or seen_add(x))]
    if len(ships) == 0:
        return "m", [message.channel, message.author.mention + ", how does one ship nobody? Mention at least two people in the message"]
    elif len(ships) == 1:
        return "m", [message.channel, message.author.mention + ", they arent that lonely. Mention at least two people in the message"]
    ships = [x.mention for x in ships]
    shipMsg = ' and '.join(ships)
    finalMSG = message.author.mention + " totally ships " + shipMsg
    return "m", [message.channel, finalMSG] 

def help_use():
    return "Ship someone with someone else"

def help_param():
    return "<MENTION>: The mention for the users you want to ship"

def help_cmd(prefix):
    return prefix + "help <MENTION1> <MENTION2>"

def help_perms():
    return 0

def help_list():
    return "Ship someone with someone else uwu"

def alias():
    return ['ship']