"""This file manages normal k! commands, provides functions for commands to use,
and distributes needed actions to needed command files"""

# pylint: disable=no-member

import datetime
from timeit import default_timer as timer
import os
import sys
import ctypes
import platform
import importlib
import asyncio
import obot
import sender

prefix = obot.botPrefix #prefix used for command
game = obot.game #game that appears on the right
c = 0
perms = [[], [], [], [], [], [], [], [], [], []]

start = timer()

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

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

def perm_add(level, userid):
    cache_perms()
    for m in range(10):
        xa = [x for x in perms[m] if x != userid]
        perms[m] = xa
    if int(level) != 0:
        perms[int(level)-1].append(userid)
    for n in range(10):
        y = n + 1
        with open("p" + str(y) + ".txt", 'w') as f:
            for s in perms[n]:
                f.write(str(s) + "\n")
        f.close()

###Identify username
def userget(cstring, targetID=327495595235213312):
    conguild = cl.get_guild(targetID)
    finaluser = conguild.get_member_named(cstring)
    if finaluser is None:
        try:
            finaluser = conguild.get_member(cstring)
            return finaluser
        except:
            return None
    else:
        return finaluser

###Print when discord bot initializes
def ready(client, driveClient):
    global alias

    global module_names
    global commands

    f = []
    sp = os.path.dirname(os.path.realpath(sys.argv[0]))
    for (dirpath, dirnames, filenames) in os.walk(sp + '/commands'):
        f.extend(filenames)
        break


    alias = {}

    py_files = filter(lambda x: os.path.splitext(x)[1] == '.py', f)
    module_names = list(map(lambda x: os.path.splitext(x)[0], py_files))

    commands = {}
    for m in module_names:
        commands[m] = importlib.import_module('commands.' + m)

    cache_perms()
    cache_help()

    global cl
    global drive
    print("")
    print("Success! The bot is online!")
    print("Running from " + sp)
    print("My name is " + client.user.name)
    print("My ID is {}".format(client.user.id))
    print("My prefix is " + prefix)
    print("I am present in " + str(len(client.guilds)) + " guilds.")
    for i in client.guilds:
        print(i.name, end=", ")
    print("")
    print("I appear to be playing " + game)
    print("")
    print(str(len(commands)) + " BOT commands loaded")
    cl = client
    drive = driveClient

    for n in module_names:
        for m in commands[n].aliasName():
            alias[m] = n

###Fetch the game the bot is "playing"
def fetch_game():
    return game

###Get the message and check if it has the prefix at the start
def check_if_prefix(message):
    if message.content.startswith(prefix):
        return True
    else:
        return False

def send(channel, message, start="", end=""):
    return sender.send(channel, message, cl, start, end)

def spam(channel, message, amount, start="", end=""):
    for i in range(int(amount)):
        sender.send(channel, message, cl, start, end)

###Reload all commands
def reload_cmd():
    global commands

    cache_help()

    f = []
    for (dirpath, dirnames, filenames) in os.walk('./commands'):
        f.extend(filenames)
        break

    py_files = filter(lambda x: os.path.splitext(x)[1] == '.py', f)
    module_names = list(map(lambda x: os.path.splitext(x)[0], py_files))

    commands = {}
    for m in module_names:
        commands[m] = importlib.import_module('commands.' + m)
    return "Reloaded help commands list\nReloaded: " + str(module_names)

###fetch helptext
def get_helptext():
    return helptext

def cache_help():
    global helptext
    clist = commands.keys()
    ft = ""
    ftn = ""
    found = False
    for i in range(11):
        found = False
        ftn = ""
        for y in clist:
            try:
                if commands[y].help_perms()[0] == i:
                    part1 = commands[y].help_cmd(prefix)
                    part2 = commands[y].help_list()
                    ftn = ftn + part1 + " :: " + part2 + "\n"
                    found = True
            except:
                if i == 0 and commands[y].help_perms() == 0:
                    part1 = commands[y].help_cmd(prefix)
                    part2 = commands[y].help_list()
                    ftn = ftn + part1 + " :: " + part2 + "\n"
                    found = True
        if found:
            if i == 0:
                ft += "== THE FOLLOWING COMMANDS DON'T NEED ANY PERMISSIONS ==\n" + ftn
            else:
                ft += "== THE FOLLOWING COMMANDS NEED THE PERMISSION LEVEL" + str(i) + " ==\n" + ftn
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
    permlist = [0,
    "MANAGE MESSAGES",
    "RPG DEVELOPER",
    "RELAY MANAGER",
    "RPG MANAGER",
    "ADMIN",
    "OWNER",]
    return permlist

def perm_get(userid):
    for i in range(10):
        if userid in perms[i]:
            return i+1
    return 0

###compose help for a specific command
def compose_help(cSearch):
    print(cSearch)
    cSearch = alias.get(cSearch, None)
    print(cSearch)
    if cSearch is None:
        return "```diff`\n- No such command -\n```"
    commandObject = commands[cSearch]
    usage1 = ":: Usage ::\n"
    usage2 = "= " + commandObject.help_cmd(prefix) + "\n"
    usage3 = commandObject.help_use() + "\n"
    paramGet = commandObject.help_param()
    if paramGet is None:
        usage4 = "No parameters required\n"
    else:
        usage4 = paramGet + "\n"
    part5 = perm_name(commandObject.help_perms())
    part6 = str(commandObject.help_perms())
    usage5 = "= You need the " + part5 + " (" + part6 + ") permission level or better to run this command\n"
    part7 = commandObject.aliasName()
    usage6 = "= Aliases: " + ", ".join(part7)
    return "```asciidoc\n" + usage1 + usage2 + usage3 + usage4 + usage5 + usage6 + "\n```"

###Google, urban and others in one megacommand
def clink(message, cmd, pre, post, rep):
    cmdlen = len(prefix + cmd)
    opstring = message.content[cmdlen:].strip().replace('+', '%2B').replace(' ', rep)
    return pre + opstring + post

###Wiki, wikti and others in one megacommand
def cwiki(message, cmd, pre, mid, post, rep):
    cmdlen = len(prefix + cmd)
    opstring = message.content[cmdlen:].strip()
    spaceloc = opstring.find(" ")
    if spaceloc == -1:
        precalc = "en"
        postcalc = opstring.strip()
    else:
        precalc = opstring[:spaceloc].strip()
        postcalc = opstring[spaceloc:].strip().replace(' ', rep)
    return pre + precalc + mid + postcalc + post




#####highest definition
@asyncio.coroutine
def main(message):
    toreturn = False
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
        runPerms = commands[cmdpart].help_perms()
        userPerms = perm_get(message.author.id)
        if userPerms >= runPerms or message.author.id == obot.ownerID:
            currentCommand = commands[cmdpart]
            yield from currentCommand.run(message, prefix, cmdoriginal)
        else:
            yield from message.channel.send("Oops! You do not have the permissions to run this command. You need " + perm_name(runPerms) + " (" + str(runPerms) + ") or better. You have " + perm_name(userPerms) + " (" + str(userPerms) + ")")


        return toreturn
