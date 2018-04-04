# pylint: disable=eval-used
# pylint: disable=broad-except

import os
import sys
import inspect
import asyncio

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

help_info = {"use": "Run code",
             "param": "{}eval <*CODE*>\n<*CODE>: The code to evaluate",
             "perms": "owner",
             "list": "Run code"}
alias_list = ['eval', 'evaluate']

def chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    for start in range(0, len(s), n):
        yield s[start:start+n]

@asyncio.coroutine
def run(message, prefix, alias_name):
    cmdlen = len(prefix + alias_name)
    opstring = message.content[cmdlen:].strip()
    mode = ""
    try:
        result = eval(opstring)
        if inspect.isawaitable(result):
            result = yield from result
    except Exception as error:
        yield from message.channel.send(type(error).__name__ + ': ' + str(error))
    chunked = chunks(str(result), 1980)
    print(chunked)
    for i in chunked:
        yield from message.channel.send("```{}\n{}\n```".format(mode, i))
