from discord.ext import commands

class HybridConverter(commands.Converter):
    async def convert(self, ctx, argument):
        got_target = None
        all_users = ctx.bot.users
        all_members = ctx.guild.members

        ### CONVERT TO MEMBER FIRST
        # Lookup by ID
        got_target = [x for x in all_members if str(x.id) == str(argument)]
        if got_target:
            return got_target[0]

        # Lookup by mention
        got_target = [x for x in all_members if x.mention == str(argument)]
        if got_target:
            return got_target[0]

        # Lookup by name#discrim
        got_target = [x for x in all_members if str(x) == str(argument)]
        if got_target:
            return got_target[0]

        # Lookup by name
        got_target = [x for x in all_members if x.name == str(argument)]
        if got_target:
            return got_target[0]

        # Lookup by nickname
        got_target = [x for x in all_members if x.nick == str(argument)]
        if got_target:
            return got_target[0]

        ### FALLBACK TO GLOBAL USER SEARCH
        # Lookup by ID
        got_target = [x for x in all_users if str(x.id) == str(argument)]
        if got_target:
            return got_target[0]

        # Lookup by mention
        got_target = [x for x in all_users if x.mention == str(argument)]
        if got_target:
            return got_target[0]

        # Lookup by name#discrim
        got_target = [x for x in all_users if str(x) == str(argument)]
        if got_target:
            return got_target[0]

        # Lookup by name
        got_target = [x for x in all_users if x.name == str(argument)]
        if got_target:
            return got_target[0]

        ### FALLBACK TO CASE-INSENSITIVE MEMBER SEARCH
        # Lookup by name#discrim
        got_target = [x for x in all_members if str(x).lower() == str(argument).lower()]
        if got_target:
            return got_target[0]

        # Lookup by name
        got_target = [x for x in all_members if x.name.lower() == str(argument).lower()]
        if got_target:
            return got_target[0]

        # Lookup by nickname
        got_target = [x for x in all_members if x.nick.lower() == str(argument).lower()]
        if got_target:
            return got_target[0]

        ### FALLBACK TO CASE-INSENSITIVE GLOBAL USER SEARCH
        # Lookup by name#discrim
        got_target = [x for x in all_users if str(x).lower() == str(argument).lower()]
        if got_target:
            return got_target[0]

        # Lookup by name
        got_target = [x for x in all_users if x.name.lower() == str(argument).lower()]
        if got_target:
            return got_target[0]

        raise commands.BadArgument(f"Member \"{argument}\" not found")
