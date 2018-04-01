from random import randint
import maincore as core

help_info = {"use": r"Wish someone a good night using a super cute kaomoji ^_^",
             "param": "{0}night <*USER>\n= {0}night --list\n<*USER>: Username, nickname or mention",
             "perms": None,
             "list": "Wish someone a good night"}
alias_list = ['night', 'n', 'goodnight', 'nacht', 'öö', 'ööd', 'oyasumi', 'おやすみ']

def run(message, prefix, alias_name):
    kaomoji = [r"お(^o^)や(^O^)す(^｡^)みぃ(^-^)ﾉﾞ",
               r" .｡.:\*･ﾟ☆Goodヾ(\*´Д｀(\*ﾟωﾟ\* )Night☆.｡.:\*･ﾟ",
               r" – =͟͟͞ (¦3[▓▓])",
               r" ｡･:\*:･ﾟ★,｡･=^∇^\*=,｡･:\*:･ﾟ☆",
               r"☆~\*.(UωU\*)おやすみぃ…\*~☆",
               r"|・ω・`）おやすみぃ♪",
               r"              ",
              ]

    selected_kaomoji = kaomoji[randint(0, len(kaomoji) - 1)]
    if message.content.strip() == prefix + alias_name:
        combine = selected_kaomoji + " Good night!"
    else:
        if len(message.mentions) == 1:
            mentiont = message.mentions[0]
            combine = selected_kaomoji + " Good night, " + mentiont.name + "!"
        else:
            cmdlen = len(prefix + alias_name)
            opstring = message.content[cmdlen:].strip()
            if opstring == "--list":
                combine = ""
                for i in kaomoji:
                    combine = combine + i + "\n"
            else:
                combine = selected_kaomoji + " Thank you, " + opstring + "!"

    core.send(message.channel, combine)
