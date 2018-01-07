import os
import sys
import discord
import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def run(message, prefix, aliasName):
    if message.content.strip() == prefix + aliasName:
        emotes = core.cl.emojis
        emoteBlocks = chunks(emotes, 50)
        for i in emoteBlocks:
            emoteJoin = "".join([str(x) for x in i])
            core.send(message.channel, emoteJoin)
    else:
        cmdlen = len(prefix + aliasName)
        opstring = message.content[cmdlen:].strip().strip(':')
        pos = discord.utils.get(core.cl.emojis, name=opstring)
        core.send(message.channel, str(pos))

def help_use():
    return "Get all the emotes the bot can use"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "emote"

def help_perms():
    return 0

def help_list():
    return "Get all the emotes the bot can use"

def aliasName():
    return ['emote']
