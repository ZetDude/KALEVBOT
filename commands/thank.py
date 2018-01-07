import os
import sys
from random import randint
import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

def run(message, prefix, aliasName):
    kaomoji = [r"♪(･ω･)ﾉ",
               r"(*ゝω・)ﾉ",
               r"ﾟ･:,｡★＼(^-^ )♪ありがと♪( ^-^)/★,｡･:･ﾟ",
               r"(★^O^★)",
               r"☆*:.｡. o(≧▽≦)o .｡.:*☆",
               r"(ノ^_^)ノ",
               r"(ﾉﾟ▽ﾟ)ﾉ",
               r"(ﾉ´ヮ´)ﾉ*:･ﾟ✧",
               r"(*^3^)/~☆",
               r"<(_ _*)> ｱﾘｶﾞﾄｫ",
               r"ありがとぅございますっっヽ(●´∀`)人(´∀`●)ﾉ",
               r"ありがとうございましたm(*-ω-)m",
               r"+｡:.ﾟヽ(*´∀)ﾉﾟ.:｡+ﾟｧﾘｶﾞﾄｩ"
              ]

    selectedKaomoji = kaomoji[randint(0, len(kaomoji) - 1)]
    if message.content.strip() == prefix + aliasName:
        combine = selectedKaomoji + " Thank you!"
    else:
        if len(message.mentions) == 1:
            mentiont = message.mentions[0]
            combine = selectedKaomoji + " Thank you, " + mentiont.name + "!"
        else:
            cmdlen = len(prefix + aliasName)
            opstring = message.content[cmdlen:].strip()
            if opstring == "--list":
                combine = ""
                for i in kaomoji:
                    combine = combine + i + "n"
            else:
                gotuser = core.userget(opstring, message.guild.id)
                if gotuser == core.cl.client.user:
                    combine = "You're welcome! \❤"
                elif gotuser == message.author:
                    combine = "Don't get too egotistical now!"
                elif gotuser is None:
                    combine = selectedKaomoji + " Thank you, " + opstring + "!"
                else:
                    combine = selectedKaomoji + " Thank you, " + gotuser.name + "!"

    core.send(message.channel, combine)

def help_use():
    return "Thank someone using a super cute kaomoji"

def help_param():
    return "<USER>: The username, nickname, mention or anything else related to the user"

def help_cmd(prefix):
    return prefix + "thank <USER>"

def help_perms():
    return 0

def help_list():
    return "Thank someone"

def aliasName():
    return ['thank', 'thanks', 'arigato', 'arigatou', 'arigatoo',
            'merci', 'arigatō', 'danke', 'aitah', 'aitäh']
