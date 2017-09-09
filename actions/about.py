import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader.load_module('basic')

def run(message, prefix, alias):
    rpgPrefix = rpg.rpgPrefix
    aboutText = """```md
Welcome to KalevRPG
This is a little text RPG-battle-explore-dungeon-rogue-like thing, whatever that is.
To get started with the game, type <{0}join>.
You might also read those instructions, to know how to <{0}upgrade>
Then, you can start exploring on your merry way using <{0}explore>.
If you encounter something you can <{0}take> it, <{0}attack> it, or do some other things.
If you don't know what an item does, just <{0}inspect> it. You can then <{0}equip> it or
<{0}use> it. Or if you decided you don't like you can just <{0}unequip> and/or <{0}drop> it.
If you want to get real evil, you can also kill other players, and take their stuff.

That's pretty much it!
This game was designed as a programming challenge, but then it got way out of hand, 
and now there are people behind it who are helping the dev (its crazy)

More to come soon, ~~if I can figure out how my own code works~~
```""".format(rpgPrefix)
    return "p", [message.author, aboutText, message.channel, "Alright " + message.author.mention + ", Check your DMs"]

def help_use():
    return "Learn more about the rpg"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "about"

def help_perms():
    return 0

def help_list():
    return "Learn more about the rpg"

def alias():
    return ['about', 'info', 'action', 'aboot']
