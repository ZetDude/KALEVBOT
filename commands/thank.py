import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
from random import randint

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

def run(message, prefix, alias):
    kaomoji = ["♪(･ω･)ﾉ",
               "(\*ゝω・)ﾉ",
               "ﾟ･:,｡★＼(^-^ )♪ありがと♪( ^-^)/★,｡･:･ﾟ",
               "(★^O^★)",
               "☆\*:.｡. o(≧▽≦)o .｡.:\*☆",
               "(ノ^\_^)ノ",
               "(ﾉﾟ▽ﾟ)ﾉ",
               "(ﾉ´ヮ´)ﾉ\*:･ﾟ✧",
               "(\*^3^)/~☆",
               "<(\_ \_\*)> ｱﾘｶﾞﾄｫ",
               "ありがとぅございますっっヽ(●´∀\`)人(´∀\`●)ﾉ",
               "ありがとうございましたm(\*-ω-)m",
               "+｡:.ﾟヽ(\*´∀)ﾉﾟ.:｡+ﾟｧﾘｶﾞﾄｩ"
               ]

    selectedKaomoji = kaomoji[randint(0, len(kaomoji) - 1)]
    if message.content.strip() == prefix + alias:
        combine = selectedKaomoji + " Thank you!"
    else:
        if len(message.mentions) == 1:
            mentiont = message.mentions[0]
            combine = selectedKaomoji + " Thank you, " + mentiont.name + "!"
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
                    combine = selectedKaomoji + " Thank you, " + gotuser.name + "!"

    return "m", [message.channel, combine]



def help_use():
    return "Thank someone using a super cute kaomoji"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "thank"

def help_perms():
    return 0

def help_list():
    return "Thank someone"

def alias():
    return ['thank', 'thanks', 'arigato', 'arigatou', 'arigatoo', 'merci', 'arigatō', 'danke', 'aitah', 'aitaeh', 'aitäh']
