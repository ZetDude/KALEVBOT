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
    gotStats, trash = handle.get_stats(message.author)
    statStat = gotStats['stat']
    isDead = handle.parse_status(int(statStat))[0]
    if isDead == False:
        welcome = "You are already alive! You don't need to respawn again >:G"
        return "m", [message.channel, message.author.mention + "!\n```\n" + welcome + "\n```"]
    else:
        mix = gotStats
        mix['health'] = mix['maxhealth']
        mix['stat'] = 0
        mix['location'] = 0
        mix['furthest'] = 0
        mix['tongue'] = 0
        mix['torso'] = 0
        mix['legs'] = 0
        mix['weapon'] = 0
        mix['ring'] = 0
        handle.write_stats(message.author.id, mix)
        welcome1 = "No! I cannot die yet! I still have dungeons to explore.\n"
        welcome2 = "The culmination of your soul gathers to re-create you\n"
        welcome3 = "It seems you have lost all your items. You still remember your skills!\n"
        welcome4 = "Good luck..... again!"
        
        return "m", [message.channel, message.author.mention + "!\n```\n" + welcome1 + welcome2 + welcome3 + welcome4 + "\n```"]

def help_use():
    return "Rejoin the fun if you died before. Doesn't reset stats"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "respawn"

def help_perms():
    return 0

def help_list():
    return "Rejoin the fun if you died before"

def alias():
    return ['respawn']
