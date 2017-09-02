import importlib.machinery

loader = importlib.machinery.SourceFileLoader('maincore', 'C:/Users/Administrator/Desktop/KALEVBOT/maincore.py')
handle = loader.load_module('maincore')

def run(message, prefix, alias):
    rList = ""
    for i in range(11):
        rList = rList + str(i) + ": " + handle.perm_name(i) + "\n"
    rList = "```\n" + rList + "\n```"
    return "m", [message.channel, rList]

def help_use():
    return "Return the list of all the permission levels and their names"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "permlist"

def help_perms():
    return 0

def help_list():
    return "Return all the permission levels"



def alias():
    return ['permlist', 'allperms']