import maincore as core

help_info = {"use": "Return the link for the wiktionary definition page for the specified text",
             "param": """{}wiki -(LANG) <*TEXT>
<*TEXT>: A string of character to search for in wiktionary
Prefix languages codes with `-` to specify for the language of the page""",
             "perms": None,
             "list": "Show the wiktionary definiton for the specified subject"}
alias_list = ['wikti', 'wiktionary']

def run(message, prefix, alias_name):
    cmdlen = len(prefix + alias_name)
    opstring = message.content[cmdlen:].strip()
    split_string = opstring.split()
    modifiers = [word for word in split_string if word[0] == '-']
    for n, i in enumerate(modifiers):
        split_string.remove(i)
        modifiers[n] = i[1:]
    opstring = "_".join(split_string)
    if len(modifiers) == 0:
        modifiers = ['en']
    core.send(message.channel, "<https://{}.wiktionary.org/wiki/{}>".format(modifiers[0], opstring))