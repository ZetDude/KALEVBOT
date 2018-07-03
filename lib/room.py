class Room:
    def __init__(self, preset):
        self.desc = preset.get("desc", make_desc())

    def make_desc(self):
        material = ["brick", "clean brick", "some sort of shiny brick",
                    "what seems like solid gold", "cracked brick",
                    "an unknown material", "slightly glowing brick",
                    "stone"]

        atmos = ["an eerie", "a wet", "a dry", "a quiet", "a nice"]
        ident = "The room is made out of " + random.choice(material) + ". It has " + random.choice(atmos) + " atmosphere to it"
        self.desc = ident