import datetime
import os
import sys
import maincore as core
from lib import relaytimegeneratorbot as rbot

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

help_info = {"use": "Display the relay deadine",
             "param": "{}deadline",
             "perms": None,
             "list": "Display the relay deadine"}
alias_list = ['deadline', 'relay']

def run(message, prefix, alias_name):
    del prefix
    del alias_name
    file = open(sp + '/deadline.txt', "r")
    deadline = file.readlines(0)[0]
    try:
        deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        core.send(message.channel, '[RELAY OVER]')
    deadline = rbot.deadline_format(deadline)
    core.send(message.channel, deadline)
