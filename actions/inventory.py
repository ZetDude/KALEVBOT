import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
import math

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader2.load_module('maincore')

def run(message, rpgPrefix, alias):
    targetID = ""
    if len(message.mentions) == 1:
        mentiont = message.mentions[0]
        targetID = mentiont.id
    else:
        cmdlen = len(rpgPrefix + alias)
        opstring = message.content[cmdlen:].strip()
        gotuser = core.userget(opstring)
        if gotuser is None:
            targetID = message.author.id
        else:
            targetID = gotuser.id
    playerlist = rpg.get_playerlist()
    if targetID not in playerlist:
        return "m", [message.channel, message.author.mention + ", that person hasn't joined the game. %join to join the game!"]
    targetEntity = playerlist[targetID]
    returnMSG = targetEntity.inv
    name = "Inventory of " + targetEntity.name + ":\n"
    compileMSG = ""
    for i, pos in enumerate(returnMSG):
        if pos is None or pos == 0:
            y = "Empty"
        else:
            y = pos.name
        sp = "  "
        if i+1 < 10:
            sp = "   "
        compileMSG += "Slot " + str(i+1) + sp + ":: " + y + "\n"
    invspaces = [targetEntity.rawstats['weapon'], 
                 targetEntity.rawstats['torso'], 
                 targetEntity.rawstats['legs'], 
                 targetEntity.rawstats['ring1'], 
                 targetEntity.rawstats['ring2'], 
                 targetEntity.rawstats['tongue']]
                 
    for i, pos in enumerate(invspaces):
        if pos == 0:
            invspaces[i] = "Nothing"
        else:
            invspaces[i] = str(pos.name)
    compileMSG += str(name + 
                  "\nWeapon   :: " + invspaces[0] + 
                  "\nTorso    :: " + invspaces[1] + 
                  "\nLeggings :: " + invspaces[2] + 
                  "\nRing 1   :: " + invspaces[3] + 
                  "\nRing 2   :: " + invspaces[4] + 
                  "\nTongue   :: " + invspaces[5])
    return "m", [message.channel, message.author.mention + ", \n```asciidoc\n" + str(compileMSG) + "\n```"]

def help_use():
    return "Get your inventory"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "inventory"

def help_perms():
    return 0

def help_list():
    return "Get your inventory"

def alias():
    return ['inventory', 'inv', 'equipment', 'wearing', 'have']
