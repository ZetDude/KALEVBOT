import importlib.machinery

loader = importlib.machinery.SourceFileLoader('maincore', 'C:/Users/Administrator/Desktop/KALEVBOT/maincore.py')
handle = loader.load_module('maincore')

def run(message, prefix, alias):
    helptext = handle.get_helptext()
    return "m", [message.channel, helptext]

def help_use():
    return "Post all the commands in chat, but watch out, it takes up a lot of room in chat"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "chathelp"

def help_perms():
    return 3

def help_list():
    return "Post the help in chat"


def alias():
    return ['chathelp', 'chelp', 'ch', 'chath']
    
