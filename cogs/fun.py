from random import randint

from discord.ext import commands


class FunCog():
    "fun fun fun fun fun fun"
    def __init__(self, bot):
        self.bot = bot
        type(self).__name__ = "Fun Commands"

    @commands.command(name='night', aliases=['n', 'goodnight', 'nacht', 'öö', 'ööd', 'oyasumi', 'おやすみ'],
                      help=(r"Wish someone a good night using a super cute kaomoji ^_^"),
                      brief="Wish someone a good night.")
    async def night(self, ctx, *, target_user=None):
        kaomoji = [r"お(^o^)や(^O^)す(^｡^)みぃ(^-^)ﾉﾞ",
                r" .｡.:\*･ﾟ☆Goodヾ(\*´Д｀(\*ﾟωﾟ\* )Night☆.｡.:\*･ﾟ",
                r" – =͟͟͞ (¦3[▓▓])",
                r" ｡･:\*:･ﾟ★,｡･=^∇^\*=,｡･:\*:･ﾟ☆",
                r"☆~\*.(UωU\*)おやすみぃ…\*~☆",
                r"|・ω・`）おやすみぃ♪",
                ]

        selected_kaomoji = kaomoji[randint(0, len(kaomoji) - 1)]
        if target_user is None:
            combine = selected_kaomoji + " Good night!"
        elif target_user == "-list":
            combine = ""
                for i in kaomoji:
                    combine = combine + i + "\n"
        else:
            try:
                target_user = await commands.MemberConverter(ctx, target_user)
                combine = selected_kaomoji + " Good night, " + target_user.name + "!"
            except:
                combine = selected_kaomoji + " Thank you, " + target_user + "!"

        ctx.send(combine)

def setup(bot):
    bot.add_cog(FunCog(bot))
