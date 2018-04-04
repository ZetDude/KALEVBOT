import os
import sys
import maincore as core
from lib import relaytimegeneratorbot as rbot

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
help_info = {"use": "Generate a new relay deadline and overwrite the old one",
             "param": "{}new",
             "perms": "relay",
             "list": "Generate a new relay deadline and overwrite the old one"}
alias_list = ['new', 'newdeadline']

def run(message, prefix, alias_name):
    del prefix
    del alias_name
    newdeadline = rbot.deadline_time()
    deadline = rbot.deadline_format(newdeadline)
    file = open(sp + "/deadline.txt", "w")
    file.write(str(newdeadline))
    core.send(message.channel, deadline)
