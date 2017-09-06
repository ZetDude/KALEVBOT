import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '\\maincore.py')
handle = loader.load_module('maincore')

def run(message, prefix, alias):
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()
    spaceloc = opstring.find(" ")
    if spaceloc == -1:
        precalc = opstring.strip()
        postcalc = message.author
    else:
        precalc = opstring[:spaceloc].strip()
        if len(message.mentions) == 1:
            mentiont = message.mentions[0]
            postcalcu = mentiont
        else:
            postcalcu = handle.userget(opstring[spaceloc:].strip())

    targetPerms = int(precalc)
    authorPerms = handle.perm_get(message.author.id)
    userPerms = handle.perm_get(postcalcu.id)
    if authorPerms == 10:
        handle.perm_add(targetPerms, postcalcu.id)
        return "m", [message.channel, "Set the permission level for " + postcalcu.name + " to " + handle.perm_name(targetPerms) + " (" + str(targetPerms) + ")"]
    elif userPerms > authorPerms:
        return "m", [message.channel, "You cannot set perms of people with higher permission. You have " + handle.perm_name(authorPerms) + " (" + str(authorPerms) + ") but your target has " + handle.perm_name(userPerms) + " (" + str(userPerms) + ")"]
    elif targetPerms > authorPerms:
        return "m", [message.channel, "You cannot set perms higher than your current one. You have " + handle.perm_name(authorPerms) + " (" + str(authorPerms) + ") but you tried setting it to " + handle.perm_name(targetPerms) + " (" + str(targetPerms) + ")"]
    else:
        handle.perm_add(targetPerms, postcalcu.id)
        return "m", [message.channel, "Set the permission level for " + postcalcu.name + " to " + handle.perm_name(targetPerms) + " (" + str(targetPerms) + ")"]
    

def help_use():
    return "Modify the permissions of another user"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "addperms"

def help_perms():
    return 8

def help_list():
    return "Modify the permissions of another user"

def alias():
    return ['addperms', 'permsadd', 'addpermissions']
