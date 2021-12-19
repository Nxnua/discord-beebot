import discord
import asyncio

token = open("token", "r").readline()



def main():

    client = discord.Client()
    async def my_background_task():
        await client.wait_until_ready()
        channel = discord.Object(id='921987302362857495')
        while not client.is_closed:
            await client.send_message(channel, "hi")
            await asyncio.sleep(5)

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
        #embed = discord.Embed(title=f"명령어 모음", description="꿀벌봇은 현재 아래 기능들을 지원하고 있습니다!", color=0xf3bb76)
        await message.channel.send(embed=embed)


    @client.event
    async def on_member_join(member):
        fmt = '협곡에서 즐거운 시간 보내세요, {0.mention} 님!'
        channel = client.get_channel('921987302362857495')
        await channel.send(fmt.format(member, member.server))
        await channel.send(embed=embed)

    @client.event
    async def on_member_remove(member):
        fmt = '{0.mention} 님이 협곡을 떠나셨어요.'
        channel = client.get_channel('921987302362857495')
        await channel.send(fmt.format(member, member.server))
        await channel.send(embed=embed)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content.startswith('!명령어'):
            #embed = discord.Embed(title=f"명령어 모음", description="꿀벌봇은 현재 아래 기능들을 지원하고 있습니다!", color=0xf3bb76)
            await message.channel.send(embed=embed)

    filtering(client)

    client.loop.create_task(my_background_task())
    client.run(token)

if __name__ == "__main__":
    main()