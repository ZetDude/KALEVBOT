import datetime
import importlib.machinery
import math
import os

loader = importlib.machinery.SourceFileLoader('basic', 'C:/Users/Administrator/Desktop/KALEVBOT/basic.py')
handle = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', 'C:/Users/Administrator/Desktop/KALEVBOT/maincore.py')
handle2 = loader2.load_module('maincore')

def run(message, rpgPrefix, alias):
    #return "m", [message.channel, "SUPRISE PERMAPERMADEATH MODE"]
    defaultStats = handle.default_stats()
    gotStats, trash = handle.get_stats(message.author)
    statStat = gotStats['stat']
    isDead = handle.parse_status(int(statStat))[0]
    if isDead == False:
        handle.write_stats(message.author.id, defaultStats)
        welcome1 = "- You commit suicide.\n"
        welcome2 = "Good job, I hope you are happy..."
        return "m", [message.channel, message.author.mention + "!\n```\n" + welcome1 + welcome2 + "\n```"]
    else:
        handle.write_stats(message.author.id, defaultStats)
        welcome1 = "! No! I cannot die yet! I still have dungeons to explore.\n"
        welcome2 = "The culmination of your soul gathers to re-create you\n"
        welcome3 = "It seems you have lost everything! It's as if you first started exploring.\n"
        welcome4 = "Good luck..... again!"
        
        return "m", [message.channel, message.author.mention + "!\n```diff\n" + welcome1 + welcome2 + welcome3 + welcome4 + "\n```"]

def help_use():
    return "Reset _everything_ and begin the game from the beginning"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "reset"

def help_perms():
    return 0

def help_list():
    return "Reset _everything_ and begin the game from the beginning"

def alias():
    return ['reset']
