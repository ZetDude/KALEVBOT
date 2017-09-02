import random
import math
import basic as mm
class Entity:
    def __init__(self, preset):
        self.name = preset.get('name', '')
        self.id = preset.get('id', None)
        self.stats = preset.get('stats', {})
        self.inv = preset.get('inv', [])

    def deal_damage(self, amount):
        print("running deal_damage as " + self.name)
        rm = ""
        tHPP = self.stats['health']
        tMAXHP = self.stats['maxhealth']
        tName = self.name
        tHP = int(math.floor(tHPP - amount))
        rm = rm + "Before damage - " + tName + " has " + str(tHPP) + "/" + str(tMAXHP) + " HP\n"
        rm = rm + str(tHPP - int(math.floor(tHPP - amount))) + " damage\n"
        rm = rm + "Before damage - " + tName + " has " + str(tHP) + "/" + str(tMAXHP) + " HP\n"
        if tHP < 0:
            rm = rm + "You killed " + tName + "! May their soul rest in peace until they respawn.\n"

        self.stats['health'] = tHP

        return rm
        

    def attack(self, target):
        print("self name: " + self.name)
        print("target name: " + target.name)
        rm = ""
        if self == target:
            return False, "Cannot attack self."
        critHit = False
        lewdHit = False
        hit = False
        canHit = False
        aLoc = self.stats['location']
        dLoc = self.stats['location']
        if aLoc != dLoc:
            return False, "Your target isn't in the same room as you. You are in room " + str(aLoc) + " but they are in room " + str(dLoc) + "."
        battlelogPath = "C:/Users/Administrator/Desktop/KALEVBOT/important/battlelog.txt"
        if target.id and self.id:
            with open(battlelogPath, "r") as f:
                lines = [line.rstrip('\n') for line in f]
            aPrev = self.id + ":" + target.id
            aOppo = target.id + ":" + self.id
            if aPrev in lines:
                return False, "You cannot attack this person because you attacked them already"
            elif aOppo in lines:
                lines.remove(aOppo)
                lines.append(aPrev)
            else:
                lines.append(aPrev)
            with open(battlelogPath, 'w') as f:
                for s in lines:
                    f.write(str(s) + "\n")
                    
            rm = rm + "Ready to strike!\n"
                    
            aSpeed = self.stats['speed']
            dSpeed = target.stats['speed']
            missChance = 0.06 + ((aSpeed - (dSpeed * 1.1)) * 0.015)
            if missChance > 0.30: #If miss chance is above 30%
                missChance = 0.30 #Don't let the miss chance go over 30%
            if missChance < 0:
                missChance = 0

            hitChance = 1 - missChance

            aLuck = self.stats['luck']
            critChance = 0.04 + aLuck * 0.0035
            if critChance > 0.30: #If crit chance is above 30%
                critChance = 0.30 #Don't let the crit chance go over 30%

            rm = rm + "Hit: " + str(int(round(hitChance*100))) + "% Crit: " + str(int(round(critChance*100))) + "%\n"
            missRoll = random.uniform(0, 1) #Roll a random float between 0 and 1
            critRoll = random.uniform(0, 1) #Roll a random float between 0 and 1
            if missRoll < missChance:
                rm = rm + "MISS!"
                return False, rm

            aAtk = self.stats['attack']
            dDef = target.stats['defense']
            dArm = 0 #temporary
            dArP = 0.55 #temporary

            damage = ((random.uniform(aAtk/3, aAtk) + random.uniform(aAtk/3, aAtk)) / 1.7) - ((dDef + dArm) / 2 * random.uniform(0.50, dArP))
            
            if critRoll < critChance:
                rm = rm + "CRITICAL HIT! DOUBLE DAMAGE!\n"
                damage = damage * 2
            else:
                rm = rm + "HIT!\n"

            if damage < 2:
                damage = 2
                rm = rm + "Damage was under 2, setting damage to guaranteed 2\n"

            print("self name: " + self.name)
            print("target name: " + target.name)
            opinion = target.deal_damage(damage)
            rm = rm + opinion

            return True, rm

    def jump_to(self, target):
        sFar = self.stats['furthest']
        sNow = self.stats['location']
        if target > sFar:
            return False, "Cannot go further than you have explored, use %explore on that"
        self.stats['location'] = target
        mm.save_playerlist()
        #mm.add_playerlist(self.id, self)
        return True, "You move from room " + str(sNow) + " to room " + str(target)

    def explore(self):

        roomlist = mm.rooms
        rm = ""
        
        sNow = self.stats['location']
        self.stats['furthest'] += 1
        self.stats['location'] = self.stats['furthest']
        sNew = self.stats['location']

        if len(roomlist) == sNew:
            newroom = Room()
            roomlist.append(newroom)
            newroom.make_desc()
            with open('important/rooms.txt', 'wb') as f: #open the file named fileName
                pickle.dump(rooms, f) #Pickle and update the stats file
            rm = "\nYou are the first person to enter this room"
        ident = roomlist[sNew].desc

        gotItem, prm = self.scavenge_item()

        print(self.id)
        #mm.add_playerlist(self.id, self)
        mm.save_playerlist()

        bothMSG = "You move from room " + str(sNow) + " to room " + str(sNew) + rm
        publicMSG = bothMSG
        privateMSG = bothMSG + "\n" + ident + "\n" + prm
        return publicMSG, privateMSG

    def scavenge_item(self):
        sLoc = self.stats['location']
        targetpool = ''
        rm = '' 
        if sLoc < 21:
            targetpool = 'testpool1'
        gotItem = mm.scavenge(targetpool)
        rm += 'The soul of the game developer calls down to you and gives you an item from the pool ' + targetpool + "\n"
        rm += 'You got ' + gotItem.sg + "\n"
        st, rma = self.add_item(gotItem)
        rm += rma
        return gotItem, rm

    def add_item(self, item):
        freeSlot = None
        print("inv starts here")
        print(len(self.inv))
        for i in range(len(self.inv)):
            print(self.inv[i])
            if self.inv[i] == None:
                freeSlot = i
                print(freeSlot)
                break

        print(freeSlot)
        if freeSlot == None:
            return False, "You do not have any room in your inventory\n"

        self.inv[freeSlot] = item
        item.set_entity(self)
        return True, "Added item " + item.name + " to slot " + str(freeSlot+1) + "\n"

    def use_slot(self, slot):
        slot = slot - 1
        if slot < 0:
            return False, False, "Slots smaller than 1 do not exist"
        try:
            isFree = self.inv[slot]
        except:
            return False, False, "That slot is outside the range of your inventory"
        if isFree == None:
            return False, False, "That slot is empty"
        print(isFree)
        print(isFree.sg)
        print(isFree.usehelp)

        state, toReturn, done = isFree.use_item()
        if done:
            self.inv[slot] = None
        mm.save_playerlist()
        return True, state, toReturn
        

        
            

        
                
            

             
            
            
            




        
