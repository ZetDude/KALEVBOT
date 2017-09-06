import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('relaytimegeneratorbot', sp + '\\relaytimegeneratorbot.py')
handle = loader.load_module('relaytimegeneratorbot')

def run(message, prefix, alias):
    newdeadline = handle.deadline_time()
    deadline = handle.deadline_format(newdeadline)
    f = open("C:/Users/Administrator/Desktop/KALEVBOT/deadline.txt", "w")
    f.write(str(newdeadline))
    return "m", [message.channel, deadline]

def help_use():
    return "Generate a new relay deadline and overwrite the old one"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "new"

def help_perms():
    return 4

def help_list():
    return "Generate a new relay deadline and overwrite the old one"

def alias():
    return ['new', 'newdeadline']