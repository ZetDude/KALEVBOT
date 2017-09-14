import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start+n]

def run(message, prefix, alias):
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()
    mode = ""
    try:
        evaluated = str(eval(opstring))
    except Exception as e:
        evaluated = "- ERROR\n- " + str(e)
        mode = "diff"
    chunked = chunks(evaluated, 1980)
    print(chunked)
    for i in chunked:
        core.send(message.channel, "```{}\n{}\n```".format(mode, i))
    

def help_use():
    return "Run code"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "eval"

def help_perms():
    return ["OWNER"]

def help_list():
    return "Run code"

def alias():
    return ['eval']