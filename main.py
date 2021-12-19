import discord

token = open("token", "r").readline()

client = discord.Client()

@client.event
async def on_ready():
    print('로그인 중입니다')
    print(client.user.name)
    print(client.user.id)
    print('성공했습니다')
    game = discord.Game("시험가동")
    await client.change_presence(status=discord.Status.online, activity=game)


embed = discord.Embed(title=f"명령어 모음", description="꿀벌봇은 현재 아래 기능들을 지원하고 있습니다!", color=0xf3bb76)


@client.event
async def on_client_join(message):
    await message.channel.send(embed=embed)


@client.event
async def on_member_join(member):
    await member.send(embed=embed)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!명령어'):
        await message.channel.send(embed=embed)


client.run(token)
