from discord.ext import commands

import wikipedia


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
        search_term = "_".join(search_term)
        search_term_space = search_term.replace("_", " ")
        if not modifiers:
            modifiers = ['en']

        wikipedia.set_lang(modifiers[0])
        try:
            page_object = wikipedia.page(search_term_space)
            search_term_space = page_object.title
            search_term = search_term_space.replace(" ", "_")
            snippet = page_object.summary[:450] + "..."
        except Exception as e:
            await ctx.send(f"{ctx.author}, page does not exist\n{e}")
            return

        ctx.send("<https://{}.wikipedia.org/wiki/{}>\n{}".format(modifiers[0], search_term, snippet))

    @google.error
    async def search_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author}, no search term given.")
    

def setup(bot):
    bot.add_cog(SearchCog(bot))
