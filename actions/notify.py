import importlib.machinery

loader = importlib.machinery.SourceFileLoader('basic', 'C:/Users/Administrator/Desktop/KALEVBOT/basic.py')
handle = loader.load_module('basic')

def run(message, rpgPrefix, alias):
    return "m", [message.channel, handle.ping()]

def help_use():
    return "Ping the users subscribed to the RPG announcement notify list."

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "notify"

def help_perms():
    return 7

def help_list():
    return "Ping the users subscribed to the RPG announcement notify list"

def alias():
    return ['notify']
