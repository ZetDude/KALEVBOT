import importlib.machinery
import os
import sys
import pickle
import math
import random
import string
import inspect
import asyncio
import discord

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start+n]

@asyncio.coroutine
def run(message, prefix, alias):
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()
    mode = ""
    python = '```py\n{}\n```'
    try:
        result = eval(opstring)
        if inspect.isawaitable(result):
            result = yield from result
    except Exception as e:
        yield from message.channel.send(python.format(type(e).__name__ + ': ' + str(e)))
    chunked = chunks(str(result), 1980)
    print(chunked)
    for i in chunked:
        yield from message.channel.send("```{}\n{}\n```".format(mode, i))
    

def help_use():
    return "Run code"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "eval"

def help_perms():
    return 10

def help_list():
    return "Run code"

def alias():
    return ['eval']