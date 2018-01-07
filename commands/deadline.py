import datetime
import importlib.machinery
import os
import sys
import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('relaytimegeneratorbot', sp + '/relaytimegeneratorbot.py')
rbot = loader.load_module('relaytimegeneratorbot')

def run(message, prefix, aliasName):
    del prefix
    del aliasName
    f = open(sp + '/deadline.txt', "r")
    deadline = f.readlines(0)[0]
    try:
        deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        core.send(message.channel, '[RELAY OVER]')
    deadline = rbot.deadline_format(deadline)
    core.send(message.channel, deadline)

def help_use():
    return "Display the relay deadine"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "deadline"

def help_perms():
    return 0

def help_list():
    return "Display the relay deadine"

def aliasName():
    return ['deadline', 'relay']
