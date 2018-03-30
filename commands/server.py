import asyncio

help_info = {"use": "Analyze the current guild",
             "param": "{}guild",
             "perms": None,
             "list": "Analyze the current guild"}
alias_list = ['guild', 'analyze', 'server']

@asyncio.coroutine
def run(message, prefix, alias_name):
    del prefix
    del alias_name
    current_guild = message.guild
    final_msg = ""
    final_msg += "You are in \"**{}**\", a guild owned by **{}**\n".format(current_guild.name,
                                                                           current_guild.owner.name)
    member_list = current_guild.members
    final_msg += "It has __{}__ members,\n".format(current_guild.member_count)
    humans = 0
    bots = 0
    for i in member_list:
        if i.bot:
            bots += 1
        else:
            humans += 1
    final_msg += "__{}__ of which are humans, and __{}__ are bots\n".format(humans, bots)
    final_msg += "and I'm on the guild, which is the best part!"
    yield from message.channel.send(final_msg)
