import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, alias):
    core.cache_perms()
    if message.content.strip() == prefix + alias:
        userPerms = core.perm_get(message.author.id)
        combine = "You have " + core.perm_name(userPerms) + " (" + str(userPerms) + ")"
    else:
        if len(message.mentions) == 1:
            mentiont = message.mentions[0]
            userPerms = core.perm_get(mentiont.id)
            combine = mentiont.name + " has " + core.perm_name(userPerms) + " (" + str(userPerms) + ")"
        else:
            cmdlen = len(prefix + alias)
            opstring = message.content[cmdlen:].strip()
            if opstring == "all":
                combine = str(core.return_perms())
            else:
                gotuser = core.userget(opstring, message.guild.id)
                if gotuser is None:
                    combine = "Something failed"
                else:
                    userPerms = core.perm_get(gotuser.id)
                    combine = gotuser.name + " has " + core.perm_name(userPerms) + " (" + str(userPerms) + ")"

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
