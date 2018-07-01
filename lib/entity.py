class ActionSuccesful(Exception):
    pass

class Entity:
    def __init__(self, preset):
        self.name = preset.get('name', '')
        self.idnum = preset.get('id', 0)
        self.inv = Inventory(preset.get('invsize', 10))
        self.inv.set_entity(self)
        self.eqp = EquipmentInv()
        self.eqp.set_entity(self)
    def __str__(self):
        return self.name

class Inventory:
    def __init__(self, size):
        self.entity = None
        self.size = size
        self.inv = [None] * size
    def set_entity(self, entity):
        self.entity = entity
    def add(self, item):
        for i, item_iter in enumerate(self.inv):
            if item_iter is None:
                self.inv[i] = item
                item.set_entity(self.entity)
                raise ActionSuccesful(f'Added item {item} to slot {i}')
        raise IndexError("No room in inventory")
    def drop(self, slot):
        pass
    def use(self, slot):
        pass

class EquipmentInv:
    def __init__(self):
        self.entity = None
        self.inv = {
            'legs': None,
            'ring1': None,
            'ring2': None,
            'tongue': None,
            'torso': None,
            'weapon': None
        }
    def set_entity(self, entity):
        self.entity = entity
    def equip(self, equipment):
        pass
    def unequip(self, slot):
        pass
    def stat_bonus(self):
        pass
