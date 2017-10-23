import importlib.machinery
import os
import sys
import asyncio
import datetime

import maincore as core

@asyncio.coroutine
def run(message, prefix, alias):
    cur = datetime.datetime.utcnow()
    sent = yield from message.channel.send("🏓 The ball is flying...")
    diffFrom = int((cur - message.created_at).total_seconds() * 1000)
    diffTo = int((sent.created_at - cur).total_seconds() * 1000)
    yield from sent.edit(content="🏓 Pong! {}ms from, {}ms to".format(diffFrom, diffTo))

def help_use():
    return "Pong!"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "ping"

def help_perms():
    return 0

def help_list():
    return "Pong!"

def alias():
    return ['ping']
