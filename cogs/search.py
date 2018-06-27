import re

import wikipedia
import discord
from discord.ext import commands

BRACKET_REGEX = re.compile(r'\([^)]*\)')
SPACE_REGEX = re.compile(' +')


class SearchCog():
    "Includes commands about searching the internet"
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Search Commands"

    @commands.command(name='google', aliases=['g'],
                      help="Return the link for the google search page for the specified text",
                      brief="Google the specified subject")
    async def google(self, ctx, *, search_term):
        await ctx.send("<https://www.google.com/search?q={}>".format(
            search_term.replace('+', '%2B').replace(' ', '+')))

    @commands.command(name='wiktionary', aliases=['wikti', 'wk'],
                      help=("Return the link for the wiktionary page for the specified text. "+
                            "Prefix language codes with a `-` to mark the language of the page"),
                      brief="Get the wiktionary definition for the specified subject")
    async def wiktionary(self, ctx, *, search_term):
        search_term = search_term.split()
        modifiers = [word for word in search_term if word[0] == '-']
        for n, i in enumerate(modifiers):
            search_term.remove(i)
            modifiers[n] = i[1:]
        search_term = "_".join(search_term)
        if not modifiers:
            modifiers = ['en']
        await ctx.send("<https://{}.wiktionary.org/wiki/{}>".format(modifiers[0], search_term))

    @commands.command(name='urbandictionary', aliases=['urban', 'ud'],
                      help="Return the link for the urban dictionary page for the specified text",
                      brief="Show the urban dictionary definiton for the specified subject")
    async def urbandictionary(self, ctx, *, search_term):
        await ctx.send("<http://www.urbandictionary.com/define.php?term={}>".format(
            search_term.replace('+', '%2B').replace(' ', '+')))

    @commands.command(name='wikipedia', aliases=['wiki', 'w'],
                      help=("Return the link for the wikipedia page for the specified text. "+
                            "Prefix language codes with a `-` to mark the language of the page"),
                      brief="Get the wikipedia page for the specified subject")
    async def wiki(self, ctx, *, search_term):
        search_term = search_term.split()
        modifiers = [word for word in search_term if word[0] == '-']
        for n, i in enumerate(modifiers):
            search_term.remove(i)
            modifiers[n] = i[1:]
        search_term = " ".join(search_term)
        if not modifiers:
            modifiers = ['en']

        wikipedia.set_lang(modifiers[0])
        try:
            page_object = wikipedia.page(search_term)
            page_title = page_object.title
            page_link = page_title.replace(" ", "_")
            page_link = f"https://{modifiers[0]}.wikipedia.org/wiki/{page_link}"
            page_content = page_object.summary
            summary = re.sub(SPACE_REGEX, ' ', re.sub(BRACKET_REGEX, '', page_content))
            snippet = summary[:450] + "..." if len(summary) > 450 else summary
        except wikipedia.PageError:
            await ctx.send(f"{ctx.author.name}, page does not exist")
            return
        except wikipedia.DisambiguationError as e:
            await ctx.send(f"{ctx.author.name}, {e}")
            return
        
        embed = discord.Embed(
            title=page_title,
            colour=0x4a90e2,
            url=page_link,
            description=snippet
            )
        await ctx.send(embed=embed)

    @google.error
    @wiki.error
    @wiktionary.error
    @urbandictionary.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.name}, no search term given.")
    

def setup(bot):
    bot.add_cog(SearchCog(bot))
