"""Looks up the desired google doc dictionary if it exists in the bot and find the assoicated
translation for a given word. Works both ways."""

import os
import sys
import asyncio
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import maincore as core

sp = os.path.dirname(os.path.realpath(sys.argv[0]))
help_info = {"use": "Translate a word into a conlang. Use the --help flag on the command for more",
             "param": """{0}conlang <*LANGUAGE> <*WORD>
= {0}conlang <*LANGUAGE> --total
= {0}conlang --total
= {0}conlang --help
<*LANGUAGE>: Language to translate to
<*WORD>: Word to translate""",
             "perms": None,
             "list": "Translate a word into a conlang"}
alias_list = ['conlang', 'lang']

@asyncio.coroutine
def run(message, prefix, alias_name):
    #this entire function is mindfuck
    #it works dont fix it
    msg = yield from message.channel.send("Establishing connection...")
    try:
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name(sp + '/GOOGLE_DRIVE_SECRET.json',
                                                                 scope)
        drive = gspread.authorize(creds)
    except IOError as error:
        print(error)
        print("Connection failed. If you dont have a google drive credentials file, ignore this.")
        yield from msg.edit(content="Connection failed! Google drive connectivity is not set up!")
        return
    langs = {"jumer":     "1gLRbwcq2PAC7Jm2gVltu3vMNaGHaPvHKcdyslEbbBvc",
             "zjailatal": "1cwsXUap7orXzBvvCVt3yC7fPoSmeQyjBW1XH0rZOrxA",
             "tree-lang": "1k-iNQSrH7p25jkx3q9Dlbv3WHyeMJ3GFg932n2HtYck",
             "zlazish":   "1FeohD1GIBdyGeuUVTbCToKykGRB6LuisRLLfdwrzSMg"}
    cmdlen = len(prefix + alias_name)
    opstring = message.content[cmdlen:].strip()
    spaceloc = opstring.find(" ")
    if spaceloc == -1:
        if opstring == "--total":
            yield from msg.edit(content="I know {} language(s)!\n{}".format(
                len(langs), ", ".join(langs.keys())))
        elif opstring == "--help":
            yield from msg.edit(content=
                                """Create a Google Sheets document, following the preset shown here:
<https://docs.google.com/spreadsheets/d/1jj7LrdfRTxJVRQjlHCKLKjt-7buYuS9nkMUa9C2wJtQ/edit?usp=sharing>
Fill the info you want, and click on 'Share' in the top right
Add `kalevbot-conlang-data-fetcher@kalevbot-zet.iam.gserviceaccount.com` and allow edit permissions.
Ping ZetDude and tell him the link and language name, add he will add it""")
        else:
            yield from msg.edit(content="Not enough parameters")
        return
    postcalc = opstring[spaceloc:].strip().lower()
    precalc = opstring[:spaceloc].strip().lower()

    conlang_id = langs.get(precalc, None)
    if not conlang_id:
        core.send(message.channel, "Invalid conlang")
        return

    sheet = drive.open_by_key(conlang_id).sheet1
    data = sheet.get_all_records()

    if postcalc == "--total":
        yield from msg.edit(content="{} has {} words in total.".format(precalc, len(data)))
        return
    if postcalc == "--link":
        yield from msg.edit(content="<https://docs.google.com/spreadsheets/d/{}>".format(
            conlang_id))
        return
    to_translate = postcalc
    found_english = []
    found_conlang = []
    for i in list(data):
        definitions_english = [y.strip().lower() for y in i["ENGLISH"].split(";")]
        definitions_conlang = [y.strip().lower() for y in i["CONLANG"].split(";")]
        if to_translate in definitions_english:
            found_english.append(i)
        if to_translate in definitions_conlang:
            found_conlang.append(i)

    final_message = ""
    final_message += "Results for {} translating to {}:\n".format(to_translate, precalc)
    if not found_english:
        final_message += ":: No translation to {} found ::\n".format(precalc)
    else:
        for entry in found_english:
            homonym = entry.get("HOMONYM", None)
            if homonym is None:
                final_message += ":: {} ::\n".format(to_translate)
            else:
                final_message += ":: {} {} ::\n".format(to_translate, homonym)
            meanings = [y.strip().lower() for y in entry["ENGLISH"].split(";")]
            meanings.remove(to_translate)
            if meanings:
                final_message += "Other meanings: {}\n".format("; ".join(meanings))
            category = entry.get("CATEGORY", None)
            if category is not None:
                final_message += "{}\n".format(category)
            final_message += "== {} ==\n".format(entry["CONLANG"])
            ipa = entry.get("PRONUNCIATION", None)
            if ipa is not None:
                final_message += "/{}/\n".format(ipa.strip("/"))
            word_class = entry.get("CLASS", None)
            if word_class is not None:
                if word_class != "-" and word_class != "":
                    final_message += "Class {} word\n".format(word_class)
            notes = entry.get("NOTES", None)
            if notes is not None:
                final_message += notes
    final_message += "\nーーー\n"
    final_message += "Results for {} translating to English:\n".format(to_translate)
    if not found_conlang:
        final_message += ":: No translation to English found ::\n"
    else:
        for entry in found_conlang:
            homonym = entry.get("HOMONYM", None)
            if homonym is None:
                final_message += ":: {} ::\n".format(to_translate)
            else:
                final_message += ":: {} {} ::\n".format(to_translate, homonym)
            meanings = [y.strip().lower() for y in entry["CONLANG"].split(";")]
            meanings.remove(to_translate)
            if meanings:
                final_message += "Other meanings: {}\n".format("; ".join(meanings))
            category = entry.get("CATEGORY", None)
            if category is not None:
                final_message += "{}\n".format(category)
            final_message += "== {} ==\n".format(entry["ENGLISH"])
            ipa = entry.get("PRONUNCIATION", None)
            if ipa is not None:
                final_message += "/{}/\n".format(ipa.strip("/"))
            word_class = entry.get("CLASS", None)
            if word_class is not None:
                if word_class != "-" and word_class != "":
                    final_message += "Class {} word\n".format(word_class)
            notes = entry.get("NOTES", None)
            if notes is not None:
                final_message += notes
            final_message += "\n"
    yield from msg.edit(content="```asciidoc\n" + final_message + "\n```")
