import os
import sys
import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

help_info = {"use": "Mark the relay as ended",
             "param": "{}end",
             "perms": "relay",
             "list": "Mark the relay as ended"}
alias_list = ['end', 'endrelay']

def run(message, prefix, alias_name):
    del prefix
    del alias_name
    file = open(sp + '/deadline.txt', "w")
    file.write("END")
    core.send(message.channel, "Ended the relay")
