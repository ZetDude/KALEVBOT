import maincore as core
import wikipedia

help_info = {"use": "Return the link for the wikipedia definition page for the specified text",
             "param": """{}wiki -(LANG) <*TEXT>
<*TEXT>: A string of character to search for in wikipedia
Prefix languages codes with `-` to specify for the language of the page""",
             "perms": None,
             "list": "Show the wikipedia definition for the specified subject"}
alias_list = ['wiki', 'wikipedia']

def run(message, prefix, alias_name):
    cmdlen = len(prefix + alias_name)
    opstring = message.content[cmdlen:].strip()
    split_string = opstring.split()
    modifiers = [word for word in split_string if word[0] == '-']
    for n, i in enumerate(modifiers):
        split_string.remove(i)
        modifiers[n] = i[1:]
    opstring = "_".join(split_string)
    opstring_space = opstring.replace("_", " ")
    if len(modifiers) == 0:
        modifiers = ['en']
    
    wikipedia.set_lang(modifiers[0])
    try:
        page_object = wikipedia.page(opstring_space)
        opstring_space = page_object.title
        opstring = opstring_space.replace(" ", "_")
        snippet = page_object.summary[:450] + "..."
    except Exception as e:
        core.send(message.channel, "{}, page does not exist\n{}".format(message.author.mention, e))
        return

    core.send(message.channel, "<https://{}.wikipedia.org/wiki/{}>\n{}".format(modifiers[0], opstring, snippet))
