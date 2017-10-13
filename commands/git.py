import importlib.machinery
import os
import sys
import git 

import maincore as core
sp = os.path.dirname(os.path.realpath(sys.argv[0]))

def run(message, prefix, alias):
    g = git.cmd.Git(sp)
    g.pull()
    core.send(message.channel, "did something")

def help_use():
    return "Do something with git"

def help_param():
    return "[ACTIONS**] - Actions to do"

def help_cmd(prefix):
    return prefix + "git [ACTIONS**]"

def help_perms():
    return 10

def help_list():
    return "Do something with git"

def alias():
    return ['git', 'github']
    