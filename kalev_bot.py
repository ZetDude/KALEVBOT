"""This is the main instance that does all the hard work.
Please run this file to run the actual bot itself"""
import errno
import os
import sys
import time

import discord  # Discord API
from discord.ext import commands
from lib import obot

import maincore as dc

bot = commands.Bot(command_prefix=commands.when_mentioned_or(obot.bot_prefix),
                   owner_id=obot.owner_id)

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
print(sp)
print(sp + "/kalev_bot.py")
print("Now running main bot instance")

print("Launching bot, this might take a few seconds")
timer_start = time.time()

dir_make = ["actions", "important", "commands", "important/lucky"]
for i in dir_make:
    try:
        os.makedirs(i)
    except OSError as err:
        if err.errno != errno.EEXIST:
            raise

@bot.event
async def on_ready():
    timer_end = time.time()
    print("Launching of bot took {} seconds".format(timer_start - timer_end))
    dc.ready(bot)
    await bot.change_presence(activity=discord.Game(type=obot.gametype, name=obot.game),
                              status=discord.Status.online)
    servers = len(bot.guilds)
    users = len(bot.users)
    print(f"Serving {users} users in " + str(servers) +
          " server" + ("s" if servers > 1 else "") + ".")

@bot.event
async def on_message(message):
    if message.author != bot.user:
        if bot.user in message.mentions:
            ping_emoji = discord.utils.get(bot.emojis, id=362665760260227073)
            await message.add_reaction(ping_emoji)

    #if message.guild is None:
        #fse = str(message.channel)
    #else:
        #fse = message.channel.name + " in " + message.guild.name
    #if message.author.bot:
        #return
    await bot.process_commands(message)
    #elif message.content.startswith(obot.game_prefix):
        #async with message.channel.typing():
            #rpg.run(message)
        #print("rpg message detected\n-----------------")

    #await client.send_typing(message.channel)

if __name__ == '__main__':
    coglist = []
    for root, directories, files in os.walk("cogs"):
        for filename in files:
            filepath = os.path.join(root, filename)
            if filepath.endswith(".py"):
                coglist.append(filepath.split(".py")[0].replace("/", ".").replace("\\", "."))

    for cog in coglist:
        try:
            bot.load_extension(cog)
            print(f'Loaded {cog} successfully')
        except Exception as err:
            print(f"Failed to load cog: {cog}, ran into {err}")
            raise
    print("Loaded all cogs")
    bot.run(obot.token, bot=True, reconnect=True)
