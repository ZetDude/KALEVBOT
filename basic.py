import random
import math
import maincore as mc
import os
import importlib
import pickle
from room import *
import item
from entity import *

rpgPrefix = "%" #The prefix used for RPG commands
helptext = "If you are seeing this, panic!" #Define the helptext variable that will be overwritten later

rooms = [Room("This room contains all the noobs who just started")]
playerlist = {}

deadCMD = ["help", "respawn", "reset", "sub", "notify", "sudo", "about"]
joinCMD = ["help", "join", "sub", "unsub", "notify", "sudo", "about"]

f = []
for (dirpath, dirnames, filenames) in os.walk('./actions'): #get every file in the actions folder
    f.extend(filenames) #and add them to this list
    break

py_files = filter(lambda x: os.path.splitext(x)[1] == '.py', f) #get all the .py files
module_names = list(map(lambda x: os.path.splitext(x)[0], py_files))

commands = {}
alias = {}  
for m in module_names:
    commands[m] = importlib.import_module('actions.' + m) #Create a dictionary of commands and import them all

print("basic.py was silently loaded in a module")

def ready():
    global rooms
    global playerlist
    global alias
##    with open('important/playerlist.txt', 'rb') as f: 
##        pickle.dump(playerlist, f)
##    with open('important/rooms.txt', 'rb') as f: 
##        pickle.dump(rooms, f)
    with open('important/rooms.txt', 'xb') as f: #open the file named fileName
        rooms = pickle.loads(f.read()) #unpickle the stats file
    with open('important/playerlist.txt', 'xb') as f: #open the file named fileName
        playerlist = pickle.loads(f.read()) #unpickle the stats file
    print(rooms)
    print(playerlist)
    for n in module_names:
        for m in commands[n].alias():
            alias[m] = n
    print(alias)
    print("basic.py rpg module loaded")
    print("RPG prefix is " + rpgPrefix)
    cache_help() #update the %help file
    print(helptext)

def get_helptext():
    return helptext #return the helptext for in case other commands need to use it

def cache_help():
    ###Compile the helptext and put it into a variable to save processing power when it is needed later
    ###a.k.a "cache" the helptext into a variable
    global helptext
    clist = commands.keys() #get all the command names from the command dictionary
    ft = ""
    ftn = ""
    found = False
    for i in range(11): #cycle through all the permission levels. This orders the command nicely
        found = False #this will stay false if nothing is found in this permission level cycle
        ftn = ""
        for y in clist:
            if commands[y].help_perms() == i: #if the command permission level matches the current permission level that is being cycled
                part1 = commands[y].help_cmd(rpgPrefix) #fetch that command's command syntax
                part2 = commands[y].help_list() #fetch that command's breif description
                ftn = ftn + part1 + " :: " + part2 + "\n" #put those two into one line added onto the previously already found help
                found = True #say that something was found in this permission level cycle
        if found: #only if something was found in that permission level (to avoid lots of empty permission headers
            ft = ft + "== THE FOLLOWING COMMANDS NEED PERMISSION LEVEL " + str(i) + " OR BETTER ==\n" + ftn
        else:
            ft = ft + ftn
                

    ft = "```asciidoc\n" + ft + "\n```" #put the text into an asciidoc codeblock to get colors
    helptext = ft #save the helptext to variable

def compose_help(cSearch):
    ###compose help for a specific command
    usage1 = "Usage:\n"
    usage2 = commands[cSearch].help_cmd(rpgPrefix) + "\n" #get that command's command syntax
    usage3 = commands[cSearch].help_use() + "\n" #get that command's (longer) explanation
    paramGet = commands[cSearch].help_param() #get that command's parameters
    if paramGet == None: #If the command takes no parameters
        usage4 = "No parameters required\n"
    else:
        usage4 = paramGet + "\n"
    part5 = mc.perm_name(commands[cSearch].help_perms()) #Get the permission level (name) needed for that command
    part6 = str(commands[cSearch].help_perms()) #Get the permission level needed for that command
    usage5 = "You need the " + part5 + " (" + part6 + ") permission level or better to run this command"
    return "```\n" + usage1 + usage2 + usage3 + usage4 + usage5 + "\n```" #put all the previous data together and return it

def sub(author, add):
    with open('important/sub.txt', 'x') as f:
        lines = [line.rstrip('\n') for line in f] #remove all the \n from the end of lines

    print(lines)
    
    if add:
        if author.id not in lines:
            lines.append(author.id)
            with open('important/sub.txt', 'w') as f:
                for s in lines:
                    f.write(str(s) + "\n")
            return "subscribed!"
            
        else:
            return "already subscribed!"
    else:
        if author.id in lines:
            lines.remove(author.id)
            with open('important/sub.txt', 'w') as f:
                for s in lines:
                    f.write(str(s) + "\n")
            return "unsubscribed!"
        else:
            return "you arent subscribed!"
        
