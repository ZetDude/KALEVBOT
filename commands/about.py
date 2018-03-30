"""An about command explaining the uses of the bot and where to support it"""

import maincore as core

help_info = {"use": "Learn more about the bot and where to support it",
             "param": "{}about",
             "perms": None,
             "list": "Learn more about the bot"}
alias_list = ['about', 'info']

def run(message, prefix, alias_name):
    del alias_name
    about_text = """
Hi! I am KalevBot, a bot with no certain purpose!
I was initially created by ZetDude, and I consist of 100% spaghetti.
I am here to help with some minor things, and also to have fun.
But what are my commands, you might wonder?
Just type <{0}help> to see!

I am made in python 3 using the discord.py API wrapper.
You can help develop the bot at:
<https://github.com/ZetDude/KALEVBOT/>
Thanks to xithiox and pecan for the help they have already provided!
""".format(prefix)
    core.send(message.channel, about_text)
