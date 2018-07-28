from discord.ext import commands
import discord

class HybridConverter(commands.Converter):
    async def convert(self, ctx, argument):
        all_users = ctx.bot.users
        all_members = ctx.guild.members

        got_target = ([x for x in all_members if str(x.id) == str(argument)] or
                      [x for x in all_members if x.mention == str(argument)] or
                      [x for x in all_members if str(x) == str(argument)] or
                      [x for x in all_members if x.name == str(argument)] or
                      [x for x in all_members if x.nick == str(argument)] or
                      [x for x in all_users if str(x.id) == str(argument)] or
                      [x for x in all_users if x.mention == str(argument)] or
                      [x for x in all_users if str(x) == str(argument)] or
                      [x for x in all_users if x.name == str(argument)] or
                      [x for x in all_members if str(x).lower() == str(argument).lower()] or
                      [x for x in all_members if x.name.lower() == str(argument).lower()] or
                      [x for x in all_members if str(x.nick).lower() == str(argument).lower()
                       and x.nick is not None] or
                      [x for x in all_users if str(x).lower() == str(argument).lower()] or
                      [x for x in all_users if x.name.lower() == str(argument).lower()] or
                      None)
        if got_target:
            return got_target[0]
        else:
            try:
                return await ctx.bot.get_user_info(int(argument))
            except (ValueError, discord.NotFound):
                raise commands.BadArgument(f"Member \"{argument}\" not found")
