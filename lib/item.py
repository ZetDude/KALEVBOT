class Item:
    def __init__(self, preset):
        self.entity = None
        self.name = preset.get('name', 'unnamed item')
        self.desc = preset.get('name', '')
        self.usable = preset.get('usable', False)
        self.on_use = preset.get('on_use', lambda: None)
        self.equippable = preset.get('equippable', False)
        self.on_equip = preset.get('on_equip', lambda: None)
    def set_entity(self, entity):
        self.entity = entity
