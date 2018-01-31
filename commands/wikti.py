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
    core.send(message.channel, "<https://{}.wiktionary.org/wiki/{}>".format(modifiers[0], opstring))


def help_use():
    return """Return the link for the wiktionary definiton page for the specified text
Prefix languages codes with `-` to specify for the language of the page"""

def help_param():
    return "<TEXT*>: A string of characters to search for in wiktionary"

def help_cmd(prefix):
    return prefix + "wikti <TEXT*>"

def help_perms():
    return 0

def help_list():
    return "Show the wiktionary definiton for the specified subject"

def aliasName():
    return ['wikti', 'wiktionary']
