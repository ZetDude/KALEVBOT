import importlib.machinery

loader = importlib.machinery.SourceFileLoader('maincore', 'C:/Users/Administrator/Desktop/KALEVBOT/maincore.py')
handle = loader.load_module('maincore')

def run(message, prefix, alias):
    ships = message.mentions
    ships = [x for x.mention in ships]
    shipMsg = ' and '.join(ships)
    finalMSG = message.author.mention + " totally ships " + shipMSG

def help_use():
    return "PM all the commands to the user or show more specific help about a single command"

def help_param():
    return "<COMMAND>: Optional. The command to get more specific infomation about. When not given, PM all the commands instead"

def help_cmd(prefix):
    return prefix + "help <COMMAND>"

def help_perms():
    return 0

def help_list():
    return "Get all the help or help about a specific command"

def alias():
    return ['help', 'halp', 'h', 'commands', 'command']