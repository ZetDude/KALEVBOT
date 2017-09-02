#####IMPORTS GO HERE

import whitelists as wl #Lists like the authorized user list
from easyread import * #module for reading/writing files easier
import relaytimegeneratorbot as rbot #module for calculating time based stuff
import datetime
import pytz
from timeit import default_timer as timer
import os
import sys
import ctypes
import platform
import commands
import importlib
from os import walk


#####IMPORTS END HERE

#####Load code

perms = [[""], [""], [""], [""], [""], [""], [""], [""], [""], [""]]
prefix = "k!" #prefix used for command
game = "bot is broken" #game that appears on the right
c = 0
helptext = """```
type k!help <command> for more info about a specific command
k!countdown    = The days, hours and minutes until the relay deadline
k!pass         = Check who has the relay torch and who gets it next
k!deadline     = See the current relay deadline
k!time in      = See the current time in that timezone
k!help         = Get the help. You did it!
k!status       = Test if the bot is *still alive*
k!identify get = Gets the identification of the user. Defaults to message sender
k!identify add = Add something to that user's identification. Defaults to message sender.
k!google       = Google the search string
k!urban        = Urban dictionary lookup the seach string
k!night        = Wish a good night to the user. Defaults to user sender
k!wiki         = Wikipedia lookup the page in the specified language
k!wikti        = Wiktionary lookup the page in the specified language
k!dev          = best command :sunglasses:
----VVV AUTHORIZED USERS ONLY COMMANDS VVV----
k!new           = Calculate a new relay deadline, overwriting the old one
k!del           = Delete messages sent by bot
k!chathelp      = Post help in chat. Takes up a lot of chat space
k!say           = Say something in a channel.
```"""
anno = ""
preanno = ""
annosilent = ""

f = []
for (dirpath, dirnames, filenames) in os.walk('./commands'):
    f.extend(filenames)
    break

py_files = filter(lambda x: os.path.splitext(x)[1] == '.py', f)
module_names = list(map(lambda x: os.path.splitext(x)[0], py_files))

commands = {}
for m in module_names:
    commands[m] = importlib.import_module('commands.' + m)
    
print("maincore.py was silently loaded in a module")

start = timer()
#####End of load code


#####Main definition code starts here

def cache_perms():
    global perms
    perms = [[], [], [], [], [], [], [], [], [], []]
    for n in range(10):
        y = n + 1
        #print("p" + str(y) + ".txt")
        with open("p" + str(y) + ".txt", 'r') as f:
            lines = [line.rstrip('\n') for line in f]
            #print(lines)
            part = ''
            for i in lines:
                perms[n].append(i)
    #print(perms)

        
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
    print(int(level))
    if int(level) != 0:
        print(str(level) + " != 0")
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
    finaluser = None
    ulist = []
    for y in conserver.members:
        ulist.append(y)
    unamelist = []
    for i in ulist:
        unamelist.append(i.name + "#" + i.discriminator)
    if cstring in unamelist:
        upos = unamelist.index(cstring)
        finaluser = ulist[upos]
        return finaluser
    else:
        try:
            finaluser = conserver.get_member(cstring)
            return finaluser
        except:
            return None

def get_anno():
    return preanno, anno, annosilent

###Print when discord bot initializes
def ready(client):

    for i in commands.values():
        print(i, end="; ")

    cache_perms()
    cache_help()
    
    global cl
    print("Success! The bot is online!")
    print("My name is " + client.user.name)
    print("My ID is " + client.user.id)
    print("I appear to be playing " + game)
    print("")
    cl = client

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
                print(part1)
                print(y)
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
        #print(i)
        #print(perms[i])
        if userid in perms[i]:
            return i+1
    #print("failed")
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



#####Command definitions

    
###Check the time in a time zone
###Import later as either "timein" or "time" with many sub-commands
def cmd_time_in(message):
    mlen = len(prefix + "time in")
    pstring = message.content[mlen:].strip().replace(' ', '_')
    try:
        converted = rbot.format_time(datetime.datetime.now(pytz.timezone(pstring)))
        return message.channel, str(converted)
    except:
        return message.channel, "NonExistentTimeError"
    
