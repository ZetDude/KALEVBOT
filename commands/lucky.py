import importlib.machinery
import os
import sys
import datetime
import random

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader2.load_module('maincore')

def run(message, prefix, alias):

    try:
        with open(sp + "/important/lucky.txt", 'r') as f:
            lucky = f.readlines(0)[0]
            parts = lucky.split(":")
            oldDay = int(parts[0])
            luckyUser = parts[1]
    except FileNotFoundError:
        print("lucky.txt didn't exist, creating")
        oldDay = None
        luckyUser = None
    
    now = datetime.datetime.now().day
    if now != oldDay:
        allUsers = list(core.cl.get_all_members())
        luckyUserObject = random.choice(allUsers)
        luckyUser = luckyUserObject.id
        with open(sp + "/important/lucky.txt", 'w') as f:
            toWrite = "{}:{}".format(now, luckyUser)
            f.write(str(toWrite))
    
    if message.author.id == luckyUser:
        core.send(message.channel, "CONGRATULATIONS {}, YOU ARE THE LUCKY USER OF TODAY".format(message.author.mention))
    else:
        core.send(message.channel, "Sorry, {}, You aren't the lucky user of today. Try again tomorrow".format(message.author.mention))
    

def help_use():
    return "Display the relay deadine"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "deadline"

def help_perms():
    return 0

def help_list():
    return "Display the relay deadine"

def alias():
    return ['lucky']