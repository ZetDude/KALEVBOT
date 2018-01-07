import os
import sys
import asyncio

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def is_me(m):
    """Return if given user is the bot. Needed for deleting the bot's messages"""
    return m.author == core.cl.user

@asyncio.coroutine
def run(message, prefix, aliasName):
    commandLength = len(prefix + aliasName)
    operatableString = message.content[commandLength:].strip()
    deleteAmount = 0
    try:
        deleteAmount = int(operatableString)
        yield from message.channel.purge(limit=deleteAmount,
                                         check=is_me,
                                         bulk=False)
        yield from message.author.send("Deleted " + str(deleteAmount) + " messages")
    except ValueError:
        yield from message.channel.send("Not an int")

def help_use():
    return "Delete the amount of messages from the bot as is specified"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "del"

def help_perms():
    return 3

def help_list():
    return "Delete messages from the bot"

def aliasName():
    return ['del', 'delete']
