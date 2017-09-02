import random 
import bisect

class Item:
                def __init__(self, preset):
                                self.name = preset.get('name', '')
                                self.desc = preset.get('desc', '')
                                self.usable = preset.get('usable', False)
                                self.equipable = preset.get('equipable', False)
                                self.modification = preset.get('modification', {})
                                self.slot = preset.get('slot', '')
                                self.usehelp = preset.get('usehelp', '')
                                self.sg = preset.get('sg', 'a ' + self.name)
                                self.pl = preset.get('pl', self.name + 's')
                                self.prop = preset.get('prop', {}) 
                                self.entity = None

                def set_entity(self, entity):
                                self.entity = entity
                                if self.usable:
                                                self.usable.set_entity(self.entity)

                def use_item(self):
                                if self.usable:
                                                rm = "Item used."
                                                rm, done = self.usable.use_item()
                                                self.entity.stats = self.entity.calculate_stats()
                                                return True, rm, done
                                else:
                                                return False, "Item cannot be used", None

class HealingItem:
                def __init__(self, heal_value, message=False):
                                self.heal_value = heal_value
                                self.entity = None
                                self.message = message

                def set_entity(self, entity):
                                self.entity = entity

                def use_item(self):
                                self.entity.rawstats['health'] += self.heal_value
                                rda = ""
                                if self.message != False:
                                                rda = "\n" + self.message
                                return "Healed for " + str(self.heal_value) + " health" + rda, True

class SuperItem:
                def __init__(self, heal_value, message=False):
                                self.heal_value = heal_value
                                self.entity = None
                                self.message = message

                def set_entity(self, entity):
                                self.entity = entity

                def use_item(self):
                                self.entity.rawstats['health'] += self.heal_value
                                self.entity.rawstats['maxhealth'] += self.heal_value
                                self.entity.rawstats['attack'] += self.heal_value
                                self.entity.rawstats['defense'] += self.heal_value
                                self.entity.rawstats['speed'] += self.heal_value
                                self.entity.rawstats['luck'] += self.heal_value
                                rda = ""
                                if self.message != False:
                                                rda = "\n" + self.message
                                return "Increased all stats by " + str(self.heal_value) + rda, True

class CrystalItem:
                def __init__(self, stat):
                                self.stat = stat
                                self.entity = None

                def set_entity(self, entity):
                                self.entity = entity

                def use_item(self):
                                self.entity.rawstats[self.stat] += 1
                                return "You broke the crystal, " + self.stat + " incereased by one", True

class SimpleWeaponEquip:
                def __init__(self, aVal):
                                self.modify['attack'] = aVal
                                self.entity = None
                                self.slot = "weapon"

                def set_entity(self, entity):
                                self.entity = entity

def get_itemlist():
                return it

def get_pools():
                return pl

def getitem(breakpoints,items):
                score = random.random() * breakpoints[-1]
                i = bisect.bisect(breakpoints, score)
                return list(items)[i]

def getbreak(weight):
                items = weight.keys()
                mysum = 0
                breakpoints = [] 
                for i in items:
                                mysum += weight[i]
                                breakpoints.append(mysum)
                return breakpoints

def rweight(weight):
                items = weight.keys()
                breakpoints = getbreak(weight) 
                gotItem = getitem(breakpoints,items)
                return gotItem
                



