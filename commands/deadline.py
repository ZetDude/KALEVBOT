import datetime
import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('relaytimegeneratorbot', sp + '\\relaytimegeneratorbot.py')
handle = loader.load_module('relaytimegeneratorbot')

def run(message, prefix, alias):

    f = open("C:/Users/Administrator/Desktop/KALEVBOT/deadline.txt", "r") 
    deadline = f.readlines(0)[0]
    try:
        deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S.%f")
    except:
        return "m", [message.channel, '[RELAY OVER]']
    #get the actual datetime object from the formatted text in the file
    deadline = handle.deadline_format(deadline)
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

def alias():
    return ['deadline', 'relay']