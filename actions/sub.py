import importlib.machinery

loader = importlib.machinery.SourceFileLoader('basic', 'C:/Users/Administrator/Desktop/KALEVBOT/basic.py')
handle = loader.load_module('basic')

def run(message, rpgPrefix, alias):
    return "m", [message.channel, handle.sub(message.author, True)]

def help_use():
    return "Subscribe to the RPG announcement notify list"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "sub"

def help_perms():
    return 0

def help_list():
    return "Subscribe to the RPG announcement notify list"

def alias():
    return ['sub']
