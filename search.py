import discord
import requests
import time as t
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


baseurl = "http://your.gg"
levelurl = "http://fow.kr/find/"

temp = []


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
    global temp
    message_content = message.content.replace("!검색 ", "")
    plusurl = message_content.replace(" ", "")
    url = baseurl + "/kr/profile/" + plusurl
    res = requests.get(url).text
    soup = BeautifulSoup(res, "html.parser")

    url_ = levelurl + plusurl
    res_ = requests.get(url_).text
    soup_ = BeautifulSoup(res_, "html.parser")

    level_ = soup_.find("a", attrs={"class" : "sbtn small"}).get_text()
    level = level_.split(" ")[1]

    img = soup.find("div", attrs={"class": "d-flex align-items-center ml-3"}).find("img").get('src')
    img = baseurl + img
    print(img)

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

    embed.set_footer(text="솔로랭크 기준 티어입니다. | 랭크 정보가 없을 시 출력되지 않습니다.", icon_url="https://mblogthumb-phinf.pstatic.net/MjAxODA1MTdfMjEx/MDAxNTI2NTQ3NTYzMDI0.GGFyQth1IVreeUdrVmYVopJlv8ZX2EsTQGqQ3h6ktjEg.r6jltvwy2lBUvB_Wh4M9xvxw-gwV4RHUR1AXSF-nqpMg.PNG.heekyun93/4fb137544b692e53.png?type=w800")

    im_show(get_info(message))
    return embed


def get_info(message):
    message_content = message.content.replace("!검색 ", "")
    plusurl = message_content.replace(" ", "")
    url = baseurl + "/kr/profile/" + plusurl
    res = requests.get(url).text
    soup = BeautifulSoup(res, "html.parser")

    url_ = levelurl + plusurl
    res_ = requests.get(url_).text
    soup_ = BeautifulSoup(res_, "html.parser")

    level_ = soup_.find("a", attrs={"class": "sbtn small"}).get_text()
    level = level_.split(" ")[1]

    img = soup.find("div", attrs={"class": "d-flex align-items-center ml-3"}).find("img").get('src')
    img = baseurl + img

    tierinfo = soup.find("div", attrs={"class": "d-flex flex-column align-items-start ml-3"}).get_text()
    tier = tierinfo.split()
    tiernode = ""
    if len(tier) == 6:
        tiername = tier[1]
        win = tier[4]
        lose = tier[5]
        lp = tier[3]
        rate = tier[2]
    else:
        tiername = tier[1]
        tiernode = tier[2]
        win = tier[5]
        lose = tier[6]
        lp = tier[4]
        rate = tier[3]

    mostchamp = soup_.find("table", attrs={"class": "tablesorter"}).find('tbody').find_all('td')

    most = []

    for i in range(3):
        if len(mostchamp) >= (i + 1) * 14:
            most.append(mostchamp[0 + i * 14].find('img').get('alt'))
            most.append(mostchamp[1 + i * 14].get_text())
            most.append(mostchamp[2 + i * 14].get_text())
            most.append(mostchamp[3 + i * 14].get_text())
        else:
            break

    if tiernode == "":
        result = [message_content, level, img, tiername + "  " + lp, win, lose, rate, most]
    else:
        result = [message_content, level, img, tiername + " " + tiernode + "  " + lp, win, lose, rate, most]

    return result


def getImage(name):
    url = name
    res = requests.get(url).content
    im = Image.open(BytesIO(res))
    return im.resize((100, 120))


def getColor(tier):
    color = (0, 0, 0)

    if tier.startswith('Unranked'):
        color = (213, 213, 213)
    elif tier.startswith('Iron'):
        color = (114, 111, 110)
    elif tier.startswith('Bronze'):
        color = (90, 71, 57)
    elif tier.startswith('Silver'):
        color = (190, 200, 209)
    elif tier.startswith('Gold'):
        color = (204, 166, 61)
    elif tier.startswith('Platinum'):
        color = (141, 191, 182)
    elif tier.startswith('Diamond'):
        color = (96, 109, 180)
    elif tier.startswith('Master'):
        color = (178, 85, 186)
    elif tier.startswith('Grandmaster'):
        color = (225, 60, 76)
    elif tier.startswith('Challenger'):
        color = (92, 158, 224)

    return color


def im_show(temp):
    im = Image.new("RGB", (320, 470), getColor(temp[3]))
    im2 = Image.new("RGB", (300, 450), (0, 0, 0))
    table = Image.new("RGB", (10, 10), (30, 32, 44))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("malgunbd.ttf", 17)
    font2 = ImageFont.truetype("malgunbd.ttf", 15)
    im.paste(im2, (10, 10))
    draw.text((20, 20), temp[0], font=font, fill=(255, 255, 255))
    draw.text((20, 50), "레벨", font=font2, fill=(140, 140, 140))
    draw.text((60, 50), temp[1], font=font2, fill=(140, 140, 140))
    im.paste(getImage(temp[2]), (110, 85))
    draw.text((20, 220), "티어 정보", font=font2, fill=(255, 255, 255))
    draw.text((20, 245), temp[3], font=font2, fill=(140, 140, 140,))

    im.show()
