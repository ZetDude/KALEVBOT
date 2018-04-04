"""Takes the relay deadline in a file and calculates the time until it"""

import datetime
import os
import sys
import maincore as core
from lib import relaytimegeneratorbot as rbot

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

help_info = {"use": "Display the time remaining until the relay deadline",
             "param": "{}countdown",
             "perms": None,
             "list": "Display the time remaining until the relay deadline"}
alias_list = ['countdown', 'remaining']

def run(message, prefix, alias_name):
    del prefix
    del alias_name
    f = open(sp + "/deadline.txt", "r")
    deadline = f.readlines(0)[0]
    try:
        deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        core.send(message.channel, '[RELAY OVER]')
    #get the actual datetime object from the formatted text in the file
    countdown = rbot.time_remain_string(deadline) + " remaining"
    #format the text using rbot
    core.send(message.channel, countdown)
