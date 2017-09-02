import importlib.machinery

loader = importlib.machinery.SourceFileLoader('basic', 'C:/Users/Administrator/Desktop/KALEVBOT/basic.py')
handle = loader.load_module('basic')

def run(message, prefix, alias):
    helptext = handle.get_helptext()
    if message.content.strip() == prefix + "help":
        return "m", [message.channel, helptext]
    else:
        cmdlen = len(prefix + alias)
        opstring = message.content[cmdlen:].strip()
        helptexta = "something bad happened"
        helptexta = handle.compose_help(opstring)
        return "m", [message.channel, helptexta]

def help_use():
    return "Post all the commands in chat or show more specific help about a single command"

def help_param():
    return "<COMMAND>: Optional. The command to get more specific infomation about. When not given, display all the commands instead"

def help_cmd(prefix):
    return prefix + "help <COMMAND>"

def help_perms():
    return 0

def help_list():
    return "Get all the help or help about a specific command"

def alias():
    return ['help']
