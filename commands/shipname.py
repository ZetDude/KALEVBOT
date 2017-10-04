import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, alias):
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()
    ships_msg = opstring.split()
    try:
        first_half = len(ships_msg[0]) // 2    # get the half of the first shipped person
        second_half = len(ships_msg[-1]) // 2  # get the half of the second shipped person
        initial = ships_msg[0][:first_half]    # get the first half of the first person's nickname
        ending = ships_msg[-1][-second_half:]   # get the second half of the second person's nickname
        mid = ""
        for i in ships_msg[1:-1]:
            third = len(i) // 3
            mid += i[third:len(i)-third]
        final = initial + mid + ending         # combine them
        final_msg = "\nI shall call it \"**" + final + "**\"" # add it to the final message
    except IndexError:
        core.send(message.channel, message.author.mention + ", not enough parameters")
        return

    core.send(message.channel, message.author.mention + final_msg)

def help_use():
    return "Create the shipname of two people."

def help_param():
    return "<NAMES**>: Names of people to ship."

def help_cmd(prefix):
    return prefix + "drop <NAMES**>"

def help_perms():
    return 0

def help_list():
    return "Create the shipname of two people."

def alias():
    return ['shipname']
