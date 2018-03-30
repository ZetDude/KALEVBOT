from lib import shipname as improved_shipname
import maincore as core

help_info = {"use": "Create the shipname of two people.",
             "param": "{}shipcount [**NAMES]\n[**NAMES]: Names of people to ship.",
             "perms": None,
             "list": "Create the shipname of two people."}
alias_list = ['shipname']

def run(message, prefix, alias_name):
    cmdlen = len(prefix + alias_name)
    opstring = message.content[cmdlen:].strip()
    ships_msg = opstring.split()
    if not ships_msg:
        core.send(message.channel,
                  message.author.mention + "\nUse at least two names after the command.")
        return
    elif len(ships_msg) == 1:
        core.send(message.channel,
                  message.author.mention + "\nUse at least two names after the command.")
        return
    first_half = ships_msg[0]
    second_half = ships_msg[-1]
    overflow_warning = ("\n**More than 2 names given, only taking the first and last ones.**"
                        if len(ships_msg) > 2 else "")
    final = improved_shipname.shipname(first_half, second_half)
    final_msg = overflow_warning + "\nI shall call it \"**" + final + "**\"!"

    core.send(message.channel, message.author.mention + final_msg)
