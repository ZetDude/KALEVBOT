import importlib.machinery
import os
import sys
import item

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader2.load_module('maincore')
loader3 = importlib.machinery.SourceFileLoader('item', sp + '/item.py')
item = loader3.load_module('item')

def run(message, rpgPrefix, alias):
    defaultStats = rpg.default_stats()
    authorID = message.author.id
    playerlist = rpg.get_playerlist()
    
    playertemplate = {'name': message.author.name,
                      'id': message.author.id,
                      'stats': defaultStats,
                      'inv': [None] * 10,
                      'prop': {'dead': False}}
    
    starters = ["starter sword", "starter torso", "starter legs", "starter ring"]
    
    if authorID in playerlist:
        welcome1 = "Welcome to the game, er...\n"
        welcome2 = "- You are already in the game! You don't need to join again >:G"
        return "m", [message.channel, message.author.mention + "!\n```\n" + welcome1 + welcome2 + "\n```"]
    else:
        rpg.add_playerlist(message.author.id, playertemplate)
        items = item.get_itemlist()
        targetP = playerlist[message.author.id]
        for t in starters:
            gItem = items[t]
            newItem = item.Item(gItem)
            sts, cm, stsc = targetP.equip(newItem, newItem.slot)
        welcome1 = "+ Welcome to the game, " + message.author.name + "!\n"
        welcome1 = ''.join(c for c in welcome1 if c <= '\uFFFF')
        welcome2 = "For now, your stats are 0. I advise you upgrade them right away.\n"
        welcome3 = "Use %upgrade <stat> <amount> for that. I have given 20 stat points\n"
        welcome4 = "The stats are: 'Health', 'Attack', 'Defense', 'Speed' and 'Luck'\n"
        welcome5 = "Upgrading these stats takes 1 stat point for one extra point in that category.\n"
        welcome6 = "Health costs one upgrade point for 2 max health upgrades.\n"
        welcome7 = "! Learn more using %about.\n"
        welcome8 = "- Good luck!"
        
        return "p", [message.author,
                     "```diff\n" + welcome1 + welcome2 + welcome3 + welcome4 + welcome5 + welcome6 + welcome7 + welcome8 + "\n```",
                     message.channel,
                     message.author.mention + "!\n" + welcome1]

def help_use():
    return "Creates a stat file for you so you could participate in the RPG"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "join"

def help_perms():
    return 0

def help_list():
    return "Join the fun"

def alias():
    return ['join', 'start', 'enter', 'play']
