import discord
import maincore as core

help_info = {"use": "Get all the emotes the bot can use or a specific emote",
             "param": "{}emote (EMOTE)\n(EMOTE): The name of the emote",
             "perms": None,
             "list": "Get an emote or all of them"}
alias_list = ['emote', 'e']

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def run(message, prefix, alias_name):
    if message.content.strip() == prefix + alias_name:
        emotes = core.cl.emojis
        emote_block = chunks(emotes, 45)
        for i in emote_block:
            emote_join = " ".join([str(x) for x in i])
            core.send(message.channel, emote_join)
    else:
        cmdlen = len(prefix + alias_name)
        opstring = message.content[cmdlen:].strip().strip(':')
        pos = discord.utils.get(core.cl.emojis, name=opstring)
        core.send(message.channel, str(pos))
