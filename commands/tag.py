import importlib.machinery
import os
import sys
import pickle
import math
import difflib

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')


class FAQTopic:
    def __init__(self, text, author, aliases=None, editor=''):
        self.text = text
        self.author = author
        self.editor = editor
        if aliases is None:
            aliases = []
        self.aliases = aliases

    def __str__(self):
        if (self.editor != ''):
            endtext = '\n\n(provided by {}, edited by {})'.format(
                self.author, self.editor
            )
        else:
            endtext = '\n\n(provided by {})'.format(self.author)
        return self.text + endtext


# Faq topics -- probably make a separate file for these eventually

aspect = """
Aspect
Aspect is the way in which an action is performed.
For example, imperfective aspect is used for actions that have not finished or are still ongoing, such as "I was walking" or "I am walking".
Perfective is used for actions that are treated as a whole, like "he walked" or "we walk".
Imperfective is often divided into further categories, such as continuous (actions still occurring), habitual (repeated actions), etc.
"""

case = """
Case is a noun's role in a sentence.
For example, in English: "**I** killed the __cat__", **I** would be the agent (performer of the action), and __cat__ would be the object of the action, and in the accusative case.
In a more complicated sentence, for example: "*my* **cat** killed the __mouse__", *my* would be the owner of the cat, and in the genitive case.
And in: "**I** slept",  **I** would be the subject, and in the nominative case. (see k!faq ergative if confused).
There are cases for many other things, such as indirect objects, location, motion, possession, etc.
"""

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
"""

feedback = "Please keep feedback in <#328465541045944320>.\nNo discussion is allowed in <#328465486398619648>!"

mood = """
Mood
Mood (or mode) is the speaker's relation, opinion, or intention of the action
There are two main categories of moods found in nearly all languages—realis and irrealis.
realis deals with actions that will, have, or are already taking place, such as if I were to say "I walk" and then proceed to walk, I would be talking in the realis mood
conversely, the irrealis mood pertains to actions that may or may not take place, such as in the english sentence "I should walk"—in this case I have the right to decide whether or not this statement becomes real.
irrealis mood often splits into several other moods, such as those used for commands (imperative) or suggestions (subjunctive)
"""

tense = """
Tense
Tense is when an action happens.
For example, in English: "walk" is in the present tense (technically nonpast) and is happening at the time of speaking
however, "walked" is in the past tense, and happened prior to the time of speaking
some languages may split one tense into multiple or combine and/or eliminate them entirely
sometimes, tense and aspect (see k!faq aspect) can be combined or treated as one element, in which case we call them "conflated"
"""


faq_topics = {
    'aspect': FAQTopic(aspect, 'xithiox', ['asp', 'aspects']),
    'case': FAQTopic(case, 'Lingo', ['cases']),
    'ergative': FAQTopic(erg, 'guff', ['erg', 'ergative-absolutive', 'abs', 'erg-abs', 'abs', 'absolutive', 'ergabs']),
    'feedback': FAQTopic(feedback, 'zet', ['fb']),
    'mood': FAQTopic(mood, 'Lingo', ['moods', 'mode', 'modes']),
    'tense': FAQTopic(tense, 'Lingo', ['tenses'], 'xithiox')
}

faq_aliases = {k: v for v in faq_topics.values() for k in v.aliases}


def run(message, prefix, alias):
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()

    if opstring in faq_topics:
        result = str(faq_topics[opstring])
    elif opstring in faq_aliases:
        result = str(faq_aliases[opstring])
    else:
        close = difflib.get_close_matches(opstring, list(faq_topics.keys:()) + list(faq_aliases.keys()))
        result = "No such tag found. Did you mean: {}?".format(" or ".join(["`" + x + "`" for x in close]))
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
