import discord
import random

def filtering(message):
    manage = "소환사님 🎀✨예쁜 말✨🎀을 사용해😡주세요~!😎😘"
    return manage

def command(message):
    embed = discord.Embed(title=f"명령어 모음", description="꿀벌봇은 현재 아래 기능들을 지원하고 있습니다!", color=0xf3bb76)
    embed.set_thumbnail(url="https://mblogthumb-phinf.pstatic.net/MjAxODA1MTdfMjEx/MDAxNTI2NTQ3NTYzMDI0.GGFyQth1IVreeUdrVmYVopJlv8ZX2EsTQGqQ3h6ktjEg.r6jltvwy2lBUvB_Wh4M9xvxw-gwV4RHUR1AXSF-nqpMg.PNG.heekyun93/4fb137544b692e53.png?type=w800")
    embed.add_field(name=f"!유저", value="`!유저 닉네임 (ex. !유저 빽핑의화신)`\n해당 유저 정보를 카드 형식으로 볼 수 있습니다", inline=False)
    embed.add_field(name=f"!챔피언", value="`!챔피언 라인 이름 (ex. !챔피언 탑 가렌)`\n해당 라인에서 챔피언의 승률 표본,\n템트리 정보를 검색합니다.",
                    inline=False)
    embed.add_field(name="ㅤ", value="ㅤ", inline=True)
    embed.add_field(name=f"[그 외 쓸모 없어 보이지만 소소한 기능들]", value="`숨겨진 몇가지 이스터에그는 덤!\n※채팅 중 심한 욕설은 삭제 될 수 있으니\n주의해 주세요※`", inline=False)
    embed.add_field(name=f"인사", value="`!안녕 (ex. !안녕, !안녕하세요)`\n꿀벌봇이 인사를 받아줍니다!", inline=False)
    embed.add_field(name=f"식사 메뉴 추천", value="`!밥 or !메뉴 (ex. !밥, !메뉴 추천좀)`\n뭘 먹을지 고민되시나요?\n식사는 꼭 챙겨드세요!", inline=False)
    embed.add_field(name="ㅤ", value="ㅤ", inline=True)
    embed.set_footer(text="버그 제보 및 문의\nhttps://github.com/NyaNyak/2021-OSS",
                     icon_url="https://mblogthumb-phinf.pstatic.net/MjAxODA1MTdfMjg5/MDAxNTI2NTQ3NTYzMDIz.awWFb8WW9qSk85krQsWf7GXGOShPNS5ilZyVOFyrbIUg.07pMLGfgYvN_IQPPn9JLBRRvVE8yMY_xiN4LzuIfElEg.PNG.heekyun93/4c7a1d3932a211fa.png?type=w800")
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
    embed.set_image(url="https://w.namu.la/s/39d986b83774de090109bcbd0ecfdb983cc21cb29fb02fbdafbc1f8170e59d7c2dd34e70c826538e6cdd9265a9c6bd5460a09495d9623fb866dc515be68abd002b697ccc9c7c5c75f927ccc791c87c8d3d25b791fbc721dce46ff6c83dafb137")
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