"""
import os
import sys

import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
help_info = {"use": "Modify the permissions of another user",
             "param": "{}about",
             "perms": None,
             "list": "Learn more about the bot"}
alias_list = ['about', 'info']

def run(message, prefix, aliasName):
    cmdlen = len(prefix + aliasName)
    opstring = message.content[cmdlen:].strip()
    spaceloc = opstring.find(" ")
    if spaceloc == -1:
        precalc = opstring.strip()
        postcalcu = message.author
    else:
        precalc = opstring[:spaceloc].strip()
        if len(message.mentions) == 1:
            mentiont = message.mentions[0]
            postcalcu = mentiont
        else:
            postcalcu = core.userget(opstring[spaceloc:].strip(), message.guild.id)

    targetPerms = int(precalc)
    authorPerms = core.perm_get(message.author.id)
    userPerms = core.perm_get(postcalcu.id)
    if authorPerms == 10:
        core.perm_add(targetPerms, postcalcu.id)
        return "m", [message.channel, "Set the permission level for " + postcalcu.name + " to " + core.perm_name(targetPerms) + " (" + str(targetPerms) + ")"]
    elif userPerms > authorPerms:
        return "m", [message.channel, "You cannot set perms of people with higher permission. You have " + core.perm_name(authorPerms) + " (" + str(authorPerms) + ") but your target has " + core.perm_name(userPerms) + " (" + str(userPerms) + ")"]
    elif targetPerms > authorPerms:
        return "m", [message.channel, "You cannot set perms higher than your current one. You have " + core.perm_name(authorPerms) + " (" + str(authorPerms) + ") but you tried setting it to " + core.perm_name(targetPerms) + " (" + str(targetPerms) + ")"]
    else:
        core.perm_add(targetPerms, postcalcu.id)
        return "m", [message.channel, "Set the permission level for " + postcalcu.name + " to " + core.perm_name(targetPerms) + " (" + str(targetPerms) + ")"]


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

def aliasName():
    return ['addperms', 'permsadd', 'addpermissions']
"""
