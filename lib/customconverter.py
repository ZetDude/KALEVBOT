from discord.ext import commands
import discord

class HybridConverter(commands.Converter):
    async def convert(self, ctx, argument):
        got_target = None
        try:
            got_target = await commands.MemberConverter().convert(ctx, argument)
            return got_target
        except discord.DiscordException:
            try:
                got_target = await commands.UserConverter().convert(ctx, argument)
                return got_target
            except discord.DiscordException:
                raise
