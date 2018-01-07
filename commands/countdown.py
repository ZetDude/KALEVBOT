import importlib.machinery
import datetime
import os
import sys
import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
loader = importlib.machinery.SourceFileLoader('relaytimegeneratorbot', sp + '/relaytimegeneratorbot.py')
rbot = loader.load_module('relaytimegeneratorbot')

def run(message, prefix, aliasName):
    del prefix
    del aliasName
    f = open(sp + "/deadline.txt", "r")
    deadline = f.readlines(0)[0]
    try:
        deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        core.send(message.channel, '[RELAY OVER]')
    #get the actual datetime object from the formatted text in the file
    countdown = rbot.time_remain_string(deadline) + " remaining"
    #format the text using rbot
    core.send(message.channel, countdown)

def help_use():
    return "Display the time remaining until the relay deadline"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "countdown"

def help_perms():
    return 0

def help_list():
    return "Display the time remaining until the relay deadline"

def aliasName():
    return ['countdown', 'remaining']
