import maincore as core

help_info = {"use": "Return the link for the google search page for the specified text",
             "param": "{}google <*TEXT>\n<*TEXT>: A string of characters to search for in google",
             "perms": None,
             "list": "Google the specified subject"}
alias_list = ['google', 'g']


def run(message, prefix, alias_name):
    cmdlen = len(prefix + alias_name)
    opstring = message.content[cmdlen:].strip()
    core.send(message.channel, "<https://www.google.com/search?q={}>".format(
        opstring.replace('+', '%2B').replace(' ', '+')))
