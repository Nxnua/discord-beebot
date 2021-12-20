import discord
import asyncio
from chatmanage import filtering, command, hello, hey, garen, meal
from discord.ext import tasks
from itertools import cycle
from search import search
import time as t
from champion import champion
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
token = open("token", "r").readline()

status = cycle(["협곡 위를 비행", "붕붕붕!"])

@client.event
async def on_ready():
    print('로그인 중입니다')
    print(client.user.name)
    print(client.user.id)
    print('성공했습니다')
    print(f"[!] 참가 중인 서버 : {len(client.guilds)}개의 서버에 참여 중\n")

    change_status.start()

@tasks.loop(seconds=3)    # n초마다 다음 메시지 출력
async def change_status():
    await client.change_presence(activity=discord.Game(name=next(status)))


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('안녕하세요 소환사님, 꿀벌봇이 왔어요🐝')
            await channel.send('도움이 필요하시다면 아래 명령을 내려주세요!')
            await channel.send(embed=command())


@client.event
async def on_member_join(member):
    #channel = client.get_channel(id=921987302362857495)
    await member.send('협곡에서 즐거운 시간 보내세요 ' + member.name + ' 님!')
    await member.send('!명령어 를 입력하시면 제가 뭘 할 수 있는지 보여드릴게요😎')


@client.event
async def on_member_remove(member):
    channel = client.get_channel(id=921987302362857495)
    await channel.send(member.name + ' 님이 협곡을 떠나셨어요.')


shit = ["시발", "씨발", "애미", "느금", "병신", "개새끼"]


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!명령어'):
        await message.channel.send(embed=command(message))
    if message.content.startswith('!안녕'):
        await message.channel.send(hello(message) + message.author.name + ' 님!')
    if message.content.startswith('!밥') or message.content.startswith('!메뉴'):
        await message.channel.send(meal(message) + ' 어떠세요?')
    if message.content.startswith('!야'):
        await message.channel.send(embed=hey(message))
    if message.content.startswith('!가붕'):
        await message.channel.send(embed=garen(message))
    if message.content.startswith('!유저'):
        t1 = t.time()
        await message.channel.send(file=search(message))
        t2 = t.time()
        embed = discord.Embed(title="데이터 출처", description="your.gg / fow.kr", color=0x62c1cc)
        embed.add_field(name="소요시간", value="`" + str(round(t2 - t1, 3)) + "초`", inline=False)
        embed.set_footer(text="솔로랭크 기준 티어입니다. | 랭크 정보가 없을 시 출력되지 않습니다.",
                         icon_url="https://mblogthumb-phinf.pstatic.net/MjAxODA1MTdfMjEx/MDAxNTI2NTQ3NTYzMDI0.GGFyQth1IVreeUdrVmYVopJlv8ZX2EsTQGqQ3h6ktjEg.r6jltvwy2lBUvB_Wh4M9xvxw-gwV4RHUR1AXSF-nqpMg.PNG.heekyun93/4fb137544b692e53.png?type=w800")

        await message.channel.send(embed=embed)
        await message.delete()
    if message.content.startswith('!챔피언'):
        await message.channel.send(file=champion(message))
        #await message.channel.send(embed=champion(message))

    else:
        for i in shit:
            if i in message.content:
                await message.delete()
                await message.channel.send(filtering(message))


client.run(token)