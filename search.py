import discord
import requests
import time as t
import txtinout
import pprint
from bs4 import BeautifulSoup

baseurl = "http://your.gg"
levelurl = "http://fow.kr/find/"

def mostresult(most):
    result = "```"
    if len(most) == 0:
        return "`기록이 없습니다!`"
    for i in range(len(most) // 4):
        result += most[0 + i * 4] + " | " + most[1 + i * 4] + "게임 | 승률 " \
                  + most[2 + i * 4] + " | KDA " + most[3 + i * 4]
        if i + 1 != len(most) // 4:
            result += '\n'
    result += "```"

    return result

def search(message):
    message_content = message.content.replace("!검색 ", "")
    plusurl = message_content.replace(" ", "")
    url = baseurl + "/kr/profile/" + plusurl
    res = requests.get(url).text
    soup = BeautifulSoup(res, "html.parser")

    url_ = levelurl + plusurl
    res_ = requests.get(url_).text
    soup_ = BeautifulSoup(res_, "html.parser")

    level = soup_.find("a", attrs={"class" : "sbtn small"}).get_text()
    level = level.split(" ")[1]

    img = soup.find("div", attrs={"class": "d-flex align-items-center ml-3"}).find("img").get('src')
    img = baseurl + img

    tierinfo = soup.find("div", attrs={"class" : "d-flex flex-column align-items-start ml-3"}).get_text()
    tier = tierinfo.split()
    tierNode = ""
    if len(tier) == 6:
        tierName = tier[1]
        win = tier[4]
        lose = tier[5]
        lp = tier[3]
        rate = tier[2]
    else:
        tierName = tier[1]
        tierNode = tier[2]
        win = tier[5]
        lose = tier[6]
        lp = tier[4]
        rate = tier[3]

    mostchamp = soup_.find("table", attrs={"class" : "tablesorter"}).find('tbody').find_all('td')

    most = []

    for i in range(3):
        if len(mostchamp) >= (i + 1) * 14:
            most.append(mostchamp[0 + i * 14].find('img').get('alt'))
            most.append(mostchamp[1 + i * 14].get_text())
            most.append(mostchamp[2 + i * 14].get_text())
            most.append(mostchamp[3 + i * 14].get_text())
        else:
            break

    embed = discord.Embed(title=message_content, description="", color=0x62c1cc)
    embed.set_thumbnail(url=img)

    embed.add_field(name="레벨", value="`" + level + "`", inline=False)
    embed.add_field(name="티어 정보", value="`" + tierName + " " + tierNode + " | " + lp + "`", inline=False)
    embed.add_field(name="승, 패, 승률", value="`" + win + " " + lose + " | " + rate + "`", inline=False)
    embed.add_field(name="모스트 챔피언", value=mostresult(most), inline=False)

    """
    embed.add_field(name="모스트 챔피언", value="```" + most[0] + " | " + most[1] + "게임 | 승률 " + most[2] + " | KDA " + most[3] + "\n" +
                                          most[4] + " | " + most[5] + "게임 | 승률 " + most[6] + " | KDA " + most[7] + "\n" +
                                          most[8] + " | " + most[9] + "게임 | 승률 " + most[10] + " | KDA " + most[11] +
                                                "```", inline=False  )

    """
    embed.set_footer(text="솔로랭크 기준 티어입니다. | 랭크 정보가 없을 시 출력되지 않습니다.", icon_url="https://mblogthumb-phinf.pstatic.net/MjAxODA1MTdfMjEx/MDAxNTI2NTQ3NTYzMDI0.GGFyQth1IVreeUdrVmYVopJlv8ZX2EsTQGqQ3h6ktjEg.r6jltvwy2lBUvB_Wh4M9xvxw-gwV4RHUR1AXSF-nqpMg.PNG.heekyun93/4fb137544b692e53.png?type=w800")
    return embed
