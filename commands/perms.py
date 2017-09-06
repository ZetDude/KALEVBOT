import datetime
import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
from random import randint

loader = importlib.machinery.SourceFileLoader('maincore', sp + '\\maincore.py')
handle = loader.load_module('maincore')

def run(message, prefix, alias):
    handle.cache_perms()
    if message.content.strip() == prefix + alias:
        userPerms = handle.perm_get(message.author.id)
        combine = "You have " + handle.perm_name(userPerms) + " (" + str(userPerms) + ")"
    else:
        if len(message.mentions) == 1:
            mentiont = message.mentions[0]
            userPerms = handle.perm_get(mentiont.id)
            combine = mentiont.name + " has " + handle.perm_name(userPerms) + " (" + str(userPerms) + ")"
        else:
            cmdlen = len(prefix + alias)
            opstring = message.content[cmdlen:].strip()
            if opstring == "all":
                combine = str(handle.return_perms())
            else:
                gotuser = handle.userget(opstring)
                if gotuser == None:
                    combine = "Something failed"
                else:
                    userPerms = handle.perm_get(gotuser.id)
                    combine = gotuser.name + " has " + handle.perm_name(userPerms) + " (" + str(userPerms) + ")"
            
    return "m", [message.channel, combine]

def help_use():
    return "Show your permission level and name"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "perms"

def help_perms():
    return 0

def help_list():
    return "Show your permission level"

def alias():
    return ['perms', 'perm', 'permissions', 'permission']