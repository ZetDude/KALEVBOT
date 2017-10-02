import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')
loader2 = importlib.machinery.SourceFileLoader('basic', sp + '/basic.py')
rpg = loader2.load_module('basic')

def run(message, prefix, alias):
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
    return "m", [message.channel, aboutText]

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

def alias():
    return ['about', 'info']
