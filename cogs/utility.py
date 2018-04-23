import os

import discord
from discord.ext import commands


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def get_free_space_mb(dirname):
    """Return folder/drive free space (in megabytes)."""
    #if platform.system() == 'Windows':
        #free_bytes = ctypes.c_ulonglong(0)
        #ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        #return free_bytes.value
    st = os.statvfs(dirname)
    return st.f_bavail * st.f_frsize

class UtilityCog():
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Utility Commands"

    @commands.command(name='emote', aliases=['e'],
                      help="Get all the emotes the bot can use or a specific emote.",
                      brief="Get an emote or all of them.")
    async def emote(self, ctx, emote_lookup=None):
        if emote_lookup is None:
            emotes = ctx.bot.emojis
            emote_block = chunks(emotes, 45)
            for i in emote_block:
                emote_join = " ".join([str(x) for x in i])
                await ctx.send(emote_join)
        else:
            emote_lookup = emote_lookup.strip(':')
            pos = discord.utils.get(ctx.bot.emojis, name=emote_lookup)
            await ctx.send(str(pos))

    @commands.command(name='ipa', aliases=[],
                      help="Display multiple options for getting the IPA chart and/or keyboard.",
                      brief="Get the link for the IPA chart.")
    async def ipa(self, ctx):
        await ctx.send("""The IPA (International Phonetic Alphabet) chart in various forms:

<http://www.ipachart.com/> Simple version of the graph with sounds
<http://westonruter.github.io/ipa-chart/keyboard/> A keyboard site for writing all things IPA using the on-screen buttons
<https://web.uvic.ca/ling/resources/ipa/charts/IPAlab/IPAlab.htm> A more detailed version of the alphabet with interactive buttons
""")

    @commands.command(name='server', aliases=['guild', 'analyze'],
                      help="Analyze the current guild",
                      brief="Analyze the current guild")
    async def server(self, ctx):
        current_guild = ctx.guild
        final_msg = ""
        final_msg += "You are in \"**{}**\", a guild owned by **{}**\n".format(current_guild.name,
                                                                               current_guild.owner.name)
        final_msg += "It has __{}__ members,\n".format(current_guild.member_count)
        member_list = current_guild.members
        humans = 0
        bots = 0
        for i in member_list:
            if i.bot:
                bots += 1
            else:
                humans += 1
        final_msg += "__{}__ of which are humans, and __{}__ are bots\n".format(humans, bots)
        final_msg += "and I'm on the guild, which is the best part!"
        await ctx.send(final_msg)
    
    #@commands.command(name='tag', aliases=['faq', 't'],
    #                  help="Answer FAQ",
    #                  brief="Answer FAQ")
    #async def tag(self, ctx):
    #TODO: tag command using database

    @commands.command(name='status', aliases=['test'],
                      help="Check the status and information of the bot, such as run time and disk space.",
                      brief="Show if the bot is still working.")    
    async def status(self, ctx):
        #difference = core.get_timer()
        diskspace = get_free_space_mb("/")
        diskspaceg = diskspace / 1024 / 1024 / 1024
        final_msg = ""
        final_msg += "It's working!"
        #final_msg += "I have been running for " + str(difference)
        final_msg += "\nApproximate disk space left for bot: {0:.2f} GB ({1} bytes)".format(diskspaceg,
                                                                                            diskspace)
        final_msg += "\nI am present in " + str(len(ctx.bot.guilds)) + " guilds."
        await ctx.send(final_msg)

def setup(bot):
    bot.add_cog(UtilityCog(bot))
