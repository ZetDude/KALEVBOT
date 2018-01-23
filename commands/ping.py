import asyncio

import maincore as core

@asyncio.coroutine
def run(message, prefix, aliasName):
    del prefix
    latency = round(core.cl.latency * 1000)
    pong = "Pong!" if aliasName == "ping" else "Ping!"
    yield from message.channel.send("🏓  {} {} ms latency".format(pong, latency))

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

def aliasName():
    return ['ping', 'pong']
