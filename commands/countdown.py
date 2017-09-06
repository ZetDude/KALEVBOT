import datetime
import importlib.machineryimport importlib.machinery
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
    countdown = handle.time_remain_string(deadline) + " remaining"
    #format the text using rbot
    return "m", [message.channel, countdown]

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


def alias():
    return ['countdown', 'remaining']