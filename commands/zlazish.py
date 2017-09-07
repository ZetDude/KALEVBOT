import pickle
import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

def run(message, prefix, alias):
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()
    param = opstring.split()
    rm = ""
    
    with open(sp + '/important/zwords.txt', 'rb') as f: 
        zwords = pickle.loads(f.read())
    with open(sp + '/important/zsuf.txt', 'rb') as f: 
        zsuf = pickle.loads(f.read())
    with open(sp + '/important/zpre.txt', 'rb') as f: 
        zpre = pickle.loads(f.read())

    for i in param:
        if i in zpre:
            rm += zpre[i]
        elif i in zsuf:
            rm = rm[:-1]
            rm += zsuf[i] + " "
        elif i in zwords:
            rm += zwords[i] + " "
        else:
            rm += i + " "

    return "m", [message.channel, "```\n" + rm + "\n```"]
                
    

def help_use():
    return "Translate a gloss into Zlazish"

def help_param():
    return "<GLOSSARY**>: Varies."

def help_cmd(prefix):
    return prefix + "zlazish <GLOSSARY**>"

def help_perms():
    return 0


def alias():
    return ['zlazish', 'z']

def help_list():
    return "Translate a gloss into Zlazish"