it = {'health potion': {'name': 'Health potion',
                                                                                                'desc': 'A bottle of shimmering red liquid',
                                                                                                'usehelp': 'Drink to restore health',
                                                                                                'usable': HealingItem(3)},
                                'speed crystal': {'name': 'Speed crystal',
                                                                                                'desc': 'A tiny crystal sparkling with blue light',
                                                                                                'usehelp': 'Use to increase speed a bit',
                                                                                                'usable': CrystalItem('speed')},
                                'damage crystal': {'name': 'Damage crystal',
                                                                                                'desc': 'A tiny crystal sparkling with orange light',
                                                                                                'usehelp': 'Use to increase attack damage a bit',
                                                                                                'usable': CrystalItem('attack')},
                                'defense crystal': {'name': 'Defense crystal',
                                                                                                'desc': 'A tiny crystal sparkling with green light',
                                                                                                'usehelp': 'Use to increase defense a bit',
                                                                                                'usable': CrystalItem('defense')},
                                'luck crystal': {'name': 'Luck crystal',
                                                                                                'desc': 'A tiny crystal sparkling with yellow light',
                                                                                                'usehelp': 'Use to increase luck a bit',
                                                                                                'usable': CrystalItem('luck')},
                                'health crystal': {'name': 'Health crystal',
                                                                                                'desc': 'A tiny crystal sparkling with red light',
                                                                                                'usehelp': 'Use to increase maximum health a bit',
                                                                                                'usable': CrystalItem('maxhealth')},
                                'super potion': {'name': 'Super potion',
                                                                                                'desc': 'A large bottle of raibow juice',
                                                                                                'usehelp': 'Use to make everyone salty',
                                                                                                'usable': SuperItem(100, "Tastes like cheating")},
                                'test sword': {'name': 'Test sword',
                                                                                                'desc': 'aaaa',
                                                                                                'usehelp': 'aaaa',
                                                                                                'modification': {'attack': 10},
                                                                                                'slot': 'weapon'},
                                'starter sword': {'name': 'Starter sword',
                                                                                                'desc': 'The sword given to you in the beginning of the game',
                                                                                                'usehelp': 'Soulbound',
                                                                                                'modification': {'attack': 4},
                                                                                                'slot': 'weapon',
                                                                                                'prop': {'soul': True}},
                                'starter torso': {'name': 'Starter chestplate',
                                                                                                'desc': 'The chestplate given to you in the beginning of the game',
                                                                                                'usehelp': 'Soulbound',
                                                                                                'modification': {'defense': 2},
                                                                                                'slot': 'torso',
                                                                                                'prop': {'soul': True}},
                                'starter legs': {'name': 'Starter leggings',
                                                                                                'desc': 'The leggings given to you in the beginning of the game',
                                                                                                'usehelp': 'Soulbound',
                                                                                                'modification': {'defense': 1, 'speed': 2},
                                                                                                'slot': 'legs',
                                                                                                'prop': {'soul': True}},
                                'starter ring': {'name': 'Starter ring',
                                                                                                'desc': 'The ring given to you in the beginning of the game',
                                                                                                'usehelp': 'Soulbound',
                                                                                                'modification': {'luck': 2},
                                                                                                'slot': 'ring',
                                                                                                'prop': {'soul': True}},
                                'cursed sword': {'name': 'The totally not cursed sword',
                                                                                                'desc': 'Try it!',
                                                                                                'usehelp': 'Curse of Binding',
                                                                                                'modification': {'attack': -4},
                                                                                                'slot': 'weapon',
                                                                                                'prop': {'bind': True}},
                                'kialtou': {'name': 'The Kialtou',
                                                                                                'sg': 'The Kialtou',
                                                                                                'pl': 'Kialtous',
                                                                                                'desc': 'A short dagger coated in blood\n--- The engraving on the blade reads:\n--- kialtoulo\'uta nakoron\n--- a quote in liakra pantakifosthulru',
                                                                                                'usehelp': 'Deathsting',
                                                                                                'modification': {'attack': 3, 'speed': 4, 'defense': -2},
                                                                                                'slot': 'weapon',
                                                                                                'prop': {'sting': True, 'stingpos': ["speed", "attack"], 'stingnum': 0}}
                        }

pl = {"testpool1": {None: 9,
                                                                                'health potion': 5,
                                                                                'speed crystal': 3,
                                                                                'damage crystal': 2,
                                                                                'defense crystal': 2,
                                                                                'luck crystal': 3,
                                                                                'health crystal': 5,
                                                                                }
                        } 

                                                                                                                        
                                                
