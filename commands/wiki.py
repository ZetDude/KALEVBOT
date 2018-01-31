import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, aliasName):
    cmdlen = len(prefix + aliasName)
    opstring = message.content[cmdlen:].strip()
    splitString = opstring.split()
    modifiers = [ word for word in splitString if word[0]=='-' ]
    for n, i in enumerate(modifiers):
        splitString.remove(i)
        modifiers[n] = i[1:]
    opstring = "_".join(splitString)
    if len(modifiers) == 0:
        modifiers = ['en']
    core.send(message.channel, "<https://{}.wikipedia.org/wiki/{}>".format(modifiers[0], opstring))


def help_use():
    return "Return the link for the wikipedia definiton page for the specified text"

def help_param():
    return "<TEXT*>: A string of character to search for in wikipedia"

def help_cmd(prefix):
    return prefix + "wiki <TEXT*>"

def help_perms():
    return 0

def help_list():
    return "Show the wikipedia definiton for the specified subject"

def aliasName():
    return ['wiki', 'wikipedia']
