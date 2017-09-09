import importlib.machinery
import os
import sys

mmod = os.path.dirname(os.path.realpath(sys.argv[0])) + "/maincore.py"

loader = importlib.machinery.SourceFileLoader('maincore', mmod)
core = loader.load_module('maincore')

def run(message, prefix, alias):
    difference = core.get_timer()
    diskspace = core.get_free_space_mb("C:")
    diskspaceg = diskspace / 1024 / 1024 / 1024
    p_working = "It's working! I have been running for " + str(difference)
    p_space = "\nApproximate disk space left for bot: " + str(diskspaceg) + " GB (" + str(diskspace) + " bytes)" 
    p_server = "\nI am present in " + str(len(core.cl.servers)) + " servers."
    p_count = "\nI have been used " + str(core.get_count()) + " time(s)"
    p_final = p_working + p_space + p_server + p_count
    core.send(message.channel, p_final)

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
    return ['status', 'ping', 'test']