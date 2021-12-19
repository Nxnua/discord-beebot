import discord
import asyncio
from chatmanage import filtering, command, hey, garen
from discord.ext import tasks
from itertools import cycle

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

async def my_background_task():
    await client.wait_until_ready()
    channel = client.get_channel(id=921987302362857495)
    while not client.is_closed:
        await channel.send("붕붕!")
        await asyncio.sleep(5)

@client.event
async def on_guild_join(guild):
    channel = client.get_channel(id=921987302362857495)
    await channel.send('안녕하세요 소환사님, 꿀벌봇이 왔어요🐝')
    await channel.send('도움이 필요하시다면 아래 명령을 내려주세요!')
    await channel.send(embed=command(guild))


@client.event
async def on_member_join(member):
    channel = client.get_channel(id=921987302362857495)
    await channel.send('협곡에서 즐거운 시간 보내세요 ' + member.name + ' 님!')
    await channel.send('!명령어 를 입력하시면 제가 뭘 할 수 있는지 보여드릴게요😎')
    """embed = command(member)"""


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
    if message.content.startswith('!야'):
        await message.channel.send(embed=hey(message))
    if message.content.startswith('!가붕'):
        await message.channel.send(embed=garen(message))

    else:
        for i in shit:
            if i in message.content:
                await message.delete()
                await message.channel.send(filtering(message))


client.loop.create_task(my_background_task())
client.run(token)