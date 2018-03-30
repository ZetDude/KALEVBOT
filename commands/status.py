import maincore as core

help_info = {"use": "Check the status and information of the bot, such as run time and disk space",
                 "param": "{}status",
                 "perms": None,
                 "list": "Show if the bot is still working"}
alias_list = ['status', 'test']

def run(message, prefix, alias_name):
    del prefix
    del alias_name
    difference = core.get_timer()
    diskspace = core.get_free_space_mb("/")
    diskspaceg = diskspace / 1024 / 1024 / 1024
    p_working = "It's working! I have been running for " + str(difference)
    p_space = "\nApproximate disk space left for bot: {0:.2f} GB ({1} bytes)".format(diskspaceg,
                                                                                     diskspace)
    p_guild = "\nI am present in " + str(len(core.cl.guilds)) + " guilds."
    p_final = p_working + p_space + p_guild
    core.send(message.channel, p_final)
