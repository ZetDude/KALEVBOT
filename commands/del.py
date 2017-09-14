import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

def run(message, prefix, alias):
    commandLength = len(prefix + alias)
    operatableString = message.content[commandLength:].strip()
    deleteAmount = 0
    try:
        deleteAmount = int(operatableString)
        return "d", deleteAmount
    except:
        return "m", [message.channel, "Not a Number"]

def help_use():
    return "Delete the amount of messages from the bot as is specified"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "del"

def help_perms():
    return ["MANAGE MESSAGES"]

def help_list():
    return "Delete messages from the bot"

def alias():
    return ['del', 'delete']