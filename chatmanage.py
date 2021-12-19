import discord
import random

def filtering(message):
    manage = "소환사님 🎀✨예쁜 말✨🎀을 사용해😡주세요~!😎😘"
    return manage

def command(message):
    embed = discord.Embed(title=f"명령어 모음", description="꿀벌봇은 현재 아래 기능들을 지원하고 있습니다!", color=0xf3bb76)
    return embed

def hello(message):
    sentence = ["안녕하세요 ", "오늘도 좋은 하루 되세요 ", "힘세고 강한 하루! ", "건강 조심하세요 ", "식사는 하셨나요? "]
    i = random.randint(0, len(sentence)-1)
    return sentence[i]

def hey(message):
    embed = discord.Embed(title="")
    embed.set_image(url="https://mblogthumb-phinf.pstatic.net/MjAxODA1MTdfMjg5/MDAxNTI2NTQ3NTYzMDIz.awWFb8WW9qSk85krQsWf7GXGOShPNS5ilZyVOFyrbIUg.07pMLGfgYvN_IQPPn9JLBRRvVE8yMY_xiN4LzuIfElEg.PNG.heekyun93/4c7a1d3932a211fa.png?type=w800")
    return embed

def garen(message):
    embed = discord.Embed(title="")
    embed.set_image(url="https://opgg-static.akamaized.net/images/lol/champion/Garen.png?image=c_scale,q_auto,w_140&v=1637122822")
    return embed

def meal(message):
    food = ["돈까스", "김밥", "햄버거", "보쌈", "컵라면", "삼각김밥", "떡볶이", "양꼬치", "짜장면",
            "파스타", "리조또", "삼겹살", "피자", "순대국", "치킨", "초밥", "라면", "닭갈비", "족발",
            "감자탕", "해장국", "순두부찌개", "치맥", "김치찌개", "부대찌개", "비빔밥", "불고기", "곱창",
            "칼국수", "설렁탕", "갈비", "삼계탕", "아구찜", "냉면", "짬뽕", "갈비탕", "샐러드", "도시락",
            "회", "쌀국수", "마라탕", "메밀소바", "라멘", "덮밥", "우동", "김치볶음밥", "오므라이스", "카레",
            "만두", "샌드위치", "닭볶음탕", "제육볶음", "된장찌개", "선짓국", "추어탕", "육개장", "샤브샤브",
            "닭발", "찜닭", "토스트", "돼지국밥", "소머리국밥"]
    i = random.randint(0, len(food)-1)
    return food[i]