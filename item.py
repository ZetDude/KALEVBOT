import random 
import bisect

class Item:
    def __init__(self, preset):
        self.name = preset.get('name', '')
        self.desc = preset.get('desc', '')
        self.usable = preset.get('usable', '')
        self.usehelp = preset.get('usehelp', '')
        self.sg = preset.get('sg', 'a ' + self.name)
        self.pl = preset.get('pl', self.name + 's') 
        self.entity = None

    def set_entity(self, entity):
        self.entity = entity
        if self.usable:
            self.usable.set_entity(self.entity)

    def use_item(self):
        if self.usable:
            rm = "Item used."
            rm, done = self.usable.use_item()
            return True, rm, done
        else:
            return False, "Item cannot be used", None

class HealingItem:
    def __init__(self, heal_value):
        self.heal_value = heal_value
        self.entity = None

    def set_entity(self, entity):
        self.entity = entity

    def use_item(self):
        self.entity.stats['health'] += self.heal_value
        return "Healed for " + str(self.heal_value) + " health", True

class CrystalItem:
    def __init__(self, stat):
        self.stat = stat
        self.entity = None

    def set_entity(self, entity):
        self.entity = entity

    def use_item(self):
        self.entity.stats[self.stat] += 1
        return "You broke the crystal, " + self.stat + " incereased by one", True

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
                        'usehelp': 'Use to incerease speed a bit',
                        'usable': CrystalItem('speed')}
      }

pl = {"testpool1": {'health potion': 5,
                    'speed crystal': 3}
      } 

                              
            
