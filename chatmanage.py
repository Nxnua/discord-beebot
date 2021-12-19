import discord

shit = ["시발", "씨발", "애미", "느금", "병신", "개새끼"]

def filtering(client):
    @client.event
    async def on_message(message):
        chat = message.content
        for i in shit:
            if i in chat:
                await message.channel.send("소환사님 🎀✨예쁜 말✨🎀을 사용해😡주세요~!😎😘")
                await message.delete()


