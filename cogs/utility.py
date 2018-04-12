import discord
from discord.ext import commands

class UtilityCog():
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Utility Commands"

    @commands.command(name='about', aliases=['info'])
    async def about(self, ctx):
        about_text = """
Hi! I am KalevBot, a bot with no certain purpose!
I was initially created by ZetDude, and I consist of 100% spaghetti.
I am here to help with some minor things, and also to have fun.
But what are my commands, you might wonder?
Just type <{0}help> to see!

I am made in python 3 using the discord.py API wrapper.
You can help develop the bot at:
<https://github.com/ZetDude/KALEVBOT/>
Or join the development Discord server:
<https://discord.gg/b89UkN5>
Thanks to xithiox and pecan for the help they have already provided!
""".format(ctx.prefix)
        await ctx.send(about_text)

def setup(bot):
    bot.add_cog(UtilityCog(bot))

