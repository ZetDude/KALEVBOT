import os

def run(message, prefix, alias):
    os.system('CLS')
    return "m", [message.channel, "ye man"]
    

def help_use():
    return "temporary debug stuff"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "c"

def help_perms():
    return 10

def help_list():
    return "temporary debug stuff"

def alias():
    return ['c']