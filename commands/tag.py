import importlib.machinery
import os
import sys
import pickle
import math
import difflib

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

erg = """
There are 3 basic syntactic roles
The subject of an intransitive sentence (S), the agent of a transitive sentence (A) and the patient of a transitive sentence (O) (also sometimes called P)(edited)
A language needs a way to differentiate between A and O, otherwise more or less all transitive sentences would be ambiguous
However since A or O never occur in the same clause as S, a language can group S with one of the other and save a whole category that way
S is like A in some ways and like O in others so both options are viable
Accusative languages group S and A together and lets O be its own category
Ergative languages group S and O together and lets A be its own category
Languages with split systems sometimes group S with A and sometimes with O
An example of this could be a case system
For the sentences "Alice fell" and "Alice hit Bob" an accusative language would do
`Alice-NOM fell`
`Alice-NOM Bob-ACC hit`
Where an ergative language would do
`Alice-ABS fell`
`Alice-ERG Bob-ABS hit`

**	-story provided by guff**"""

feedback = "Please keep feedback in <#328465541045944320>.\nNo discussion is allowed in <#328465486398619648>!"
tags = {"feedback": feedback,
        "fb": feedback,
        "ergative": erg,
        "erg": erg,
        "erg-abs": erg,
        "ergabs": erg}
        
matches = list(tags.keys())

def run(message, prefix, alias):
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()
    result = tags.get(opstring, False)
    if result is False:
        close = difflib.get_close_matches(opstring, matches)
        core.send(message.channel, "No such tag found. Did you mean: {}?".format(" or ".join(["`" + x + "`" for x in close])))
        return
    core.send(message.channel, result)

def help_use():
    return "Answer FAQ"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "tag"

def help_perms():
    return 0

def help_list():
    return "Answer FAQ"

def alias():
    return ['tag', 'faq']