def return_itemlist():
    return item.get_itemlist()

def return_pools():
    return item.get_pools()

def scavenge(tp):
    items = item.get_itemlist() 
    pools = item.get_pools()
    target = pools[tp] 
    fItem = item.rweight(target)
    if fItem == None:
        return None
    gItem = items[fItem]
    newItem = item.Item(gItem)
    return newItem  
    
def ping():
    sm = ""
    with open('important/sub.txt', 'x') as f:
        lines = [line.rstrip('\n') for line in f] #remove all the \n from the end of lines

    print(lines)
    for i in lines:
        sm = sm + "<@" + i + ">, "

    return sm
    
def default_stats():
    defaultStats = {'maxhealth': 40,
                    'health': 40,
                    'attack': 5,
                    'speed': 3,
                    'defense': 3,
                    'luck': 3,
                    'stat': 0,
                    'location': 0,
                    'furthest': 0,
                    'statpoints': 20,
                    'tongue': 0,
                    'torso': 0,
                    'legs': 0,
                    'weapon': 0,
                    'ring1': 0,
                    'ring2': 0}

    return defaultStats

def parse_status(status):
    ###Convert the base 10 representation of the status into a list of booleans
    binaryStatus = "{0:08b}".format(status) #Convert base 10 to base 2
    binaryList = list(binaryStatus) #Convert binary number into a binary list
    booleanList = [bool(int(x)) for x in binaryList] #Convert binary list into a boolean list
    return booleanList #Return the boolean list
    ###Status boolean list explanation
    ###length: 8
    ###element 0; PVP status - True if the player has opted in to get random attacks

def compile_status(booleanList):
    ###Convert the binary list representation of the status into a base 10 int
    binaryList = [str(int(x)) for x in booleanList] #Covert boolean list into binary list
    binaryStatus = "".join(binaryList) #Convert binary list into binary string
    decimalStatus = int(binaryStatus, 2) #convert binary string into base 10 int
    return decimalStatus #Return the base 10 representation of

    
def add_playerlist(pid, value):
    global playerlist
    playerlist[pid] = Entity(value)
    with open('important/playerlist.txt', 'wb') as f: 
        pickle.dump(playerlist, f)

def get_playerlist():
    return playerlist

def save_playerlist():
    global playerlist
    with open('important/playerlist.txt', 'wb') as f: 
        pickle.dump(playerlist, f)

def new_playerlist(playerlistnew):
    global playerlist
    playerlist = playerlistnew
    with open('important/playerlist.txt', 'wb') as f: 
        pickle.dump(playerlistnew, f)
    
    


def run(message):
    toreturn = None
    cmdpart = "help"
    canPlay = True
    spaceloc = message.content.find(" ")
    if spaceloc == -1:
        cmdpart = message.content
    else:
        cmdpart = message.content[:spaceloc].strip()
    rprefix = len(rpgPrefix)
    cmdpart = cmdpart[rprefix:]
    print(cmdpart)
    print(commands.keys())
    if cmdpart.lower() in alias:
        cmdoriginal = cmdpart
        cmdpart = alias[cmdpart]
        runPerms = commands[cmdpart].help_perms()
        userPerms = mc.perm_get(message.author.id)
        hasFile = message.author.id in playerlist
        isDead = False
        canPlay = False
        if hasFile:
            print(playerlist[message.author.id].stats)
            sEnt = playerlist[message.author.id]
            isDead = sEnt.prop.get('dead', False)
            print(isDead)
            if isDead:
               if cmdpart in deadCMD:
                    canPlay = True
               else:    
                    canPlay = False
            else:
                canPlay = True
        else:
            if cmdpart in joinCMD:
                canPlay = True
            else:
                canPlay = False
        if canPlay:
            if userPerms >= runPerms:
            #if userPerms == 10:
                toreturn = commands[cmdpart].run(message, rpgPrefix, cmdoriginal)
            else:
                toreturn = "m", [message.channel, "Oops! You do not have the permissions to run this command. You need " + mc.perm_name(runPerms) + " (" + str(runPerms) + ") or better. You have " + mc.perm_name(userPerms) + " (" + str(userPerms) + ")"]
                #toreturn = "m", [message.channel, "Bot is in lockdown mode"]
        elif isDead:
            toreturn = "m", [message.channel, "You are dead! Use %respawn to start from square one, with your stats, or\nUse %reset to completely restart everything, losing ***__ALL__*** of your progress"]
        else:
            toreturn = "m", [message.channel, "Oops! You haven't joined the game. Use %join to join in on the fun"]
            
        print(toreturn)
        return toreturn
    else:
        return "m", [message.channel, "Command not found"]
