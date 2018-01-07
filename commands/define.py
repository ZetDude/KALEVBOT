import os
import sys
from PyDictionary import PyDictionary
import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

def run(message, prefix, aliasName):
    cmdlen = len(prefix + aliasName)
    opstring = message.content[cmdlen:].strip().lower()
    dictionary = PyDictionary()
    defin = dictionary.meaning(opstring)
    finalMessage = ":: " + opstring + " ::\n"
    if defin is None:
        finalMessage += ":: Has no definition ::"
        core.send(message.channel, "```asciidoc\n" + finalMessage + "\n```")
        return
    for i, y in defin.items():
        finalMessage += "= " + i + "\n"
        for n in y:
            finalMessage += n + "\n"

    core.send(message.channel, finalMessage, "```asciidoc\n", "\n```")

def help_use():
    return "Get the english definition of a word"

def help_param():
    return "[WORD*] - The word to get the definition of"

def help_cmd(prefix):
    return prefix + "define [WORD*]"

def help_perms():
    return 0

def help_list():
    return "Get the english definition of a word"

def aliasName():
    return ['define']
