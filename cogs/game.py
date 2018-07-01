import os
import pickle
import sys

from discord.ext import commands
from lib import entity, item


class GameCog():
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "RPG"

    @commands.command(name='join', aliases=['enter', 'play'],
                      help="Join the RPG!",
                      brief="Creates a player for you so you could participate in the RPG")
    async def join(self, ctx):
        running_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        datafile = running_path + "/important/playerdata.pickle"
        try:
            with open(datafile, "rb") as opened_file:
                players = pickle.load(opened_file)
        except FileNotFoundError:
            players = []
        except pickle.UnpicklingError:
            await ctx.send(f"file {datafile} is corrupt, cannot fetch data.")
            return
        players_id = [x.idnum for x in players]
        if ctx.author.id in players_id:
            await ctx.send(f"{ctx.author.name}, you have already joined!")
            return
        author_data = { 
            "name": ctx.author.name,
            "id": ctx.author.id,
            "invsize": 10,
        }
        new_player = entity.Entity(author_data)
        players.append(new_player)
        with open(datafile, 'wb') as opened_file:
            pickle.dump(players, opened_file)
        welcome_message = ("```diff\n"
                           f"+ Welcome to the game, {ctx.author.name}!\n"
                           f"For now, your stats are 0. I advise you upgrade them right away.\n"
                           f"Use {ctx.prefix}upgrade <stat> <amount> for that. "
                           f"I have given you 20 stat points\n"
                           f"The stats are: 'Health', 'Attack', 'Defense', 'Speed' and 'Luck'\n"
                           f"! Learn more using {ctx.prefix}about.\n"
                           f"- Good luck!\n"
                           "```")
        await ctx.send(welcome_message)

def setup(bot):
    bot.add_cog(GameCog(bot))