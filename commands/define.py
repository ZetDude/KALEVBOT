from PyDictionary import PyDictionary
import maincore as core

help_info = {"use": "Get the english definition of a word",
             "param": "{}define <*WORD>\n<*WORD>: Word to define",
             "perms": None,
             "list": "Get the english definition of a word"}
alias_list = ['define', 'definition']

def run(message, prefix, alias_name):
    cmdlen = len(prefix + alias_name)
    opstring = message.content[cmdlen:].strip().lower()
    dictionary = PyDictionary()
    definition = dictionary.meaning(opstring)
    final_message = ":: " + opstring + " ::\n"
    if definition is None:
        final_message += ":: Has no definition ::"
        core.send(message.channel, "```asciidoc\n" + final_message + "\n```")
        return
    for i, y in definition.items():
        final_message += "= " + i + "\n"
        for n in y:
            final_message += n + "\n"

    core.send(message.channel, final_message, "```asciidoc\n", "\n```")