###Puprposefully crash the bot
###pretty useless, do not import?
def cmd_stop(message):
    return message.channel, "ITS ME GOODBYE! <https://youtu.be/y_hWeN249fs?t=25s>"

###check who has torch and who is next
def cmd_pass(message):
    fromt = eread("torchFrom.txt")
    tot = eread("torchTo.txt")
    return message.channel, "Currently, " + fromt + " has the torch, and they will pass it to " + tot

###countdown: time remaining
def cmd_countdown(message):
    deadline = eread("deadline.txt") #read the deadline time
    deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S.%f")
    #get the actual datetime object from the formatted text in the file
    countdown = rbot.time_remain_string(deadline) + " Remaining"
    #format the text using rbot
    return message.channel, countdown

###little mod-only command for saying things
def cmd_say(message):
    cmdlen = len(prefix + "say")
    opstring = message.content[cmdlen:].strip()
    #get the string without the command attached to it
    parameters = []
    spaceloc = opstring.find(" ")
    if spaceloc == -1:
        parameters.append("")
        parameters[0] = opstring
    else:
        parameters.append("")
        parameters[0] = opstring[:spaceloc].strip()
        parameters.append("")
        parameters[1] = opstring[spaceloc:].strip()
    #fetch the parameter count
    if len(parameters) == 1:
        return message.channel, opstring
        #if only one parameter, return the string in the same channel
    elif len(parameters) == 2:
        server = cl.get_server("327495595235213312")
        servers = []
        for y in server.channels:
            servers.append(y)
        servernames = []
        for i in servers:
            servernames.append(i.name)
        sstring = parameters[0]
        if sstring in servernames:
            location = servernames.index(sstring)
            serverfinal = servers[location]
            return serverfinal, parameters[1]
        else:
            return message.channel, opstring
    else:
        return message.channel, "Something failed"

def cmd_identify(message):
    cleaned = None
    cmdlen = len(prefix + "identify")
    opstring = message.content[cmdlen:].strip()
    #get the string without the command attached to it
    premsg = ""
    parameters = []
    if len(message.mentions) == 0:
        hashloc = opstring.find("#")
        maxlen = len(prefix + "identify 12345678901234567890123456789012")
        if hashloc == -1 or hashloc > maxlen:
            parameters.append("")
            spaceloc = opstring.find(" ")
            cleaned = opstring[:spaceloc]
            ftype = opstring[spaceloc:spaceloc+4].strip()
            ftypeend = opstring[spaceloc+4:]
            
        else:
            parameters.append("")
            parameters[0] = opstring[:hashloc].strip()
            parameters.append("")
            parameters[1] = opstring[hashloc:hashloc+5].strip()
            cleaned = parameters[0] + parameters[1]
            ftype = opstring[hashloc+5:hashloc+9].strip()
            ftypeend = opstring[hashloc+9:]
            
        cleaned = cleaned.strip()
        fetched = userget(cleaned)
        premsg = ""
        if fetched == None:
            print("Incorrect name, defaulting")
            fetched = message.author
            premsg = ""
            ftypeend = opstring[3:].strip()
            ftype = opstring[:3].strip()
    else:
        fetched = message.mentions[0]
        lloc = opstring.find(">")
        floc = opstring.find("<@!")
        mloc = opstring[floc+3:lloc]
        print(mloc)
        if userget(mloc) == fetched:
            ftype = opstring[lloc+1:lloc+5].strip()
            ftypeend = opstring[lloc+5:].strip()
            
    toreturnf = ""
    filename = "id00<>"
    if ftype == "get":
        filename = "id00" + fetched.id + ".txt"
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                lines = [line.rstrip('\n') for line in f]
                part = ''
                for i in lines:
                    part = part + i + "; "

            toreturnf = premsg + "Identification of " + fetched.name + ": " + part
        else:
            toreturnf = premsg + fetched.name + " doesn't have anything in their identification file"

        
    elif ftype == "add":

        toadd = ftypeend.strip()
        filename = "id00" + fetched.id + ".txt"
        if not os.path.exists(filename):
            open(filename, 'w').close() 
        with open(filename, 'r') as f:
            lines = [line.rstrip('\n') for line in f]
            part = ''
            for i in lines:
                part = part + i + "; "

            part = part + toadd + "; "
            
        lines.append(toadd)
        with open(filename, 'w') as f:
             for s in lines:
                cs = ''.join(c for c in s if c <= '\u2000')
                f.write(str(cs) + "\n")
             f.close()
        toreturnf = premsg + "New identification for " + fetched.name + ": " + part
        

    # + "\n" + fetched.mention + ", " + fetched.name + ", " + ftype + ", " + filename
    print(fetched.mention + ", " + fetched.name + ", " + ftype + ", " + ftypeend + ', ' + filename)
    return message.channel, toreturnf
        

