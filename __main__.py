from discord.ext import commands
import os
from dotenv import load_dotenv
import discord

load_dotenv()

bot = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())


@bot.event
async def on_ready():
    exts = [file for file in os.listdir('./cogs/') if file.endswith(".py")]
    for i in exts: bot.load_extension(f"cogs.{i.replace('.py', '')}")
    print(f'{bot.user} On Ready.')


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="No verification")
    await member.add_roles(role)
    channel = bot.get_channel(817597919313526817)
    await channel.send(f'{member.mention} 님 어서오세요! 이 곳은 완두콩 서포트 서버입니다. '
                       f'\n\n우선, <#817704888980340737> 에서 역할을 받을 수 있습니다.\n\n'
                       '<#818283475693076514> 에서 명령어 사용이 가능하고,\n\n'
                       '기능을 건의하고 싶다면 <#818104521652699157> 를 이용해주세요. \n\n'
                       '또한 버그가 있다면 <#818104481593688104> 에 알려주시면 봇 운영에 큰 도움이 됩니다!')


@bot.event
async def on_raw_reaction_add(payload):
    if str(payload.emoji) == '1️⃣':
        role = discord.utils.get(payload.member.guild.roles, name="[ User ]")
        await (payload.member.guild.get_member(payload.user_id)).add_roles(role)

    elif str(payload.emoji) == '2️⃣':
        role = discord.utils.get(payload.member.guild.roles, name="[ 업데이트 알림 ]")
        await (payload.member.guild.get_member(payload.user_id)).add_roles(role)

    elif str(payload.emoji) == '3️⃣':
        role = discord.utils.get(payload.member.guild.roles, name="[ 서버 공지 알림 ]")
        await (payload.member.guild.get_member(payload.user_id)).add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(int(payload.user_id))

    if str(payload.emoji) == '2️⃣':
        role = discord.utils.get(member.guild.roles, name="[ 업데이트 알림 ]")
        await member.remove_roles(role)

    elif str(payload.emoji) == '3️⃣':
        role = discord.utils.get(member.guild.roles, name="[ 서버 공지 알림 ]")
        await member.remove_roles(role)

    else:
        pass


bot.run(os.getenv("TOKEN"))