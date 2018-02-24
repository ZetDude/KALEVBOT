import os
import sys
from random import randint
import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

def run(message, prefix, aliasName):
    kaomoji = [r"お(^o^)や(^O^)す(^｡^)みぃ(^-^)ﾉﾞ",
               r" .｡.:\*･ﾟ☆Goodヾ(\*´Д｀(\*ﾟωﾟ\* )Night☆.｡.:\*･ﾟ",
               r" – =͟͟͞ (¦3[▓▓])",
               r" ｡･:\*:･ﾟ★,｡･=^∇^\*=,｡･:\*:･ﾟ☆",
               r"☆~\*.(UωU\*)おやすみぃ…\*~☆",
               r"|・ω・`）おやすみぃ♪",
               r"              ",
              ]

    selectedKaomoji = kaomoji[randint(0, len(kaomoji) - 1)]
    if message.content.strip() == prefix + aliasName:
        combine = selectedKaomoji + " Good night!"
    else:
        if len(message.mentions) == 1:
            mentiont = message.mentions[0]
            combine = selectedKaomoji + " Good night, " + mentiont.name + "!"
        else:
            cmdlen = len(prefix + aliasName)
            opstring = message.content[cmdlen:].strip()
            if opstring == "--list":
                combine = ""
                for i in kaomoji:
                    combine = combine + i + "\n"
            else:
                combine = selectedKaomoji + " Thank you, " + opstring + "!"

    core.send(message.channel, combine)

def help_use():
    return "Wish someone a good night using a super cute kaomoji ^\_^"

def help_param():
    return "<USER>: The username, nickname, mention or anything else related to the user"

def help_cmd(prefix):
    return prefix + "night <USER>"

def help_perms():
    return 0

def help_list():
    return "Wish someone a good night"

def aliasName():
    return ['night', 'goodnight']

