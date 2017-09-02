import random
import math
import maincore as mc
import os
import importlib
import pickle
from room import *
from item import *
from entity import *

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
    #with open('important/playerlist.txt', 'wb') as f: 
        #pickle.dump(playerlist, f)
    with open('important/rooms.txt', 'rb') as f: #open the file named fileName
        rooms = pickle.loads(f.read()) #unpickle the stats file
    with open('important/playerlist.txt', 'rb') as f: #open the file named fileName
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

def temp_user(user):
    ###--Temporary workaround to the lack of the discord module, for now--
    ###!!Unused now!!
    if user.lower() == "zet":
        return "104626896360189952"
    elif user.lower() == "dummy":
        return "333255360095846401"

def sub(author, add):
    with open('important/sub.txt', 'r') as f:
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
    return get_itemlist()

def return_pools():
    return get_pools()

def scavenge(tp):
    items = get_itemlist() 
    pools = get_pools()
    target = pools[tp] 
    fItem = rweight(target)
    gItem = items[fItem] 
    newItem = Item(gItem)
    return newItem  
    
def ping():
    sm = ""
    with open('important/sub.txt', 'r') as f:
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
                    'ring1': 0}

    return defaultStats

def players_in_room(room):
    path = 'C:/Users/Administrator/Desktop/KALEVBOT/stats/'

    for filename in os.listdir(path):
        with open(filename, 'rb') as f: #open the file named fileName
            lines = pickle.loads(f.read()) #unpickle the stats file
            #if lines['location'] == room:
        
        
def explore(userGet):
    material = ["brick", "clean brick", "some sort of shiny brick",
            "what seems like solid gold", "cracked brick",
            "an unknown material", "slightly glowing brick",
            "stone"]

    atmos = ["an eerie", "a wet", "a dry", "a quiet", "a nice"]
    global rooms
    rm = ""
    itemdesc = ""
    roomitem = None
    statsGet, trash = get_stats(userGet)
    locationNow = statsGet['furthest']
    locationCur = statsGet['location']
    locationNext = locationNow + 1
    if random.uniform(0, 1) > 0.65:
        itemlist = get_itemlist()
        print(itemlist)
        itemTemplate = random.choice(list(itemlist.values()))
        print(itemTemplate)
        roomitem = Item(itemTemplate)
        itemdesc = "\nThere is a(n) " + roomitem.name + " in the room"
    if len(rooms) == locationNext:
        ident = "The room is made out of " + random.choice(material) + ". It has " + random.choice(atmos) + " atmosphere to it"
        if roomitem:
            rooms.append(Room(ident, [roomitem]))   
        else:
            rooms.append(Room(ident))
        with open('important/rooms.txt', 'wb') as f: #open the file named fileName
            pickle.dump(rooms, f) #Pickle and update the stats file
        rm = "\nYou are the first person to enter this room"
    else:
        ident = rooms[locationNext].desc

    

    bothMSG = "You move from room " + str(locationCur) + " to room " + str(locationNext) + rm
    publicMSG = bothMSG
    privateMSG = bothMSG + "\n" + ident + itemdesc
    return publicMSG, privateMSG, locationNext

def look(number):
    public = "You are in room " + str(number)
    rm = public
    targetRoom = rooms[number]
    descript = targetRoom.desc
    items = targetRoom.itemlist
    rm = rm + "\n" + descript
    for i in items:
        rm = rm + "\nThere is a(n) " + i.name + " in the room"
    return "```\n" + rm + "\n```", "```\n" + public + "\n```"

def jump(userGet, target):
    statsGet, trash = get_stats(userGet)
    locationNow = statsGet['location']
    locationFar = statsGet['furthest']
    if target > locationFar:
        return None, "Cannot go to further than you have explored, use %explore for that"
    statsGet['location'] = target
    write_stats(userGet.id, statsGet)
    publicMSG = "You move from room " + str(locationNow) + " to room " + str(target)
    return publicMSG, None
    
def get_stats(userGet):
    ###Fetch the stats bound to an user
    userID = userGet.id
    opinion = ""
    fileName = "stats" + userID + ".txt" #construct the file name, such as stats104626896360189952.txt
    hasFile = os.path.isfile('stats/' + fileName) #check if that user has joined the game
    if hasFile == False: #if they don't
        opinion = userGet.name + " doesnt have stats, which means you cannot interact with them. If you want them to join, ask them to use %join\n"
        return {}, opinion #return an empty dictionary and a string explaining the problem
    with open('stats/' + fileName, 'rb') as f: #open the file named fileName
        lines = pickle.loads(f.read()) #unpickle the stats file

    return lines, opinion #return the dictionary represeting the stats

