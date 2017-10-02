import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
from random import randint

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

def run(message, prefix, alias):
    kaomoji = ["お(^o^)や(^O^)す(^｡^)みぃ(^-^)ﾉﾞ",
               " .｡.:\*･ﾟ☆Goodヾ(\*´Д｀(\*ﾟωﾟ* )Night☆.｡.:\*･ﾟ",
               " – =͟͟͞͞ (¦3[▓▓])",
               " ｡･:*:･ﾟ★,｡･=^∇^\*=,｡･:*:･ﾟ☆",
               "☆~\*.(UωU\*)おやすみぃ…\*~☆",
               "|・ω・`）おやすみぃ♪"
               ]
    selectedKaomoji = kaomoji[randint(0, len(kaomoji) - 1)]
    if message.content.strip() == prefix + alias:
        combine = selectedKaomoji + " Good night!"
    else:
        if len(message.mentions) == 1:
            mentiont = message.mentions[0]
            combine = selectedKaomoji + " Good night, " + mentiont.name + "!"
        else:
            cmdlen = len(prefix + alias)
            opstring = message.content[cmdlen:].strip()
            if opstring == "all":
                combine = ""
                for i in kaomoji:
                    combine = combine + i + "\n"
            else:
                gotuser = core.userget(opstring, message.guild.id)
                if gotuser is None:
                    combine = "Something failed"
                else:
                    combine = selectedKaomoji + " Good night, " + gotuser.name + "!"

    return "m", [message.channel, combine]

def help_use():
    return "Simply wish a good night to everyone or to a specific user. It even comes with a super cute kaomoji "

def help_param():
    return "<USER>: Optional. The Username + Discriminator, ID or a mention of the user you want to wish a good night to"

def help_cmd(prefix):
    return prefix + "night <USER>"

def help_perms():
    return 0

def help_list():
    return "Wish a good night"

def alias():
    return ['night', 'n', 'goodnight']
