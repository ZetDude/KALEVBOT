import maincore as core

help_info = {"use": "Return the link for the urban dictionary page for the specified text",
             "param": "{}urban <*TEXT>\n<*TEXT>: A string of characters to search for",
             "perms": None,
             "list": "Show the urban dictionary definiton for the specified subject"}
alias_list = ['urban', 'urbandictionary', 'ud']

def run(message, prefix, alias_name):
    cmdlen = len(prefix + alias_name)
    opstring = message.content[cmdlen:].strip()
    core.send(message.channel, "<http://www.urbandictionary.com/define.php?term={}>".format(
        opstring.replace('+', '%2B').replace(' ', '+')))