###Modify the from and to torch files without having to use the vm
def cmd_from(message):
    cmdlen = len(prefix + "from")
    opstring = message.content[cmdlen:].strip()
    ewrite("torchFrom.txt", opstring)
    return message.channel, "torchFrom updated to " + opstring
def cmd_to(message):
    cmdlen = len(prefix + "to")
    opstring = message.content[cmdlen:].strip()
    ewrite("torchTo.txt", opstring)
    return message.channel, "torchTo updated to " + opstring

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

#####debug cmds
def cmd_db_channels(message):
    added = ""
    fetched = conlang_channels()
    for u in fetched:
        if u.topic == None:
            utopic = "None"
        else:
            utopic = u.topic
        uname = ''.join(c for c in u.name if c <= '\uFFFF')
        uid = ''.join(c for c in u.id if c <= '\uFFFF')
        upos = ''.join(c for c in str(u.position) if c <= '\uFFFF')
        utopic = ''.join(c for c in utopic if c <= '\uFFFF')
        added = added + uname + "|id: " + uid + "|pos: " + upos + "|about: " + utopic + "\n"
    return message.channel, added

def cmd_db_perms(message, target):
    server = cl.get_server("327495595235213312")
    servers = []
    if target == 0:
        focus = server.get_member("342125773307510784")
        cmdlen = len(prefix + "%permsbot")
        opstring = message.content[cmdlen:].strip()
    elif target == 1:
        focus = message.author
        cmdlen = len(prefix + "%perms")
        opstring = message.content[cmdlen:].strip()
    elif target == 2:
        cmdlen = len(prefix + "%permsmanual")
        opstring = message.content[cmdlen:].strip()
        print(opstring)
        parameters = []
        spaceloc = opstring.find(" ")
        parameters.append("")
        parameters[0] = opstring[:spaceloc].strip()
        parameters.append("")
        parameters[1] = opstring[spaceloc:].strip()
        userchange = parameters[0]
        opstring = parameters[1]
        print(parameters)
        focus = userget(userchange)

    
    print(focus.name)
    for y in server.channels:
        servers.append(y)
    servernames = []
    for i in servers:
        servernames.append(i.name)
    sstring = opstring
    if sstring in servernames:
        location = servernames.index(sstring)
        serverfinal = servers[location]
        fperms = focus.permissions_in(serverfinal)
        sastring = ">"
        for g in fperms:
            sastring = sastring + str(g) + "\n"
        return message.channel, sastring

def cmd_db_user(message):
    cmdlen = len(prefix + "%user")
    opstring = message.content[cmdlen:].strip()
    gotuser = userget(opstring)
    if gotuser == None:
        returns = "Oops, something happened"
    else:
        returns = gotuser.mention
    return message.channel, returns
    



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
    cmdpart = cmdpart[rprefix:]
    if cmdpart in commands.keys():
        runPerms = commands[cmdpart].help_perms()
        userPerms = perm_get(message.author.id)
        if userPerms >= runPerms:
            toreturn = commands[cmdpart].run(message, prefix)
        else:
            toreturn = "m", [message.channel, "Oops! You do not have the permissions to run this command. You need " + perm_name(runPerms) + " (" + str(runPerms) + ") or better. You have " + perm_name(userPerms) + " (" + str(userPerms) + ")"]
            

        return toreturn
    else:
        return "m", [message.channel, "Command not found"]
                
                


    
        
