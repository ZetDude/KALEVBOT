import importlib.machinery
import math

loader = importlib.machinery.SourceFileLoader('basic', 'C:/Users/Administrator/Desktop/KALEVBOT/basic.py')
handle = loader.load_module('basic')
loader2 = importlib.machinery.SourceFileLoader('maincore', 'C:/Users/Administrator/Desktop/KALEVBOT/maincore.py')
handle2 = loader2.load_module('maincore')

def run(message, rpgPrefix, alias):
    targetID = ""
    target = ""
    combine = None
    print(len(message.mentions))
    if len(message.mentions) == 1:
        mentiont = message.mentions[0]
        target = mentiont
        targetID = mentiont.id
    else:
        cmdlen = len(rpgPrefix + alias)
        opstring = message.content[cmdlen:].strip()
        gotuser = handle2.userget(opstring)
        if gotuser == None:
            combine = "Something failed, defaulting to message sender"
            target = message.author
            targetID = message.author.id
        else:
            target = gotuser
            targetID = gotuser.id
    print(targetID)
    
    print(target)
    print(target.name)
    playerlist = handle.get_playerlist()
    if targetID not in playerlist:
        return "m", [message.channel, message.author.mention + ", that person hasn't joined the game. %join to join the game!"]
    targetEntity = playerlist[targetID]
    returnMSG = targetEntity.stats
    rreturnMSG = targetEntity.rawstats
    ireturnMSG = targetEntity.invstats
    name = "+ Stats of " + targetEntity.name + ":\n"
    sts = "+ Stat points remaining: " + str(returnMSG['statpoints'])
    dead = ""
    if targetID != message.author.id:
        sts = ""
    if returnMSG['statpoints'] == 0:
        sts = ""
    div = "-" * len(sts)
    if len(div) == 0:
        div = "-" * (len(name) - 1)
    if returnMSG['health'] < 1:
        dead = "\n- DEAD"
    
    r = {}
    rs = ['maxhealth', 'attack', 'speed', 'defense', 'luck']
    for i in rs:
        fRaw = str(rreturnMSG[i])
        fInv = str(ireturnMSG[i])
        fAll = str(returnMSG[i])
        rSp = 3 - len(fRaw)
        iSp = 3 - len(fInv)
        aSp = 3 - len(fAll)
        g =  fRaw + rSp * " " + " + " + fInv + iSp * " " + " = " + fAll + aSp * " "
        r[i] = g
    newhp = str(returnMSG['health'])
    maxhp = str(returnMSG['maxhealth'])
    atk = str(returnMSG['attack'])
    spd = str(returnMSG['speed'])
    dfs = str(returnMSG['defense'])
    luk = str(returnMSG['luck'])
    loc = str(returnMSG['location'])
    far = str(returnMSG['furthest'])
    compileMSG = str(name + div +
                     "\n- Health   : " + newhp + "/" + maxhp + dead +
                     "\nMax health : " + r['maxhealth'] + 
                     "\nAttack     : " + r['attack'] +
                     "\nSpeed      : " + r['speed'] +
                     "\nDefense    : " + r['defense'] +
                     "\nLuck       : " + r['luck'] +
                     "\nLocation   : " + loc + "/" + far + "\n" + sts)
    print(returnMSG)
    return "m", [message.channel, message.author.mention + ", \n```diff\n" + str(compileMSG) + "\n```"]

def help_use():
    return "Get your stats"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "stats"

def help_perms():
    return 0

def help_list():
    return "Get your stats"

def alias():
    return ['stats']