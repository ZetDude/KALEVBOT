import maincore as core
#import os
#import sys
#sp = os.path.dirname(os.path.realpath(sys.argv[0]))
#corefile = sp + '/maincore.py'
#sys.path.append(os.path.dirname(os.path.expanduser(corefile)))


#loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
#core = loader.load_module('maincore')
#import sp + '/maincore.py'

def run(message, prefix, alias):
    if message.content.strip().lower() == (prefix + alias).lower():
        helptext = core.get_helptext()
        core.send(message.author, helptext)
        core.send(message.channel, "Alright " + message.author.mention + ", check your DMs")
        return
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()
    helptext = "something bad happened"
    helptext = core.compose_help(opstring)
    core.send(message.channel, helptext)

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
