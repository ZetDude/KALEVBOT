import os
import sys

import gspread
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials


class LookupCog():
    "Includes commands about looking up information, from the internet or otherwise"
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Lookup Commands"

    @commands.command(name='conlang', aliases=['lang'],
                      help=("Translate a word into a conlang. " +
                            "Use the -help flag on the command for more."),
                      brief="Translate a word into a conlang.")
    async def conlang(self, ctx, *, search_word):
        #this entire function is mindfuck
        #it works dont fix it
        msg = await ctx.send("Establishing connection...")
        try:
            sp = os.path.dirname(os.path.realpath(sys.argv[0]))
            scope = ['https://spreadsheets.google.com/feeds']
            creds = ServiceAccountCredentials.from_json_keyfile_name(sp + '/GOOGLE_DRIVE_SECRET.json',
                                                                     scope)
            drive = gspread.authorize(creds)
        except IOError as error:
            print(error)
            print("If you dont have a google drive credentials file, ignore this.")
            await msg.edit(content="Connection failed! Google drive connectivity is not set up!")
            return
        langs = {"jumer":     "1gLRbwcq2PAC7Jm2gVltu3vMNaGHaPvHKcdyslEbbBvc",
                 "zjailatal": "1cwsXUap7orXzBvvCVt3yC7fPoSmeQyjBW1XH0rZOrxA",
                 "tree-lang": "1k-iNQSrH7p25jkx3q9Dlbv3WHyeMJ3GFg932n2HtYck",
                 "zlazish":   "1FeohD1GIBdyGeuUVTbCToKykGRB6LuisRLLfdwrzSMg"}
        spaceloc = search_word.find(" ")
        if spaceloc == -1:
            if search_word == "-total":
                await msg.edit(content="I know {} language(s)!\n{}".format(
                    len(langs), ", ".join(langs.keys())))
            elif search_word == "-help":
                await msg.edit(content=
                               """Create a Google Sheets document, following the preset shown here:
<https://docs.google.com/spreadsheets/d/1jj7LrdfRTxJVRQjlHCKLKjt-7buYuS9nkMUa9C2wJtQ/edit?usp=sharing>
Fill the info you want, and click on 'Share' in the top right
Add `kalevbot-conlang-data-fetcher@kalevbot-zet.iam.gserviceaccount.com` and allow edit permissions.
Message zetty#4213 and tell him the link and language name, add he will add it""")
            else:
                await msg.edit(content="Not enough parameters")
            return
        to_translate = search_word[spaceloc:].strip().lower()
        target_language = search_word[:spaceloc].strip().lower()

        conlang_id = langs.get(target_language, None)
        if not conlang_id:
            await msg.edit(content="Invalid conlang")
            return

        sheet = drive.open_by_key(conlang_id).sheet1
        data = sheet.get_all_records()

        if to_translate == "-total":
            await msg.edit(content="{} has {} words in total.".format(target_language, len(data)))
            return
        if to_translate == "-link":
            await msg.edit(content="<https://docs.google.com/spreadsheets/d/{}>".format(
                conlang_id))
            return
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
        result_message = ""
        result_message += "Results for {} translating to {}:\n".format(
            to_translate, target_language)
        for entry in found_english:
            homonym = entry.get("HOMONYM", None)
            if homonym is None:
                result_message += ":: {} ::\n".format(to_translate)
            else:
                result_message += ":: {} {} ::\n".format(to_translate, homonym)
            meanings = [y.strip().lower() for y in entry["ENGLISH"].split(";")]
            meanings.remove(to_translate)
            if meanings:
                result_message += "Other meanings: {}\n".format("; ".join(meanings))
            category = entry.get("CATEGORY", None)
            if category is not None:
                result_message += "{}\n".format(category)
            result_message += "== {} ==\n".format(entry["CONLANG"])
            ipa = entry.get("PRONUNCIATION", None)
            if ipa is not None:
                result_message += "/{}/\n".format(ipa.strip("/"))
            word_class = entry.get("CLASS", None)
            if word_class is not None:
                if word_class != "-" and word_class != "":
                    result_message += "Class {} word\n".format(word_class)
            notes = entry.get("NOTES", None)
            if notes is not None:
                result_message += notes
        if found_english:
            final_message += result_message
        result_message = ""
        result_message += "Results for {} translating to English:\n".format(to_translate)
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
        if found_conlang:
            if found_english and found_conlang:
                final_message += "\nーーー\n"
            final_message += result_message
        if final_message == "":
            final_message = "[No results found]"
        await msg.edit(content="```asciidoc\n" + final_message + "\n```")
    
def setup(bot):
    bot.add_cog(LookupCog(bot))
