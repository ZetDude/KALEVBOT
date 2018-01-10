import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader2.load_module('maincore')
loader3 = importlib.machinery.SourceFileLoader('item', sp + '/item.py')
item = loader3.load_module('item')

def run(message, rpgPrefix, aliasName):
    #return "m", [message.channel, "SUPRISE PERMAPERMADEATH MODE"]
    playerlist = rpg.get_playerlist()
    selfEntity = playerlist[message.author.id]
    gotStats = selfEntity.rawstats
    isDead = selfEntity.prop.get('dead', False)
    if isDead is False:
        welcome = "- You are already alive! You don't need to respawn again >:G"
        return "m", [message.channel, message.author.mention + "!\n```diff\n" + welcome + "\n```"]
    mix = gotStats
    mix['health'] = mix['maxhealth']
    mix['location'] = 0
    mix['furthest'] = 0

    equipment = ["tongue", "ring1", "ring2", "weapon", "torso", "legs"]
    starters = ["starter sword", "starter torso", "starter legs", "starter ring"]

    for i, val in enumerate(selfEntity.inv):
        if val is not None:
            if not val.prop.get("legendary", False):
                selfEntity.inv[i] = None

    for i in equipment:
        if selfEntity.stats[i].prop.get("legendary", False):
            selfEntity.unequip(i)


    items = rpg.return_itemlist()
    for t in starters:
        gItem = items[t]
        newItem = item.Item(gItem)
        sts, cm, stsc = selfEntity.equip(newItem, newItem.slot)

    selfEntity.inv = [None] * 10
    selfEntity.prop = {'dead': False}
    selfEntity.rawstats = mix
    selfEntity.invstats = selfEntity.inv_changes()
    selfEntity.stats = selfEntity.calculate_stats()
    rpg.save_playerlist()
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

def aliasName():
    return ['respawn']
