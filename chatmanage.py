import discord

def filtering(message):
    manage = "소환사님 🎀✨예쁜 말✨🎀을 사용해😡주세요~!😎😘"
    return manage

def command(message):
    embed = discord.Embed(title=f"명령어 모음", description="꿀벌봇은 현재 아래 기능들을 지원하고 있습니다!", color=0xf3bb76)
    return embed

def hey(message):
    embed = discord.Embed(title="")
    embed.set_image(url="https://mblogthumb-phinf.pstatic.net/MjAxODA1MTdfMjg5/MDAxNTI2NTQ3NTYzMDIz.awWFb8WW9qSk85krQsWf7GXGOShPNS5ilZyVOFyrbIUg.07pMLGfgYvN_IQPPn9JLBRRvVE8yMY_xiN4LzuIfElEg.PNG.heekyun93/4c7a1d3932a211fa.png?type=w800")
    return embed

def garen(message):
    embed = discord.Embed(title="")
    embed.set_image(url="https://opgg-static.akamaized.net/images/lol/champion/Garen.png?image=c_scale,q_auto,w_140&v=1637122822")
    return embed