import os
import sys
from random import randint
import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
help_info = {"use": r"Thank someone using a super cute kaomoji ^_^",
             "param": "{0}thank <*USER>\n= {0}thank --list\n<*USER>: Username, nickname or mention",
             "perms": None,
             "list": "Thank someone"}
alias_list = ['thank', 'thanks', 'arigato', 'arigatou', 'arigatoo', 'merci', 'arigatō', 'danke',
              'aitah', 'aitäh']

def run(message, prefix, alias_name):
    kaomoji = [r"♪(･ω･)ﾉ",
               r"(\*ゝω・)ﾉ",
               r"ﾟ･:,｡★＼(^-^ )♪ありがと♪( ^-^)/★,｡･:･ﾟ",
               r"(★^O^★)",
               r"☆\*:.｡. o(≧▽≦)o .｡.:\*☆",
               r"(ノ^_^)ノ",
               r"(ﾉﾟ▽ﾟ)ﾉ",
               r"(ﾉ´ヮ´)ﾉ\*:･ﾟ✧",
               r"(\*^3^)/\~☆",
               r"<(\_ \_\*)> ｱﾘｶﾞﾄｫ",
               r"ありがとぅございますっっヽ(●´∀\`)人(´∀\`●)ﾉ",
               r"ありがとうございましたm(\*-ω-)m",
               r"+｡:.ﾟヽ(\*´∀)ﾉﾟ.:｡+ﾟｧﾘｶﾞﾄｩ"
              ]

    selected_kaomoji = kaomoji[randint(0, len(kaomoji) - 1)]
    if message.content.strip() == prefix + alias_name:
        combine = selected_kaomoji + " Thank you!"
    else:
        if len(message.mentions) == 1:
            mentiont = message.mentions[0]
            if mentiont == core.cl.user:
                combine = "You're welcome, {}! \❤".format(message.author.mention)
            elif mentiont == message.author:
                combine = "Why would I need to thank you, {}?".format(message.author.mention)
            else:
               combine = selected_kaomoji + " Thank you, " + mentiont.name + "!"
        else:
            cmdlen = len(prefix + alias_name)
            opstring = message.content[cmdlen:].strip()
            if opstring == "--list":
                combine = ""
                for i in kaomoji:
                    combine = combine + i + "\n"
            else:
                gotuser = core.userget(opstring, message.guild.id)
                if gotuser == core.cl.user:
                    combine = "You're welcome, {}! \❤".format(message.author.mention)
                elif gotuser == message.author:
                    combine = "Why would I need to thank you, {}?".format(message.author.mention)
                elif gotuser is None:
                    combine = selected_kaomoji + " Thank you, " + opstring + "!"
                else:
                    combine = selected_kaomoji + " Thank you, " + gotuser.name + "!"
