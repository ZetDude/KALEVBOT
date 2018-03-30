from googletrans import Translator
import pycountry
import maincore as core

help_info = {"use": "Translate something from a language to another using Google Translate",
             "param": """{}translate -(LANG1) -(LANG2) <*TEXT>
[WORDS**] The word(s) or sentence(s) to translate into English
Prefix words with `-` to mark the target or destination language. These are optional.
k!tr text               = guess language and translate to English
k!tr -lang text         = translate text to lang
k!tr -lang1 -lang2 text = translate text from lang1 to lang2""",
             "perms": None,
             "list": "Translate something."}
alias_list = ['translate', 'tr', 'atr']

def run(message, prefix, alias_name):
    cmdlen = len(prefix + alias_name)
    opstring = message.content[cmdlen:].strip()
    translator = Translator()
    split_string = opstring.split()
    modifiers = [word for word in split_string if word[0] == '-']
    for n, i in enumerate(modifiers):
        split_string.remove(i)
        modifiers[n] = i[1:]
    opstring = " ".join(split_string)
    try:
        if len(modifiers) == 0:
            done = translator.translate(opstring)
        elif len(modifiers) == 1:
            done = translator.translate(opstring, dest=modifiers[0])
        else:
            done = translator.translate(opstring, src=modifiers[0], dest=modifiers[1])
    except Exception as e:
        core.send(message.channel, ("Something failed while translating. Please ensure you are" +
                                    " using codes for indicating language, such as `en` or `ja`, " +
                                    "or use the full language name, such as `norwegian` or " +
                                    "`german`\n\nError:{}".format(e)))
        return
    try:
        fromlang = pycountry.languages.get(alpha_2=done.src).name
    except:
        fromlang = done.src
    try:
        tolang = pycountry.languages.get(alpha_2=done.dest).name
    except:
        tolang = done.dest
    core.send(message.channel, ":: translating {} -> {}::\n{}\n({})".format(
        fromlang, tolang, done.text, done.pronunciation), "```asciidoc\n", "\n```")
