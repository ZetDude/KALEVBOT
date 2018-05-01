from discord.ext import commands

class ImportantCog():
    "Includes important commands users should use"
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Important Commands"

    @commands.command(name='about', aliases=['info'],
                      help="Learn more about the bot and where to support it.",
                      brief="Learn more about the bot.")
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
Want me on your own server? Use <{0}invite> to get the link!
Thanks to xithiox and pecan for the help they have already provided!
""".format(ctx.prefix)
        await ctx.send(about_text)

    @commands.command(name='invite', aliases=['inv'],
                      help="Get URL for adding bot to a Discord server.",
                      brief="Get bot invite URL.")
    async def invite(self, ctx):
        await ctx.send(("<https://discordapp.com/oauth2/authorize?client_id="
                        f"{ctx.bot.user.id}&scope=bot>"))
 
    @commands.command(name='ping', aliases=['pong'],
                      help="Pong!",
                      brief="Pong!")
    async def ping(self, ctx):
        ping_message = "Pong!" if ctx.invoked_with == "ping" else "Ping!"
        resp = await ctx.send(f'{ping_message} Loading...')
        diff = resp.created_at - ctx.message.created_at
        totalms = 1000*diff.total_seconds()
        await resp.edit(content=f'{ping_message} Response Time: {totalms}ms.')

    #@commands.command(name='help')
    #async def help(self, ctx):
    
    #help is handled by the built-in system, for now...

def setup(bot):
    bot.add_cog(ImportantCog(bot))
