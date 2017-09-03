import random
import math
import basic as mm
import pickle
import room
class Entity:
    def __init__(self, preset):
        self.name = preset.get('name', '')
        self.id = preset.get('id', None)
        self.rawstats = preset.get('stats', {})
        self.stats = self.rawstats
        self.invstats = self.inv_changes()
        self.stats = self.calculate_stats()
        self.prop = preset.get('prop', {})
        self.inv = preset.get('inv', [])

    def deal_damage(self, amount):
        print("running deal_damage as " + self.name)
        rm = ""
        tHPP = self.rawstats['health']
        tMAXHP = self.stats['maxhealth']
        tName = self.name
        tHP = int(math.floor(tHPP - amount))
        rm = rm + "Before damage - " + tName + " has " + str(tHPP) + "/" + str(tMAXHP) + " HP\n"
        rm = rm + "- " + str(tHPP - int(math.floor(tHPP - amount))) + " damage\n"
        rm = rm + "Before damage - " + tName + " has " + str(tHP) + "/" + str(tMAXHP) + " HP\n"
        if tHP < 0:
            rm = rm + "You killed " + tName + "! May their soul rest in peace until they respawn.\n"
            self.prop['dead'] = True
        self.rawstats['health'] = tHP
        mm.save_playerlist()
        return rm
        
    def attack(self, target):
        print("self name: " + self.name)
        print("target name: " + target.name)
        rm = ""
        if self == target:
            return False, "- Cannot attack self."
        critHit = False
        lewdHit = False
        hit = False
        canHit = False
        aLoc = self.stats['location']
        dLoc = target.stats['location']
        if aLoc != dLoc:
            return False, "- Your target isn't in the same room as you. You are in room " + str(aLoc) + " but they are in room " + str(dLoc) + "."
        battlelogPath = "C:/Users/Administrator/Desktop/KALEVBOT/important/battlelog.txt"
        if target.id and self.id:
            with open(battlelogPath, "r") as f:
                lines = [line.rstrip('\n') for line in f]
            aPrev = self.id + ":" + target.id
            aOppo = target.id + ":" + self.id
            if aPrev in lines:
                return False, "- You cannot attack this person because you attacked them already"
            elif aOppo in lines:
                lines.remove(aOppo)
                lines.append(aPrev)
            else:
                lines.append(aPrev)
            with open(battlelogPath, 'w') as f:
                for s in lines:
                    f.write(str(s) + "\n")
                    
            rm = rm + "+ Ready to strike!\n"
                    
            aSpeed = self.stats['speed']
            dSpeed = target.stats['speed']
            missChance = 0.06 + ((dSpeed - (aSpeed * 1.1)) * 0.015)
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
                rm = rm + "- MISS!"
                return False, rm

            aAtk = self.stats['attack']
            dDef = target.stats['defense']
            dArP = 0.55 #temporary
            
            randomVar = random.uniform(aAtk/3, aAtk) + random.uniform(aAtk/3, aAtk)
            dif =  randomVar / (aAtk * 2)
            if dif < 0.20:
                hitType = "- A poor hit"
            elif dif < 0.40:
                hitType = "A decent hit"
            elif dif < 0.70:
                hitType = "A good hit"
            elif dif < 0.90:
                hitType = "A great hit!"
            else:
                hitType = "+ An excellent hit"
            damage = (randomVar / 1.7) - (dDef / 2 * random.uniform(0.50, dArP))
            
            if critRoll < critChance:
                rm = rm + "+ CRITICAL HIT! DOUBLE DAMAGE!\n"
                damage = aAtk * 2 / 1.5 - (dDef / 2 * random.uniform(0.50, dArP))
                damage = damage * 2
            else:
                rm = rm + hitType + "\n"

            if damage < 2:
                damage = 2
                rm = rm + "- Damage was under 2, setting damage to guaranteed 2\n"

            print("self name: " + self.name)
            print("target name: " + target.name)
            opinion = target.deal_damage(damage)
            rm = rm + opinion
            oDead = target.prop.get('dead', False)
            if oDead:
                weapon = self.rawstats['weapon']
                wP = weapon.prop
                if wP.get('sting', False):
                    o = weapon.modification[wP['stingpos'][wP['stingnum']]]
                    if o < 7:
                        c = 1
                    else:
                        cp = o ** (1/float(2.2))
                        cp = cp - 2.25
                        c = 1 - cp
                    roll = random.uniform(0, 1)
                    if roll <= c:
                        o += 1
                        self.rawstats['weapon'].modification[wP['stingpos'][wP['stingnum']]] = o
                        rm += "- The blood on your weapon glows brightly\n"
                        rm += "- " + wP['stingpos'][wP['stingnum']] + " increased by 1"
                        wP['stingnum'] += 1
                        if wP['stingnum'] == len(wP['stingpos']):
                            wP['stingnum'] = 0
                        self.invstats = self.inv_changes()
                        self.stats = self.calculate_stats()
                    else:
                        rm += "- The blade shimmers, but nothing happens\n"
            
            
            mm.save_playerlist()
            
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
        
        sNow = self.rawstats['location']
        self.rawstats['furthest'] += 1
        self.rawstats['location'] = self.rawstats['furthest']
        sNew = self.rawstats['location']

        if len(roomlist) == sNew:
            newroom = room.Room()
            roomlist.append(newroom)
            newroom.make_desc()
            with open('important/rooms.txt', 'wb') as f: #open the file named fileName
                pickle.dump(roomlist, f) #Pickle and update the stats file
            rm = "\n! You are the first person to enter this room"
        ident = roomlist[sNew].get_desc()

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
        if targetpool != '':
            gotItem = mm.scavenge(targetpool)
            if gotItem != None:
                rm += '+ The soul of the game developer calls down to you and gives you an item from the pool ' + targetpool + "\n"
                rm += '+ You got ' + gotItem.sg + "\n"
                st, rma = self.add_item(gotItem)
                rm += rma
            return gotItem, rm
        else:
            return None, ""

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
            return False, "- You do not have any room in your inventory\n"

        self.inv[freeSlot] = item
        item.set_entity(self)
        return True, "+ Added item " + item.name + " to slot " + str(freeSlot+1) + "\n"

    def use_slot(self, slot):
        slot = slot - 1
        if slot < 0:
            return False, False, "- Slots smaller than 1 do not exist"
        try:
            isFree = self.inv[slot]
        except:
            return False, False, "- That slot is outside the range of your inventory"
        if isFree == None:
            return False, False, "- That slot is empty"

        state, toReturn, done = isFree.use_item()
        if done:
            self.inv[slot] = None
        self.stats = self.calculate_stats()
        mm.save_playerlist()
        return True, state, toReturn
    
    def drop_slot(self, slot):
        slot = slot - 1
        if slot < 0:
            return "- Slots smaller than 1 do not exist"
        try:
            isFree = self.inv[slot]
        except:
            return "- That slot is outside the range of your inventory"
        if isFree == None:
            return "- That slot is empty"

        self.inv[slot] = None
        if isFree.prop.get("soul", False) == True:
            mm.save_playerlist()
            return "- " + isFree.name + " is Soulbound and was destroyed on drop"
        roomlist = mm.rooms
        sNow = self.stats['location']
        rNow = roomlist[sNow]
        rNow.itemlist.append(isFree)
        with open('important/rooms.txt', 'wb') as f: #open the file named fileName
            pickle.dump(roomlist, f)
        mm.save_playerlist()
        return "Dropped " + isFree.name + " into room " + str(sNow)

    def inspect_slot(self, slot):
        slot = slot - 1
        if slot < 0:
            return "- Slots smaller than 1 do not exist"
        try:
            isFree = self.inv[slot]
        except:
            return "- That slot is outside the range of your inventory"
        if isFree == None:
            return "- That slot is empty"

        rm = ""
        rm += "+ " + isFree.name + "\n"
        rm += "--- " + isFree.desc + "\n"
        rm += "In inventory slot " + str(slot+1) + "\n"
        if isFree.usable:
            rm += "Can be used.\n"
        else:
            rm += "Can be equipped.\n"
            for i, k in list(isFree.modification.items()):
                if k < 0:
                    j = "- Decreases"
                else:
                    j = "+ Increases"
                rm += j + " stat " + i + " by " + str(abs(k)) + "\n"
        rm += "\n" + isFree.usehelp + "\n"
        return rm

    def inv_changes(self):
        invItems = ['tongue', 'torso', 'legs', 'weapon', 'ring1', 'ring2']
        modList = ['maxhealth', 'attack', 'defense', 'speed', 'luck']
        toModify = {"maxhealth": 0, "attack": 0, "defense": 0, "speed": 0, "luck": 0}
        for i in invItems:
            if self.rawstats[i] == 0:
                continue
            for y in modList:
                toModify[y] += self.rawstats[i].modification.get(y, 0)

        return toModify

    def calculate_stats(self):
        aAdd = dict(self.rawstats)
        bAdd = self.invstats
        for i in bAdd:
            aAdd[i] += bAdd[i]
        print(aAdd)
        return aAdd
    
    def has_slot(self):
        if None in self.inv:
            return True
        else:
            return False

    def equip(self, tItem, slot):
        dg = ""
            
        if slot == "ring":
            if self.rawstats["ring2"] == 0 and self.rawstats["ring1"] == 0:
                slot = "ring1"
            elif self.rawstats["ring2"] == 0:
                slot = "ring2"
            else:
                slot = "ring1"
                
        prevItem = self.rawstats[slot]
        
        if prevItem != 0:
            if prevItem.prop.get('bind', False) == True:
                self.stats = self.calculate_stats()
                mm.save_playerlist()
                return prevItem, "- " + "Your currently equipped " + prevItem.name + " is cursed and cannot be removed", True
                
        self.rawstats[slot] = tItem
        print("Equipping " + tItem.sg)
        self.invstats = self.inv_changes()
        self.stats = self.calculate_stats()
        mm.save_playerlist()
        return prevItem, "Equipped " + tItem.name + " to equipment slot " + slot, False
    
    def unequip(self, slot):
        prevItem = self.rawstats[slot]
        if prevItem == 0:
            return prevItem, "No equipment in that slot"
        if prevItem.prop.get('bind', False) == True:
            self.stats = self.calculate_stats()
            mm.save_playerlist()
            return prevItem, "- " + "Your currently equipped " + prevItem.name + " is cursed and cannot be removed"
        if self.has_slot():
            self.rawstats[slot] = 0
            st, rm = self.add_item(prevItem)
            self.stats = self.calculate_stats()
            self.invstats = self.inv_changes()
            self.stats = self.calculate_stats()
            mm.save_playerlist()
            return prevItem, "Unequipped " + prevItem.name + " from equipment slot " + slot + "\n" + rm
        else:
            return prevItem, "You don't have room in your inventory to unequip " + prevItem.name + " from equipment slot " + slot

    def equip_slot(self, slot):
        slot = slot - 1
        rm = ""
        if slot < 0:
            return "- Slots smaller than 1 do not exist"
        try:
            isFree = self.inv[slot]
        except:
            return "- That slot is outside the range of your inventory"
        if isFree == None:
            return "- That slot is empty"
        eSlot = isFree.slot
        prevItem, rma, notDone = self.equip(isFree, eSlot)
        rm += rma + "\n"
        if notDone:
            pass
        elif prevItem != 0:
            self.inv[slot] = prevItem
            rm += "Previously equipped " + prevItem.name + " has been put into inventory slot " + str(slot+1)
        else:
            self.inv[slot] = None
            
        self.invstats = self.inv_changes()
        self.stats = self.calculate_stats()

        mm.save_playerlist()
        
        return rm

    
    def take_room(self, room_slot):
        room_slot -= 1
        rm = ""
        roomlist = mm.rooms
        sLoc = self.rawstats['location']
        rm += "You are in room {}\n".format(sLoc)
        sRoom = roomlist[sLoc]
        srItems = sRoom.itemlist
        try:
            rItem = srItems[room_slot]
        except:
            rm += "- Invalid slot"
            return False, rm
        sts, rd = self.add_item(rItem)
        rm += rd
        if sts == False:
            rm += "- Couldn't add item"
            return False, rm
        roomlist[sLoc].itemlist.pop(room_slot)
        with open('important/rooms.txt', 'wb') as f:
            pickle.dump(roomlist, f)
        return True, rm
        