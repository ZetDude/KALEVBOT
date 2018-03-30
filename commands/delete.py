import asyncio
import maincore as core

help_info = {"use": "Delete the amount of messages from the bot as is specified",
             "param": "{}del <*AMOUNT>\n<*AMOUNT>: Number of messages to delete",
             "perms": "message",
             "list": "Delete messages from the bot"}
alias_list = ['del', 'delete']

def is_me(m):
    """Return if given user is the bot. Needed for deleting the bot's messages"""
    return m.author == core.cl.user

@asyncio.coroutine
def run(message, prefix, alias_name):
    command_length = len(prefix + alias_name)
    operatable_string = message.content[command_length:].strip()
    delete_amount = 0
    try:
        delete_amount = int(operatable_string)
        yield from message.channel.purge(limit=delete_amount,
                                         check=is_me,
                                         bulk=False)
        yield from message.author.send("Deleted " + str(delete_amount) + " messages")
    except ValueError:
        yield from message.channel.send("Not an int")
