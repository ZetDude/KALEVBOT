import importlib.machinery

loader = importlib.machinery.SourceFileLoader('maincore', 'C:/Users/karlk/Desktop/KALEVBOT/maincore.py')
handle = loader.load_module('maincore')

def run(message, prefix):
    helptext = handle.get_helptext()
    if message.content.strip() == prefix + "help":
        return "m", [message.author, helptext]
    else:
        cmdlen = len(prefix + "help")
        opstring = message.content[cmdlen:].strip()
        helptexta = "something bad happened"
        helptexta = handle.compose_help(opstring)
        return "m", [message.channel, helptexta]

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
