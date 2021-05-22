import discord
from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='역할')
    @commands.is_owner()
    async def _give_roles(self, ctx):
        embed = discord.Embed(
            title='역할 받기',
            description=':one: : 유저 역할 받기 \n:two: : 업데이트 알림 역할 받기\n:three: : 서버 공지 알림 역할 받기',
            color=0x00FFFF
        )
        a = await ctx.send(embed=embed)

        await a.add_reaction("1️⃣")
        await a.add_reaction("2️⃣")
        await a.add_reaction("3️⃣")


def setup(bot):
    bot.add_cog(Welcome(bot))