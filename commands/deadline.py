import datetime
import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('relaytimegeneratorbot', sp + '/relaytimegeneratorbot.py')
rbot = loader.load_module('relaytimegeneratorbot')
loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader2.load_module('maincore')

def run(message, prefix, aliasName):

    f = open(sp + '/deadline.txt', "r")
    deadline = f.readlines(0)[0]
    try:
        deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S.%f")
    except:
        return "m", [message.channel, '[RELAY OVER]']
    #get the actual datetime object from the formatted text in the file
    deadline = rbot.deadline_format(deadline)
    #format the text using rbot
    return "m", [message.channel, deadline]

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
