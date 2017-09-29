import importlib.machinery
import os
import sys
from PyDictionary import PyDictionary

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader2.load_module('maincore')

def run(message, prefix, alias):
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip().lower()
    dictionary=PyDictionary()
    defin = dictionary.meaning(opstring)
    finalMessage = ":: " + opstring + " ::\n"
    if defin == None:
        finalMessage += ":: Has no definition ::"
        core.send(message.channel, "```asciidoc\n" + finalMessage + "\n```")
        return
    for i, y in defin.items():
        finalMessage += "= " + i + "\n"
        for n in y:
            finalMessage += n + "\n"
        
    core.send(message.channel, finalMessage, "```asciidoc\n", "\n```")

def help_use():
    return "Display the relay deadine"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "deadline"

def help_perms():
    return 0

def help_list():
    return "Display the relay deadine"

def alias():
    return ['define']
    