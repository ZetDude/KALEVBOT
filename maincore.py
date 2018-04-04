"""This file manages normal k! commands, provides functions for commands to use,
and distributes needed actions to needed command files"""

# pylint: disable=no-member
# pylint: disable=global-statement

import datetime
from timeit import default_timer as timer
import os
import sys
import ctypes
import platform
import importlib
import asyncio
from lib import obot
from lib import sender
from lib import logger

prefix = obot.bot_prefix #prefix used for command
game = obot.game #game that appears on the right
c = 0
perms = [[], [], [], [], [], [], [], [], [], []]

start = timer()

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

###Print when discord bot initializes
def ready(client):
    global alias

    global module_names
    global commands
    commands = {}

    f = []
    for (dirpath, dirnames, filenames) in os.walk(sp + '/commands'):
        del dirpath
        del dirnames
        f.extend(filenames)
        break

    py_files = filter(lambda x: os.path.splitext(x)[1] == '.py', f)
    module_names = list(map(lambda x: os.path.splitext(x)[0], py_files))

    for m in module_names:
        commands[m] = importlib.import_module('commands.' + m)

    cache_help()
    alias = {}
    for n in module_names:
        for m in commands[n].alias_list:
            alias[m] = n


    global cl
    readytext = """
Success! The bot is online!
Running from {}
My name is {}
My ID is {}
My prefix is {}
My owner is {}
I am present in {} guilds""".format(sp, client.user.name, client.user.id, prefix, obot.owner_id, len(client.guilds))
    readytext += ", ".join([i.name for i in client.guilds])
    readytext += """
I appear to be playing {}

{} BOT commands loaded under {} aliases""".format(game, str(len(commands)), str(len(alias)))
    print(readytext)
    logger.log(readytext)
    cl = client

def get_timer():
    sub = timer()
    difference = (sub - start)
    difference = str(datetime.timedelta(seconds=difference))
    return difference

def get_free_space_mb(dirname):
    """Return folder/drive free space (in megabytes)."""
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    st = os.statvfs(dirname)
    return st.f_bavail * st.f_frsize

###Identify username
def userget(cstring, targetID=327495595235213312):
    conguild = cl.get_guild(targetID)
    finaluser = conguild.get_member_named(cstring)
    if finaluser is None:
        return conguild.get_member(cstring)
    return None

def send(channel, message, starting="", ending=""):
    return sender.send(channel, message, cl, starting, ending)

def spam(channel, message, amount, starting="", ending=""):
    for i in range(int(amount)):
        del i
        sender.send(channel, message, cl, starting, ending)

def cache_help():
    global helptext
    clist = commands.keys()
    ft = ""
    ftn = ""
    found = False
    for i in permissions():
        found = False
        ftn = ""
        for y in clist:
            try:
                if i in commands[y].help_info["perms"]:
                    part1 = prefix + y
                    part2 = commands[y].help_info["list"]
                    ftn = ftn + part1 + " :: " + part2 + "\n"
                    found = True
            except:
                if i is None and commands[y].help_info["perms"] is None:
                    part1 = prefix + y
                    part2 = commands[y].help_info["list"]
                    ftn = ftn + part1 + " :: " + part2 + "\n"
                    found = True
        if found:
            if i is None:
                ft += "== THE FOLLOWING COMMANDS DON'T NEED ANY PERMISSIONS ==\n" + ftn
            else:
                ft += "== THE FOLLOWING COMMANDS NEED THE PERMISSION " + i.upper() + " ==\n" + ftn
        else:
            ft = ft + ftn


    ft = "```asciidoc\n" + ft + "\n```"
    helptext = ft

def perm_name(num):
    permdict = {0: "NONE",
    1: "ELEVATED",
    2: "INFLUENCIAL",
    3: "POWERFUL",
    4: "HIGHLY POWERFUL",
    5: "OVERPOWERED",
    6: "ASCENDED",
    7: "HEAVENLY",
    8: "GODLY",
    9: "OVER-DIVINE",
    10: "ALMIGHTY"}
    return permdict.get(num, "INVALID PERMISSION")

def permissions():
    return [None,
    "message",
    "relay",
    "rpg",
    "admin",
    "owner"]

def perm_get(userid):
    for i in range(10):
        if userid in perms[i]:
            return i+1
    return 0

###compose help for a specific command
def compose_help(cSearch):
    cSearch = alias.get(cSearch, None)
    if cSearch is None:
        return "```diff`\n- No such command -\n```"
    commandObject = commands[cSearch]
    cmd_info = commandObject.help_info
    usage1 = ":: Usage ::\n"
    usage2 = "= " + cmd_info["param"].format(prefix) + "\n"
    usage3 = cmd_info["use"] + "\n"
    part4 = str(cmd_info["perms"])
    usage4 = "= You need the " + part4.upper() + " permission to run this command\n"
    part5 = commandObject.alias_list
    usage5 = "= Aliases: " + ", ".join(part5)
    return "```asciidoc\n" + usage1 + usage2 + usage3 + usage4 + usage5 + "\n```"

#####highest definition
@asyncio.coroutine
def main(message):
    cmdpart = "help"
    spaceloc = message.content.find(" ")
    if spaceloc == -1:
        cmdpart = message.content
    else:
        cmdpart = message.content[:spaceloc].strip()
    rprefix = len(prefix)
    cmdpart = cmdpart[rprefix:].lower()
    if cmdpart in alias:
        cmdoriginal = cmdpart
        cmdpart = alias[cmdpart]
        runPerms = commands[cmdpart].help_info['perms']
        userPerms = perm_get(message.author.id)
        # TODO: Fix this section when new permision system is implemented. This is temporary
        if message.author.id == obot.owner_id or runPerms is None:
            currentCommand = commands[cmdpart]
            yield from currentCommand.run(message, prefix, cmdoriginal)
        elif runPerms is not None:
            yield from message.channel.send("Oops! You do not have the permissions to run this command. You need " + perm_name(runPerms) + " (" + str(runPerms) + ") or better. You have " + perm_name(userPerms) + " (" + str(userPerms) + ")")
