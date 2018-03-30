import maincore as core

help_info = {"use": "PM all the commands to the user or"+
                    "show more specific help about a single command",
             "param": """{0}help (COMMAND)
= {0}help here
(COMMAND): The command to get more specific infomation about""",
             "perms": None,
             "list": "Google the specified subject"}
alias_list = ['help', 'halp', 'h', 'commands', 'command']

def run(message, prefix, alias_name):
    if message.content.strip().lower() == (prefix + alias_name).lower():
        helptext = core.helptext
        core.send(message.author, helptext)
        core.send(message.channel, "Alright " + message.author.mention + ", check your DMs")
        return
    elif message.content.strip().lower() == (prefix + alias_name + " here").lower():
        helptext = core.helptext
        core.send(message.channel, helptext)
        return
    cmdlen = len(prefix + alias_name)
    opstring = message.content[cmdlen:].strip()
    helptext = core.compose_help(opstring)
    core.send(message.channel, helptext)
