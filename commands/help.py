import maincore as core

def run(message, prefix, aliasName):
    if message.content.strip().lower() == (prefix + aliasName).lower():
        helptext = core.helptext
        core.send(message.author, helptext)
        core.send(message.channel, "Alright " + message.author.mention + ", check your DMs")
        return
    elif message.content.strip().lower() == (prefix + aliasName + " here").lower():
        helptext = core.helptext
        core.send(message.channel, helptext)
        return
    cmdlen = len(prefix + aliasName)
    opstring = message.content[cmdlen:].strip()
    helptext = core.compose_help(opstring)
    core.send(message.channel, helptext)

def help_use():
    return "PM all the commands to the user or show more specific help about a single command"

def help_param():
    return "<COMMAND>: Optional. The command to get more specific infomation about. When not given, PM all the commands instead"

def help_cmd(prefix):
    return prefix + "help <COMMAND>"

def help_perms():
    return 0

def help_list():
    return "Get all the help or help about a specific command"

def aliasName():
    return ['help', 'halp', 'h', 'commands', 'command']
