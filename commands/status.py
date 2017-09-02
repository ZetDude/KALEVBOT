import importlib.machinery

loader = importlib.machinery.SourceFileLoader('maincore', 'C:/Users/Administrator/Desktop/KALEVBOT/maincore.py')
handle = loader.load_module('maincore')

def run(message, prefix, alias):
    difference = handle.get_timer()
    diskspace = handle.get_free_space_mb("C:")
    diskspaceg = diskspace / 1024 / 1024 / 1024
    p_working = "It's working! I have been running for " + str(difference)
    p_space = "\nApproximate disk space left for bot: " + str(diskspaceg) + " GB (" + str(diskspace) + " bytes)" 
    return "m", [message.channel, p_working + p_space]

def help_use():
    return "Check the status and information of the bot, suh as run time and disk space"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "status"

def help_perms():
    return 0

def help_list():
    return "Show if the bot is still working"

def alias():
    return ['status', 'ping']