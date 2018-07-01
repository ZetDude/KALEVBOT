import gspread
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from googletrans import Translator, LANGUAGES
from oauth2client.service_account import ServiceAccountCredentials
from PyDictionary import PyDictionary



def filosoft_lookup(target_word, fetch_conjugations):
    url = "http://www.filosoft.ee/gene_et/gene.cgi"

    post_request = requests.post(url, data={
        'word': target_word,
        'gi': fetch_conjugations,
    })

    soup = BeautifulSoup(post_request.content, "html.parser")
    table = soup.find("table")

    datasets = []
    for row in table.find_all("tr")[:]:
        dataset = [td.get_text().replace('\xa0', ' ') for td in row.find_all("td")][0]
        dataset = dataset.split("//")
        dataset = [x.strip().strip(",") for x in dataset]
        datasets.append(dataset)
    return datasets

class LookupCog():
    "Includes commands about looking up information, from the internet or otherwise"
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Lookup"

    @commands.command(name='conlang', aliases=['lang'],
                      help=("Translate a word into a conlang. " +
                            "Use the -help flag on the command for more."),
                      brief="Translate a word into a conlang.")
    async def conlang(self, ctx, *, search_word):
        #this entire function is mindfuck
        #it works dont fix it
        msg = await ctx.send("Establishing connection...")
        try:
            scope = ['https://spreadsheets.google.com/feeds']
            creds = ServiceAccountCredentials.from_json_keyfile_name('GOOGLE_DRIVE_SECRET.json',
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

    @commands.command(name='inflect', aliases=['kääna'],
                      help="Inflect Estonian nouns or adjectives to some forms, "+
                      "most are left out as they are easily derived from other forms",
                      brief="Inflect Estonian nouns or adjectives")
    async def inflect(self, ctx, *, word):
        inflections = [" sg n, ", " sg g, ", " sg p, ", " pl n, ", " pl g, ", " pl p, ",
                       " sg ill, adt, "]
        datasets = filosoft_lookup(word, inflections)
        final_message = "\n".join([" - ".join(x[1:]) for x in datasets])
        await ctx.send("```\n" + final_message + "\n```")

    @commands.command(name='conjugate', aliases=['pööra'],
                      help="Conjugate Estonian verbs to some forms, "+
                      "most are left out as they are easily derived from other forms",
                      brief="Conjugate Estonian verbs")
    async def conjugate(self, ctx, *, word):
        conjugations = [" da, ", " n, ", " tud, "]
        datasets = filosoft_lookup(word, conjugations)
        final_message = "\n".join([" - ".join(x[1:]) for x in datasets])
        await ctx.send("```\n" + final_message + "\n```")

    @commands.command(name='translate', aliases=['tr', 'atr'],
                      help="Translate something from a language to another using Google Translate.",
                      brief="Translate something.")
    async def translate(self, ctx, *, phrase):
        translator = Translator()
        phrase = phrase.split()
        modifiers = [word for word in phrase if word[0] == '-']
        for n, i in enumerate(modifiers):
            phrase.remove(i)
            modifiers[n] = i[1:]
        phrase = " ".join(phrase)
        try:
            if not modifiers:
                done = translator.translate(phrase)
            elif len(modifiers) == 1:
                done = translator.translate(phrase, dest=modifiers[0])
            else:
                done = translator.translate(phrase, src=modifiers[0], dest=modifiers[1])
        except ValueError:
            await ctx.send(("Something failed while translating. Please ensure you are "
                            "using codes for indicating language, such as `en` or `ja`, "
                            "or use the full language name, such as `norwegian` or "
                            "`german`"))
            return
        fromlang = LANGUAGES[done.src]
        tolang = LANGUAGES[done.dest]
        await ctx.send("{}:: translating {} -> {} ::\n{}\n{}".format(
            "```asciidoc\n", fromlang, tolang, done.text, "\n```"))

    @commands.command(name='define', aliases=['definition'],
                      help="Get the english definition of a word.",
                      brief="Get the english definition of a word.")
    async def define(self, ctx, *, word):
        dictionary = PyDictionary()
        definition = dictionary.meaning(word)
        final_message = ":: " + word + " ::\n"
        if definition is None:
            final_message += ":: Has no definition ::"
            ctx.send("```asciidoc\n" + final_message + "\n```")
            return
        for i, y in definition.items():
            final_message += "= " + i + "\n"
            for n in y:
                final_message += n + "\n"

        await ctx.send("```asciidoc\n" + final_message + "\n```")

def setup(bot):
    bot.add_cog(LookupCog(bot))
