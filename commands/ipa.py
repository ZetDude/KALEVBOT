import importlib.machinery
import os
import sys

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader.load_module('maincore')

def run(message, prefix, alias):
    return "m", [message.channel, """The IPA (International Phonetic Alphabet) chart in various forms:

<http://www.ipachart.com/> Simple version of the graph with interactable buttons
<http://westonruter.github.io/ipa-chart/keyboard/> A keyboard site for writing all things IPA using the on-screen buttons
<https://web.uvic.ca/ling/resources/ipa/charts/IPAlab/IPAlab.htm> A more detailed version of the alphabet with interactive buttons
"""]

def help_use():
    return "Display multiple options for getting the IPA chart and/or keyboard"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "ipa"

def help_perms():
    return 0

def help_list():
    return "Get the link for the IPA chart"

def alias():
    return ['ipa']