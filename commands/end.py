import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

def run(message, prefix, alias):
    newdeadline = "END"
    deadline = "The relay has ended. I hope everyone had fun!"
    f = open(sp + '/deadline.txt', "w")
    f.write(str(newdeadline))
    return "m", [message.channel, deadline]

def help_use():
    return "Mark the relay as ended"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "end"

def help_perms():
    return ["RELAY MANAGER"]

def help_list():
    return "Mark the relay as ended"

def alias():
    return ['end', 'endrelay']