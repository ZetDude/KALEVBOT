import importlib.machinery
import os
import sys
import pickle
import itertools

mmod = os.path.dirname(os.path.realpath(sys.argv[0]))

def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start+n]

nums = "1.012345e0070.123414e-004-0.1234567891.21423"

def run(message, prefix, alias):
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()
    try:
        fileName = mmod + opstring
        with open(fileName, "rb") as f:
            lines = pickle.loads(f.read())
    except:
        fileName = mmod + opstring
        with open(fileName, "r") as f:
            lines = [line.rstrip('\n') for line in f]
    rSplit = []
    lines = str(lines)
    for chunk in chunks(lines, 2000):
        rSplit.append(message.channel)
        rSplit.append(chunk)
    return "a", [rSplit]

def help_use():
    return "Read a file's contents"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "file"

def help_perms():
    return 10

def help_list():
    return "Read a file's contents"

def alias():
    return ['file', 'read', 'readfile']