"""An about command explaining the uses of the bot and where to support it"""

import os
import sys
import maincore as core
import basic as rpg

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

def run(message, prefix, aliasName):
    del prefix
    del aliasName
    nPrefix = core.prefix
    rpgPrefix = rpg.rpgPrefix
    aboutText = """
Hi! I am KalevBot, a bot designed specifically for this guild!
I was designed by ZetDude, with a lot of help from xithiox, and I consist of 100% spaghetti.
I am here to help with the relay managment and some other minor things.
I also have a little text RPG-battle-explore-dungeon-rogue-like thing, whatever that is.
To learn about that, use <{1}about> instead.
But what are my commands, you might wonder?
Just type <{0}help> to see!

I am made in python using the discord.py API wrapper.
You can help develop the bot at:
<https://github.com/ZetDude/KALEVBOT/>
Thanks for all the support!
""".format(nPrefix, rpgPrefix)
    core.send(message.channel, aboutText)

def help_use():
    return "Learn more about the bot"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "about"

def help_perms():
    return 0

def help_list():
    return "Learn more about the bot"

def aliasName():
    return ['about', 'info']