def write_stats(userID, toWrite):
    ###Overwrite the old stats with toWrite
    fileName = "stats" + userID + ".txt" #construct the file name, such as stats104626896360189952.txt
    with open('stats/' + fileName, 'wb') as f: #open the file named fileName
        pickle.dump(toWrite, f) #Pickle and update the stats file

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

def update_battle_log(fromID, toID):
    ###Check if the battle log already has an attack from the same player to the same player
    ###If it does, null the attack and don't do anything
    ###If it doesn't, remove any attacks from the current defender that targetted the current attacker
    ###This makes a turn-based back-and-forth system where you can only attack the other person if they have attacked you already before
    with open('important/battlelog.txt', 'r') as f: #open the battle log
        lines = [line.rstrip('\n') for line in f] #remove all the \n from the end of lines
        f.close()#close the file

    attackerPrevious = fromID + ":" + toID #The string that should be in the battle log if the attacker has attacke before
    attackerOpposite = toID + ":" + fromID #The string that should be in the battle log if the current defended has attacked the current attacker before
    if attackerPrevious in lines: #If that person has indeed attacked the same person before, 
        return "You cannot attack this person because you attacked them already" #don't do anything
    if fromID == toID:
        return "You cannot attack yourself. Idiot."
    if attackerOpposite in lines: #If returning an attack
        lines.remove(attackerOpposite) #Remove the current defender's previous attack to the current attacker
        lines.append(attackerPrevious) #Add the current attack to the new battle log
        
    else: #If the players have never attacked eachother before
        lines.append(attackerPrevious) #Add the current attack to the new battle log
        

    with open('important/battlelog.txt', 'w') as f:
        for s in lines:
            f.write(str(s) + "\n") #Update the battle log
    f.close()
    return True #Return that the attack is allowed

def attack_miss_chance(fromSpeed, toSpeed):
    ###Calculate miss chance
    chance = 0.06 + ((toSpeed - (fromSpeed * 1.1)) * 0.015)
    if chance > 0.30: #If miss chance is above 30%
        chance = 0.30 #Don't let the miss chance go over 30%
    if chance < 0:
        chance = 0
    return chance

def attack_crit_chance(fromLuck):
    ###Calculate crit chance
    chance = 0.04 + fromLuck * 0.0035
    if chance > 0.30: #If crit chance is above 30%
        chance = 0.30 #Don't let the crit chance go over 30%
    return chance

def attack_damage(fromAttack, toDefense, crit, lewd):
    ###Calculate the attack damage
    toArmor = 0 #Temporary default armor value
    toArmorP = 0.55 #Temporary default armor percentage value
    damage = ((random.uniform(fromAttack/3, fromAttack) + random.uniform(fromAttack/3, fromAttack)) / 1.7) - ((toDefense + toArmor) / 2 * random.uniform(0.50, toArmorP))
    #deviation = random.uniform(0.83, 1.39)
    #damage = 1.8 * (fromAttack * deviation / (1 + 0.1 * toDefense))
    if damage < 0: #if damage is negative
        damage = 0 #deal no damage
    if lewd: #if damage is self-hit
        return damage / 1.5 #reduce damage
    if crit: #if attack is a crit
        return damage * 2 #double daage
    else: #if just a normal attack
        return damage

def attack_lewd_chance(lewd):
    ###calculate self-hit chance
    chance = (lewd**1.2)/200
    if chance > 0.4: #if chance is over 40%
        chance = 0.4 #do not let it go over 40%
    return chance

def deal_damage(damageDealt, toPlayerStats, toID, ts, reset):
    ###Deal damage to an user
    rm = ""
    enemyHealth = toPlayerStats['health'] #fetch health from dictionary
    enemyMaxHealth = toPlayerStats['maxhealth'] #fetch max health from dictionary
    enemyHealth = int(math.floor(enemyHealth - damageDealt)) #get how much health would remain, floored
    if reset: #if debug respawn mode is on
        if enemyHealth <= 0: #if person is dead
            rm = "You killed " + ts + "!" + " Due to debug reasons, their health has been reset to max" + "\n"
            enemyHealth = enemyMaxHealth #reset health
    else:
        if enemyHealth <= 0: #if dead
            rm = "You killed " + ts + "! May their soul rest in peace until they respawn"
                                              
    toPlayerStats['health'] = enemyHealth
    
    write_stats(toID, toPlayerStats) #rewrite stats
    return rm, enemyHealth

