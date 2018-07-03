import random

class Room:
    def __init__(self, preset):
        self.desc = preset.get("desc", self.make_desc())
        self.type = preset.get("type", 1)
        # [entrance, empty]
        room_contents = ["= This room contains everybody who hasn't entered the dungeon yet =",
                         "= The room is empty = "]
        self.typedesc = room_contents[self.type]

    def make_desc(self):
        material = ["brick", "clean brick", "some sort of shiny brick",
                    "what seems like solid gold", "cracked brick",
                    "an unknown material", "slightly glowing brick",
                    "stone"]

        atmos = ["an eerie", "a wet", "a dry", "a quiet", "a nice"]
        ident = (f"The room is made out of {random.choice(material)}. "
                 f"It has {random.choice(atmos)} atmosphere to it")
        return ident
