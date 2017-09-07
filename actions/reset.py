import datetime
import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
import math

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
handle = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
handle2 = loader2.load_module('maincore')
loader3 = importlib.machinery.SourceFileLoader('item', sp + '/item.py')
handle3 = loader3.load_module('item')

def run(message, rpgPrefix, alias):
    #return "m", [message.channel, "SUPRISE PERMAPERMADEATH MODE"]
    defaultStats = handle.default_stats()
    playerlist = handle.get_playerlist()
    selfEntity = playerlist[message.author.id]
    gotStats = selfEntity.rawstats
    isDead = selfEntity.prop.get('dead', False)
    
    gotStats = defaultStats
        
    starters = ["starter sword", "starter torso", "starter legs", "starter ring"]
    
    items = handle.return_itemlist()
    selfEntity.rawstats = gotStats
    for t in starters:
        gItem = items[t]
        newItem = handle3.Item(gItem)
        sts, cm, stsc = selfEntity.equip(newItem, newItem.slot)
    selfEntity.inv = [None] * 10
    selfEntity.prop = {'dead': False}
    selfEntity.invstats = selfEntity.inv_changes()
    selfEntity.stats = selfEntity.calculate_stats()
    handle.save_playerlist()
        
    if isDead == False:
        
        welcome1 = "- You commit suicide.\n"
        welcome2 = "Good job, I hope you are happy..."
        return "m", [message.channel, message.author.mention + "!\n```diff\n" + welcome1 + welcome2 + "\n```"]
    else:
        welcome1 = "! No! I cannot die yet! I still have dungeons to explore.\n"
        welcome2 = "The culmination of your soul gathers to re-create you, {}\n".format(selfEntity.name)
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
