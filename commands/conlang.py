import importlib.machinery
import os
import sys
import urllib.request,urllib.parse

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader2.load_module('maincore')

def run(message, prefix, alias):
    
    langs = {"jumer": "si3M1gPJ"}
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()
    spaceloc = opstring.find(" ")
    if spaceloc == -1:
        core.send(message.channel, "Not enough parameters")
        return
    postcalc = opstring[spaceloc:].strip().lower()
    precalc = opstring[:spaceloc].strip()
    
    id = langs.get(precalc, None)
    if not id:
        core.send(message.channel, "Invalid conlang")
        return
    
    raw = "https://pastebin.com/raw/"+id
    try:
        dataOnline = urllib.request.urlopen(raw).read().decode("utf-8")
    except Exception as e:
        core.send(message.channel, e)
    dataOnline = dataOnline.split("\r\n")
    data = []
    for i in dataOnline:
        points = i.split(",")
        data.append([n.strip() for n in points])

    if postcalc == "--total":
        core.send(message.channel, "{} has {} words in total.".format(precalc, len(data)))
        return
    toTranslate = postcalc
    found = []
    for i in data:
        definitions = [y.strip() for y in i[0].split(";")]
        if toTranslate in definitions:
            found.append(i)

    finalMessage = ""
    finalMessage += "Results for {}:\n".format(toTranslate)
    if not found:
        finalMessage += "Word not defined\n"
    else:
        for z in found:
            finalMessage += ":: {} {} ::\n".format(toTranslate, z[1])
            finalMessage += "{}\n".format(z[2])
            meanings = [y.strip() for y in z[0].split(";")]
            meanings.remove(toTranslate)
            if meanings:
                finalMessage += "Other meanings: {}\n".format("; ".join(meanings))
            finalMessage += "== {} ==\n".format(z[3])
            if z[4] != 0:
                finalMessage += "Class {} word\n".format(z[4])
            finalMessage += "\n"
    core.send(message.channel, finalMessage, "```asciidoc\n", "\n```")



def help_use():
    return "Display the relay deadine"

def help_param():
    return None

def help_cmd(prefix):
    return prefix + "deadline"

def help_perms():
    return 0

def help_list():
    return "Display the relay deadine"

def alias():
    return ['conlang', 'lang']