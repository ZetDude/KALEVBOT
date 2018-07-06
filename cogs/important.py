from discord.ext import commands
import discord

class ImportantCog():
    "Includes important commands users should use"
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Important"

    @commands.command(name='about', aliases=['info'],
                      help="Learn more about the bot and where to support it.",
                      brief="Learn more about the bot.")
    async def about(self, ctx):
        embed = discord.Embed(
            title="Hi! I am KalevBot, a bot with no certain purpose!",
            colour=0x0000ff,
            url="https://discord.gg/b89UkN5",
            description=(f"I was initially created by ZetDude, and I consist of 100% spaghetti, "
                         f"written in python3 using discord.py.\n"
                         f"I am here to help with some minor things, and also to have fun.\n"
                         f"But what are my commands, you might wonder?"
                         f"Just type <{ctx.prefix}help> to see!\nWant me on your server?"
                         f"Use <{ctx.prefix}!invite> to get the link.")
            )
        embed.set_thumbnail(
            url=ctx.bot.user.avatar_url
            )
        embed.set_footer(
            text="Thanks to xithiox and pecan for the help they've provided!"
        )
        embed.add_field(
            name="How to help!",
            value=("[GitHub repository](https://github.com/ZetDude/KALEVBOT/)\n"
                   "[Development discord server](https://discord.gg/b89UkN5)"), inline=True)

        await ctx.send(embed=embed)

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
        await resp.edit(content=f'\U0001F3D3 {ping_message} Response Time: {totalms}ms.')

def setup(bot):
    bot.add_cog(ImportantCog(bot))
