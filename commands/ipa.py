import maincore as core

help_info = {"use": "Display multiple options for getting the IPA chart and/or keyboard",
             "param": "{}ipa",
             "perms": None,
             "list": "Get the link for the IPA chart"}
alias_list = ['ipa']

def run(message, prefix, alias_name):
    del prefix
    del alias_name
    core.send(message.channel, """The IPA (International Phonetic Alphabet) chart in various forms:

<http://www.ipachart.com/> Simple version of the graph with sounds
<http://westonruter.github.io/ipa-chart/keyboard/> A keyboard site for writing all things IPA using the on-screen buttons
<https://web.uvic.ca/ling/resources/ipa/charts/IPAlab/IPAlab.htm> A more detailed version of the alphabet with interactive buttons
""")