def attack(fromUser, toUser):
    ###Main attack function
    rm = ""
    ts = "the enemy" #little snippets for more "personalization" of strings
    tso = "enemy has"
    typ = "m"
    critHit = False
    lewdHit = False
    fromID = fromUser.id
    toID = toUser.id
    fromPlayerStats, opinion = get_stats(fromUser) #Fetch the stats of the attacking player
    rm = rm + opinion
    toPlayerStats, opinion = get_stats(toUser) #Fetch the stats of the defending player
    rm = rm + opinion
    if fromPlayerStats['location'] != toPlayerStats['location']:
        return "That person isn't in the same room as you. You are in room " + str(fromPlayerStats['location']) + " but they are in room " + str(toPlayerStats['location'])
    light = update_battle_log(fromID, toID) #Fetch if attack is allowed and update the battle log
    if light != True: #If attack isnt allowed
        rm = rm + light + "\n" #return why
    else: #If attacj is allowed
        rm = rm + "Ready to strike!" + "\n"
        ts = toUser.name
        tso = toUser.name + " has"
        missChance = attack_miss_chance(fromPlayerStats['speed'], toPlayerStats['speed']) #Calculate the miss chance
        critChance = attack_crit_chance(fromPlayerStats['luck']) #Caluclate the crit chance
        lewdChance = attack_lewd_chance(toPlayerStats['lewdness']) #Caluclate the lewd self hit chance
        rm = rm + "M: " + str(int(round(missChance*100))) + "% C: " + str(int(round(critChance*100))) + "% L: " + str(int(math.floor(lewdChance*100))) + "%\n"
        missRoll = random.uniform(0, 1) #Roll a random float between 0 and 1
        critRoll = random.uniform(0, 1) #Roll a random float between 0 and 1
        lewdRoll = random.uniform(0, 1) #Roll a random float between 0 and 1
        print("Miss rolled: " + str(missRoll))
        print("Crit rolled: " + str(critRoll))
        print("Lewd rolled: " + str(lewdRoll))
        if lewdRoll < lewdChance:
            rm = rm + "THE LEWDNESS OF THE ENEMY CAUSES YOU TO ATTACK YOURSELF!" + "\n"
            lewdHit = True
            toPlayerStats, opinion = get_stats(fromUser)
            missChance = 0.0
            critChance = 0.0
            toID = fromID
            ts = "youself"
            tso = "you have"
        if missRoll > missChance:
            if critRoll < critChance:
                rm = rm + "CRITICAL HIT! DOUBLE DAMAGE!" + "\n"
                critHit = True
            else:
                rm = rm + "HIT!" + "\n"

            enemyHealth = toPlayerStats['health']
            enemyMaxHealth = toPlayerStats['maxhealth']
            rm = rm + "Before attack - " + tso + " " + str(enemyHealth) + " HP out of " + str(enemyMaxHealth) + "\n"
            damageDealt = attack_damage(fromPlayerStats['attack'], toPlayerStats['defense'], critHit, lewdHit)
            dmgres, enemyHealthPost = deal_damage(damageDealt, toPlayerStats, toID, ts, False)
            if enemyHealthPost < 1:
                print("ded")
                isDead = parse_status(int(toPlayerStats['stat']))
                isDead[0] = True
                isDead = compile_status(isDead)
                toPlayerStats['stat'] = isDead
                print(toPlayerStats)
                write_stats(toID, toPlayerStats)
            rm = rm + str(enemyHealth - int(math.floor(enemyHealth - damageDealt))) + " damage! \n"
            rm = rm + "After attack - " + tso + " " + str(enemyHealthPost) + " HP out of " + str(enemyMaxHealth) + "\n" + dmgres
            
        else:
            rm = rm + "MISS!" + "\n"

    return rm
    
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
    
    


##gotStats = get_stats(temp_user(input("--> ")))
##hpmax, hpnow, at, sp, df, lk, st = gotStats
##print("HP - " + str(hpnow) + "/" + str(hpmax))
##print("AT - " + str(at))
##print("SP - " + str(sp))
##print("DF - " + str(df))
##print("LK - " + str(lk))
##print("ST - " + str(st))
##print("ST PARSE - " + str(parse_status(st)))

##while True:
##    action = input("Action >>> ")
##    if action == "action":
##        player = input("Who is playing? >>> ")
##        playerid = temp_user(player)
##        actionType = input("Type of action? >>> ")
##        if actionType == "attack":
##            attackTarget = input("Attack who? >>> ")
##            attackTargetID = temp_user(attackTarget)
##            attack(playerid, attackTargetID)

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
    if cmdpart in alias:
        cmdoriginal = cmdpart
        cmdpart = alias[cmdpart]
        runPerms = commands[cmdpart].help_perms()
        userPerms = mc.perm_get(message.author.id)
        hasFile = message.author.id in playerlist
        isDead = False
        canPlay = False
        if hasFile:
            print(playerlist[message.author.id].stats)
            statStat = playerlist[message.author.id].stats['stat']
            isDead = parse_status(int(statStat))[0]
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
