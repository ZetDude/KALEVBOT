#####IMPORTS GO HERE

from easyread import * #module for reading/writing files easier
import relaytimegeneratorbot as rbot #module for calculating time based stuff
import datetime
import pytz
from timeit import default_timer as timer
import os
import sys
import ctypes
import platform
import importlib
import obot
from os import walk
import obot


#####IMPORTS END HERE

#####Load code

perms = [[""], [""], [""], [""], [""], [""], [""], [""], [""], [""]]
<<<<<<< HEAD
prefix = obot.botPrefix #prefix used for command
=======
prefix = obot.prefix #prefix used for command
>>>>>>> 6362246b8c9e4940784ced5d7e2e1a0db4c20293
game = obot.game #game that appears on the right
c = 0
anno = ""
preanno = ""
annosilent = ""

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
    
start = timer()
#####End of load code


#####Main definition code starts here

def get_count():
    try:
        with open('discordCount.txt', 'r') as f:
            count = int(f.readlines(0)[0])
            count += 1
    except:
        print("discordCount.txt didn't exist, creating")
        count = 1
        with open('discordCount.txt', 'w') as f:
            f.write(str(count))
    return count
    
def cache_perms():
    global perms
    perms = [[], [], [], [], [], [], [], [], [], []]
    for n in range(10):
        y = n + 1
        try:
            with open(sp + "/p" + str(y) + ".txt", 'r') as f:
                lines = [line.rstrip('\n') for line in f]
                part = ''
                for i in lines:
                    perms[n].append(i)
        except:
            continue
        
def return_perms():
    return perms

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
    else:
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
def userget(cstring):
    conserver = cl.get_server("327495595235213312")
    cstring = cstring
    finaluser = conserver.get_member_named(cstring)
    if finaluser == None:
        try:
            finaluser = conserver.get_member(cstring)
            return finaluser
        except:
            return None
    else:
        return finaluser

def get_anno():
    return preanno, anno, annosilent

###Print when discord bot initializes
def ready(client):
    global alias

    cache_perms()
    cache_help()
    
    global cl
    print("")
    print("Success! The bot is online!")
    print("Running from " + sp)
    print("My name is " + client.user.name)
    print("My ID is " + client.user.id)
    print("My prefix is " + prefix)
    print("I am present in " + str(len(client.servers)) + " servers.")
    for i in client.servers:
        print(i.name, end=", ")
    print("")
    print("I appear to be playing " + game)
    print("")
    print(str(len(commands)) + " BOT commands loaded")
    cl = client
    
    for n in module_names:
        for m in commands[n].alias():
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
    

###Check if message sent was from PM
def check_if_pm(message):
    if message.server == None:
        return True
    else:
        return False

###Check if message is NOT a PM
def npm(message):
    if message.server == None:
        return False
    else:
        return True

###Crash this scipt
def crash():
    sys.exit()

###Return all channels in the conlang channel
def conlang_channels():
    server = cl.get_server("327495595235213312")
    servers = []
    for y in server.channels:
        servers.append(y)
    return servers

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
            if commands[y].help_perms() == i:
                part1 = commands[y].help_cmd(prefix)
                part2 = commands[y].help_list()
                ftn = ftn + part1 + " :: " + part2 + "\n"
                found = True
        if found:
            above = " OR ABOVE ==\n"
            if i == 10:
                above = " ==\n"
            ft = ft + "== THE FOLLOWING COMMANDS NEED PERMISSION LEVEL " + str(i) + above + ftn
        else:
            ft = ft + ftn
                

    ft = "```asciidoc\n" + ft + "\n```"
    helptext = ft
            
        

def perm_name(num):
    if num == 0:
        return "NONE"
    elif num == 1:
        return "ELEVATED"
    elif num == 2:
        return "INFLUENCIAL"
    elif num == 3:
        return "POWERFUL"
    elif num == 4:
        return "HIGHLY POWERFUL"
    elif num == 5:
        return "OVERPOWERED"
    elif num == 6:
        return "ASCENDED"
    elif num == 7:
        return "HEAVENLY"
    elif num == 8:
        return "GODLY"
    elif num == 9:
        return "OVER-DIVINE"
    elif num == 10:
        return "ALMIGHTY"

def perm_get(userid):
    for i in range(10):
        if userid in perms[i]:
            return i+1
    return 0

###compose help for a specific command
def compose_help(cSearch):
    usage1 = "Usage:\n"
    usage2 = commands[cSearch].help_cmd(prefix) + "\n"
    usage3 = commands[cSearch].help_use() + "\n"
    paramGet = commands[cSearch].help_param()
    if paramGet == None:
        usage4 = "No parameters required\n"
    else:
        usage4 = paramGet + "\n"
    part5 = perm_name(commands[cSearch].help_perms())
    part6 = str(commands[cSearch].help_perms())
    usage5 = "You need the " + part5 + " (" + part6 + ") permission level or better to run this command"
    return "```\n" + usage1 + usage2 + usage3 + usage4 + usage5 + "\n```"

###Google, urban and others in one megacommand
def clink(message, cmd, pre, post, rep):
    cmdlen = len(prefix + cmd)
    opstring = message.content[cmdlen:].strip().replace('+', '%2B').replace(' ', rep)
    return message.channel, pre + opstring + post

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
    return message.channel, pre + precalc + mid + postcalc + post




#####highest definition

def main(message):
    toreturn = False
    cmdpart = "help"
    spaceloc = message.content.find(" ")
    if spaceloc == -1:
        cmdpart = message.content
    elif message.content == prefix:
        cmdpart = "help"
    else:
        cmdpart = message.content[:spaceloc].strip()
    rprefix = len(prefix)
    cmdpart = cmdpart[rprefix:].lower()
    if cmdpart in alias:
        cmdoriginal = cmdpart
        cmdpart = alias[cmdpart]
        runPerms = commands[cmdpart].help_perms()
        userPerms = perm_get(message.author.id)
        if userPerms >= runPerms:
            toreturn = commands[cmdpart].run(message, prefix, cmdoriginal)
        else:
            toreturn = "m", [message.channel, "Oops! You do not have the permissions to run this command. You need " + perm_name(runPerms) + " (" + str(runPerms) + ") or better. You have " + perm_name(userPerms) + " (" + str(userPerms) + ")"]
            

        return toreturn
    else:
        return "m", [message.channel, "Command not found"]
