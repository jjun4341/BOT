import discord
from discord.ext import commands
from pymongo import MongoClient
import asyncio


class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = MongoClient('mongodb://localhost:27017/').Manage_Bot.user

    @commands.command(name='warn')
    @commands.has_role("[ Bot Developer ]")
    async def give_warn(self, ctx, user: discord.Member, count: int):
        if self.coll.find_one({"_id": str(user.id)}):
            find = {"_id": str(ctx.author.id)}
            setdata = {"$inc": {"warn_count": int(count)}}
            self.coll.update_one(find, setdata)
            await ctx.send(f'`{await self.bot.fetch_user(int(user.id))}`님에게 경고 `{count}` 개를 지급했습니다.', delete_after=5.0)
        else:
            self.coll.insert_one({
                "_id": str(user.id),
                "warn_count": 0
            })
            find = {"_id": str(ctx.author.id)}
            setdata = {"$inc": {"warn_count": int(count)}}
            self.coll.update_one(find, setdata)
            await ctx.send(f'`{await self.bot.fetch_user(int(user.id))}`님에게 경고 `{count}` 개를 지급했습니다.',
                           delete_after=5.0)

        channel = self.bot.get_channel(817964393437462560)
        embed = discord.Embed(
            title='경고',
            description=f'경고 받은 사용자 : `{await self.bot.fetch_user(int(user.id))}`\n지급 받은 경고 갯수 : {count}',
            color=0x00FFFF
        )
        await channel.send(embed=embed)

    @commands.command(name='mute')
    @commands.has_role("[ Bot Developer ]")
    async def _mute(self, ctx, user: discord.Member, type: str, time: int):
        role = ctx.guild.get_role(817963983352102922)
        roles = ctx.guild.get_role(817598594009661450)
        channel = self.bot.get_channel(817964393437462560)

        if type in ['시간', 'h', 'H', 'hour']:
            await user.add_roles(role)
            await user.remove_roles(roles)
            embed = discord.Embed(
                title='뮤트',
                description=f'뮤트 받은 사용자 : `{await self.bot.fetch_user(int(user.id))}`\n뮤트 기간 : `{time}`시간',
                color=0x00FFFF
            )
            await channel.send(embed=embed)
            try:
                await user.send('뮤트가 시작되었습니다.')
            except:
                await user.create_dm()
                await user.send('뮤트가 시작되었습니다.')
            await asyncio.sleep(time * 3600)
            await user.remove_roles(role)
            await user.add_roles(roles)
            await user.send('뮤트가 해제되었습니다.')

        elif type in ['분', 'm', 'M', 'minutes','minute']:
            await user.add_roles(role)
            await user.remove_roles(roles)
            embed = discord.Embed(
                title='뮤트',
                description=f'뮤트 받은 사용자 : `{await self.bot.fetch_user(int(user.id))}`\n뮤트 기간 : `{time}`분',
                color=0x00FFFF
            )
            await channel.send(embed=embed)
            try:
                await user.send('뮤트가 시작되었습니다.')
            except:
                await user.create_dm()
                await user.send('뮤트가 시작되었습니다.')
            await asyncio.sleep(time * 60)
            await user.remove_roles(role)
            await user.add_roles(roles)
            await user.send('뮤트가 해제되었습니다.')


def setup(bot):
    bot.add_cog(Warn(bot))