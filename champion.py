import discord
import requests
import time as t
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from chamDB import chamdb

baseurl = "http://fow.kr/stats/"
pos = {"탑" : "top", "미드" : "middle", "정글" : "jungle", "원딜" : "bottom", "서폿" : "utility"}

def champion(message):
    message_content = message.content.replace("!챔피언 ", "")
    temp = list(message_content.split(" "))
    line, name = temp[0], temp[1]

    if line not in pos:
        embed = discord.Embed(title="잘못된 라인 명칭", description="다음 중 하나를 입력해주세요. \n`탑`, `정글`, `미드`, `원딜`, `서폿`", color=0x62c1cc)
        return embed
    if chamdb(name) == -1:
        embed = discord.Embed(title="잘못된 챔피언 명", description="오타가 있는지 확인해주세요.", color=0x62c1cc)
        return embed

    url = baseurl + chamdb(name) + "/" + pos[line]
    res = requests.get(url).text
    soup = BeautifulSoup(res, "html.parser")


    lineinfo = soup.find("div", attrs={"class" : "position_selected"})
    icon_url = lineinfo.find('img').get('src')
    line_name = line
    temp = lineinfo.find('span').get_text()
    temp = temp.split("\n")
    del temp[0]
    del temp[3]
    temp[0] = "챔피언 라인 픽률 " + temp[0]
    line_info = [icon_url, line_name, temp]

    iteminfo = soup.select('body > div:nth-child(4) > div > div:nth-child(1) > div:nth-child(12) > div:nth-child(1) > div:nth-child(2) > table > tbody')
    print(type(iteminfo[0]))

    item = iteminfo[0].find_all("img")
    item = [i.get("src") for i in item]
    temp = iteminfo[0].get_text()
    temp = temp.replace("▶", "")
    temp = temp.replace(" ", "")
    temp = list(temp.split("\n"))
    temp = [i for i in temp if i != ""]

    #반환 형태 설명
    #item 배열은 [1번템트리 1번이미지, 1번템트리 2번이미지, 1번템트리 3번이미지, 2번템트리 1번이미지...]
    #즉, 0~2 한셋, 3~5 한셋, 6~8 한셋 총 3세트 이용

    #temp 배열은 [1번템트리 픽률, 1번템트리 승률, 1번템트리 표본, 2번템트리 픽률...]

    embed = discord.Embed(title="더미", description="더미", color=0x62c1cc)
    return embed

"""
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
"""

"""
def getImage(name):
    url = name
    res = requests.get(url).content
    im = Image.open(BytesIO(res))
    return im.resize((100, 120))


def getColor(tier):
    color = (0, 0, 0)
    color2 = (0, 0, 0)

    if tier.startswith('Unranked'):
        color = (213, 213, 213)
        color2 = (143, 143, 143)
    elif tier.startswith('Iron'):
        color = (114, 111, 110)
        color2 = (103, 79, 76)
    elif tier.startswith('Bronze'):
        color = (90, 71, 57)
        color2 = ()
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

    return color, color2


def im_show(temp):
    im = Image.new("RGB", (360, 510), getColor(temp[3])[0])
    im2 = Image.new("RGB", (320, 470), (0, 0, 0))
    im3 = Image.new("RGB", (340, 490), getColor(temp[3])[1])
    table = Image.new("RGB", (10, 10), (30, 32, 44))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("malgunbd.ttf", 17)
    font2 = ImageFont.truetype("malgunbd.ttf", 15)
    im.paste(im3, (10, 10))
    im.paste(im2, (20, 20))
    draw.text((40, 35), temp[0], font=font, fill=(255, 255, 255))
    draw.text((40, 60), "레벨", font=font2, fill=(140, 140, 140))
    draw.text((80, 60), temp[1], font=font2, fill=(140, 140, 140))
    im.paste(getImage(temp[2]), (130, 90))
    draw.text((40, 225), "티어 정보", font=font2, fill=(255, 255, 255))
    draw.text((40, 250), temp[3], font=font2, fill=(140, 140, 140,))

    im.show()
"""