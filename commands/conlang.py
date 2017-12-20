import importlib.machinery
import os
import sys
import asyncio
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread

sp = os.path.dirname(os.path.realpath(sys.argv[0]))

import maincore as core

@asyncio.coroutine
def run(message, prefix, aliasName):
    msg = yield from message.channel.send("Establishing connection...")
    gStart = time.time()
    try:
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name(sp + '/GOOGLE_DRIVE_SECRET.json',
                                                                 scope)
        drive = gspread.authorize(creds)
    except Exception as e:
        print(e)
        print("Connection failed. If you dont have a google drive credentials file, ignore this.")
        yield from msg.edit(content="Connection failed!")
        return
    gEnd = time.time()
    print("Launching gdrive connection took {} seconds".format(gEnd - gStart))
    langs = {"jumer": "1gLRbwcq2PAC7Jm2gVltu3vMNaGHaPvHKcdyslEbbBvc",
             "zjailatal": "1cwsXUap7orXzBvvCVt3yC7fPoSmeQyjBW1XH0rZOrxA",
             "tree-lang": "1k-iNQSrH7p25jkx3q9Dlbv3WHyeMJ3GFg932n2HtYck",
             "zlazish": "1FeohD1GIBdyGeuUVTbCToKykGRB6LuisRLLfdwrzSMg"}
    cmdlen = len(prefix + aliasName)
    opstring = message.content[cmdlen:].strip()
    spaceloc = opstring.find(" ")
    if spaceloc == -1:
        if opstring == "--total":
            yield from msg.edit(content="I know {} language(s)!\n{}".format(len(langs), ", ".join(langs.keys())))
            return
        if opstring == "--help":
            yield from msg.edit(content="Create a Google Sheets document, following the preset shown here:\n<https://docs.google.com/spreadsheets/d/1jj7LrdfRTxJVRQjlHCKLKjt-7buYuS9nkMUa9C2wJtQ/edit?usp=sharing>\nFill the info you want, and click on 'Share' in the top right\nAdd `kalevbot-conlang-data-fetcher@kalevbot-zet.iam.gserviceaccount.com` and allow edit permissions. Ping ZetDude and tell him the link and language name, add he will add it")
            return
        yield from msg.edit(content="Not enough parameters")
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
        yield from msg.edit(content="{} has {} words in total.".format(precalc, len(data)))
        return
    if postcalc == "--link":
        yield from msg.edit(content="<https://docs.google.com/spreadsheets/d/{}>".format(id))
        return
    toTranslate = postcalc
    foundEN = []
    foundCL = []
    for i in list(data):
        definitionsEN = [y.strip().lower() for y in i["ENGLISH"].split(";")]
        definitionsCL = [y.strip().lower() for y in i["CONLANG"].split(";")]
        if toTranslate in definitionsEN:
            foundEN.append(i)
        if toTranslate in definitionsCL:
            foundCL.append(i)

    finalMessage = ""
    finalMessage += "Results for {} translating to {}:\n".format(toTranslate, precalc)
    if not foundEN:
        finalMessage += ":: No translation to {} found ::\n".format(precalc)
    else:
        for z in foundEN:
            homonym = z.get("HOMONYM", None)
            if homonym is None:
                finalMessage += ":: {} ::\n".format(toTranslate)
            else:
                finalMessage += ":: {} {} ::\n".format(toTranslate, homonym)
            meanings = [y.strip().lower() for y in z["ENGLISH"].split(";")]
            meanings.remove(toTranslate)
            if meanings:
                finalMessage += "Other meanings: {}\n".format("; ".join(meanings))
            category = z.get("CATEGORY", None)
            if category is not None:
                finalMessage += "{}\n".format(category)
            finalMessage += "== {} ==\n".format(z["CONLANG"])
            ipa = z.get("PRONUNCIATION", None)
            if ipa is not None:
                finalMessage += "/{}/\n".format(ipa.strip("/"))
            type = z.get("CLASS", None)
            if type is not None:
                if type != "-" and type != "":
                    finalMessage += "Class {} word\n".format(type)
            notes = z.get("NOTES", None)
            if notes is not None:
                finalMessage += notes
    finalMessage += "ーーー\n"
    finalMessage += "Results for {} translating to English:\n".format(toTranslate, precalc)
    if not foundCL:
        finalMessage += ":: No translation to English found ::\n"
    else:
        for z in foundCL:
            homonym = z.get("HOMONYM", None)
            if homonym is None:
                finalMessage += ":: {} ::\n".format(toTranslate)
            else:
                finalMessage += ":: {} {} ::\n".format(toTranslate, homonym)
            meanings = [y.strip().lower() for y in z["CONLANG"].split(";")]
            meanings.remove(toTranslate)
            if meanings:
                finalMessage += "Other meanings: {}\n".format("; ".join(meanings))
            category = z.get("CATEGORY", None)
            if category is not None:
                finalMessage += "{}\n".format(category)
            finalMessage += "== {} ==\n".format(z["ENGLISH"])
            ipa = z.get("PRONUNCIATION", None)
            if ipa is not None:
                finalMessage += "/{}/\n".format(ipa.strip("/"))
            type = z.get("CLASS", None)
            if type is not None:
                if type != "-" and type != "":
                    finalMessage += "Class {} word\n".format(type)
            notes = z.get("NOTES", None)
            if notes is not None:
                finalMessage += notes
            finalMessage += "\n"
    yield from msg.edit(content="```asciidoc\n" + finalMessage + "\n```")



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

def aliasName():
    return ['conlang', 'lang']
