import discord

shit = ["시발", "씨발", "애미", "느금"]

@client.event
async def filtering(message):
    chat = message.content
    for i in shit:
        if i in chat:
            await message.channel.send("소환사님 예쁜 말^^을 사용해^^주세요~!")
            await message.delete()
