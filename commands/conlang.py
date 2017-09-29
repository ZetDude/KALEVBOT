import importlib.machinery
import os
import sys
import urllib.request,urllib.parse

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

loader2 = importlib.machinery.SourceFileLoader('maincore', sp + '/maincore.py')
core = loader2.load_module('maincore')

def run(message, prefix, alias):
    drive = core.drive
    if not drive:
        core.send(message.channel, "No connection with google drive. Cannot fetch.")
        return
    langs = {"jumer": "1gLRbwcq2PAC7Jm2gVltu3vMNaGHaPvHKcdyslEbbBvc",
             "zjailatal": "1cwsXUap7orXzBvvCVt3yC7fPoSmeQyjBW1XH0rZOrxA"}
    cmdlen = len(prefix + alias)
    opstring = message.content[cmdlen:].strip()
    spaceloc = opstring.find(" ")
    if spaceloc == -1:
        if opstring == "--total":
            core.send(message.channel, "I know {} language(s)!\n{}".format(len(langs), ", ".join(langs.keys())))
            return
        if opstring == "--help":
            core.send(message.channel, "Create a Google Sheets document, following the preset shown here:\n<https://docs.google.com/spreadsheets/d/1jj7LrdfRTxJVRQjlHCKLKjt-7buYuS9nkMUa9C2wJtQ/edit?usp=sharing>\nFill the info you want, and click on 'Share' in the top right\nAdd `kalevbot-conlang-data-fetcher@kalevbot-zet.iam.gserviceaccount.com` and allow edit permissions. Ping ZetDude and tell him the link and language name, add he will add it")
            return
        core.send(message.channel, "Not enough parameters")
        return
    postcalc = opstring[spaceloc:].strip().lower()
    precalc = opstring[:spaceloc].strip().lower()
    
    id = langs.get(precalc, None)
    if not id:
        core.send(message.channel, "Invalid conlang")
        return
    
    sheet = drive.open_by_key(id).sheet1
    data = sheet.get_all_records()

    if postcalc == "--total":
        core.send(message.channel, "{} has {} words in total.".format(precalc, len(data)))
        return
    toTranslate = postcalc
    found = []
    for i in list(data):
        definitions = [y.strip().lower() for y in i["ENGLISH"].split(";")]
        if toTranslate in definitions:
            found.append(i)

    finalMessage = ""
    finalMessage += "Results for {}:\n".format(toTranslate)
    if not found:
        finalMessage += "Word not defined\n"
    else:
        for z in found:
            homonym = z.get("HOMONYM", None)
            if homonym is None:
                finalMessage += ":: {} ::\n".format(toTranslate)
            else:
                finalMessage += ":: {} {} ::\n".format(toTranslate, homonym)
            meanings = [y.strip().lower() for y in z["ENGLISH"].split(";")]
            meanings.remove(toTranslate)
            if meanings:
                finalMessage += "Other meanings: {}\n".format("; ".join(meanings))
            finalMessage += "{}\n".format(z["CATEGORY"])
            finalMessage += "== {} ==\n".format(z["CONLANG"])
            ipa = z.get("PRONUNCIATION", None)
            if ipa is not None:
                finalMessage += "/{}/\n".format(ipa)
            type = z.get("CLASS", None)
            if type is not None:
                if type != "-":
                    finalMessage += "Class {} word\n".format(type)
            finalMessage += "\n"
    core.send(message.channel, finalMessage, "```asciidoc\n", "\n```")



def help_use():
    return "Translate a word into a conlang"

def help_param():
    return "[LANGUAGE*] - The language to translate to\n[WORD*] - The word(s) to translate"

def help_cmd(prefix):
    return prefix + "conlang [LANGUAGE*] [WORD*]"

def help_perms():
    return 0

def help_list():
    return "Translate a word into a conlang"

def alias():
    return ['conlang', 'lang']