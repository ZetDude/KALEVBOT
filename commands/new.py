import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('relaytimegeneratorbot', sp + '/relaytimegeneratorbot.py')
rbot = loader.load_module('relaytimegeneratorbot')
loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader2.load_module('maincore')

def run(message, prefix, alias):
    newdeadline = rbot.deadline_time()
    deadline = rbot.deadline_format(newdeadline)
    f = open(sp + "/deadline.txt", "w")
    f.write(str(newdeadline))
    core.send(message.channel, deadline)

def help_use():
    return "Generate a new relay deadline and overwrite the old one"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "new"

def help_perms():
    return 4

def help_list():
    return "Generate a new relay deadline and overwrite the old one"

def alias():
    return ['new', 'newdeadline']