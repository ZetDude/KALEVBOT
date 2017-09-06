import datetime
import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
import math

loader = importlib.machinery.SourceFileLoader('basic', sp + '\\basic.py')
handle = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '\\maincore.py')
handle2 = loader2.load_module('maincore')
loader3 = importlib.machinery.SourceFileLoader('item', sp + '\\item.py')
handle3 = loader3.load_module('item')

def run(message, rpgPrefix, alias):
    #return "m", [message.channel, "SUPRISE PERMAPERMADEATH MODE"]
    playerlist = handle.get_playerlist()
    selfEntity = playerlist[message.author.id]
    gotStats = selfEntity.rawstats
    isDead = selfEntity.prop.get('dead', False)
    if isDead == False:
        welcome = "- You are already alive! You don't need to respawn again >:G"
        return "m", [message.channel, message.author.mention + "!\n```diff\n" + welcome + "\n```"]
    else:
        mix = gotStats
        mix['health'] = mix['maxhealth']
        mix['location'] = 0
        mix['furthest'] = 0
        mix['tongue'] = 0
        mix['torso'] = 0
        mix['legs'] = 0
        mix['weapon'] = 0
        mix['ring1'] = 0
        mix['ring2'] = 0
        starters = ["starter sword", "starter torso", "starter legs", "starter ring"]
    
        items = handle.return_itemlist()
        for t in starters:
            gItem = items[t]
            newItem = handle3.Item(gItem)
            sts, cm, stsc = selfEntity.equip(newItem, newItem.slot)
            
        selfEntity.inv = [None] * 10
        selfEntity.prop = {'dead': False}
        selfEntity.rawstats = mix
        selfEntity.invstats = selfEntity.inv_changes()
        selfEntity.stats = selfEntity.calculate_stats()
        handle.save_playerlist()
        welcome1 = "! No! I cannot die yet! I still have dungeons to explore.\n"
        welcome2 = "The culmination of your soul gathers to re-create you, {}\n".format(selfEntity.name)
        welcome3 = "It seems you have lost all your items. You still remember your skills!\n"
        welcome4 = "Good luck..... again!"
        
        return "m", [message.channel, message.author.mention + "!\n```diff\n" + welcome1 + welcome2 + welcome3 + welcome4 + "\n```"]

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
