import random
import basic as mm
class Room:
    def __init__(self, desc="An unidentified room", itemlist=None):
        self.desc = desc
        if itemlist is None:
            self.itemlist = []
        else:
            self.itemlist = itemlist

    def make_desc(self):
        material = ["brick", "clean brick", "some sort of shiny brick",
            "what seems like solid gold", "cracked brick",
            "an unknown material", "slightly glowing brick",
            "stone"]

        atmos = ["an eerie", "a wet", "a dry", "a quiet", "a nice"]
        ident = "The room is made out of " + random.choice(material) + ". It has " + random.choice(atmos) + " atmosphere to it"
        self.desc = ident
        
    def get_desc(self):
        rm = ""
        rm += self.desc + "\n"
        if len(self.itemlist) > 0:
            rm += "The room contains: "
            for i in range(len(self.itemlist)):
                rm += str(i+1) + ": " + self.itemlist[i].sg + ", "
            rm += "\n(%take [NUMBER SEEN BEFORE ITEM] to take an item)"
        ##players = mm.playerlist
        ##for i in players.values()
        return rm
            