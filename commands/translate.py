import os
import sys
from googletrans import Translator
import pycountry

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

def run(message, prefix, aliasName):
    cmdlen = len(prefix + aliasName)
    opstring = message.content[cmdlen:].strip()
    translator = Translator()
    splitString = opstring.split()
    modifiers = [ word for word in splitString if word[0]=='-' ]
    for n, i in enumerate(modifiers):
        splitString.remove(i)
        modifiers[n] = i[1:]
    opstring = " ".join(splitString)
    try:
        if len(modifiers) == 0:
            done = translator.translate(opstring)
        elif len(modifiers) == 1:
            done = translator.translate(opstring, dest=modifiers[0])
        else:
            done = translator.translate(opstring, src=modifiers[0], dest=modifiers[1])
    except Exception as e:
        core.send(message.channel, "Something failed while translating. Please ensure you are using codes for indicating language, such as `en` or `ja`, or use the full language name, such as `nowegian` or `german`\n\nError:{}".format(e))
        return
    try:
        fromlang = pycountry.languages.get(alpha_2=done.src).name
    except:
        fromlang = done.src
    try:
        tolang = pycountry.languages.get(alpha_2=done.dest).name
    except:
        tolang = done.dest
    core.send(message.channel, ":: translating {} -> {}::\n{}\n({})".format(fromlang, tolang, done.text, done.pronunciation), "```asciidoc\n", "\n```")

def help_use():
    return "Translate something from a language to another language, using Google Translate"

def help_param():
    return "[WORDS**] The word(s) or sentence(s) to translate into English\nPrefix words with `-` to mark the target or destination language. These are optional."

def help_cmd(prefix):
    return prefix + "translate [WORDS**]"

def help_perms():
    return 0

def help_list():
    return "Translate something."

def aliasName():
    return ['translate', 'tr', 'atr']
