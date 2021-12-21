import discord
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


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
        color2 = (99, 98, 98)
    elif tier.startswith('Silver'):
        color = (145, 165, 173)
        color2 = (130, 113, 97)
    elif tier.startswith('Gold'):
        color = (204, 166, 61)
        color2 = (71, 123, 84)
    elif tier.startswith('Platinum'):
        color = (57, 157, 140)
        color2 = (96, 215, 140)
    elif tier.startswith('Diamond'):
        color = (87, 73, 172)
        color2 = (207, 138, 241)
    elif tier.startswith('Master'):
        color = (150, 68, 191)
        color2 = (244, 99, 237)
    elif tier.startswith('Grandmaster'):
        color = (84, 59, 59)
        color2 = (252, 61, 67)
    elif tier.startswith('Challenger'):
        color = (2, 135, 230)
        color2 = (232, 223, 180)

    return color, color2


def search(message):
    message_content = message.content.replace("!유저 ", "")
    plusurl = message_content.replace(" ", "")
    url = baseurl + "/kr/profile/" + plusurl
    res = requests.get(url).text
    soup = BeautifulSoup(res, "html.parser")

    url_ = levelurl + plusurl
    res_ = requests.get(url_).text
    soup_ = BeautifulSoup(res_, "html.parser")

    if soup_.find("a", attrs={"class": "sbtn small"}) == None:
        return -1

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
            temp = mostchamp[0 + i * 14].find('img').get('alt') + "   "
            temp += mostchamp[1 + i * 14].get_text() + "   "
            temp += mostchamp[2 + i * 14].get_text() + "   "
            temp += mostchamp[3 + i * 14].get_text()
            most.append(temp)
        else:
            break

    if tiernode == "":
        temp = [message_content, level, img, tiername + "  " + lp, win + " " + lose + "  " + rate, most]
    else:
        temp = [message_content, level, img, tiername + " " + tiernode + "  " + lp, win + " " + lose + "  " + rate, most]

    im = Image.new("RGB", (360, 565), getColor(temp[3])[0])
    im2 = Image.new("RGB", (320, 525), (0, 0, 0))
    im3 = Image.new("RGB", (340, 545), getColor(temp[3])[1])
    table = Image.new("RGB", (320, 305), (30, 32, 44))
    table2 = Image.new("RGB", (300, 93), (54, 54, 61))
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("malgunbd.ttf", 17)
    font2 = ImageFont.truetype("malgunbd.ttf", 15)
    im.paste(im3, (10, 10))
    im.paste(im2, (20, 20))
    draw.text((40, 35), temp[0], font=font, fill=(255, 255, 255))
    draw.text((40, 60), "레벨", font=font2, fill=(140, 140, 140))
    draw.text((80, 60), temp[1], font=font2, fill=(140, 140, 140))
    im.paste(getImage(temp[2]), (130, 90))
    im.paste(table, (20, 240))
    draw.text((40, 255), "티어 정보", font=font2, fill=(255, 255, 255))
    draw.text((40, 280), temp[3], font=font2, fill=(140, 140, 140))
    draw.text((40, 320), "승/패 | 승률", font=font2, fill=(255, 255, 255))
    draw.text((40, 350), temp[4], font=font2, fill=(140, 140, 140))
    draw.text((40, 390), "모스트 챔피언", font=font2, fill=(255, 255, 255))
    draw.text((40, 410), "챔피언 | 게임 수 | 승률 | KDA", font=font2, fill=(188, 188, 188))
    im.paste(table2, (30, 438))

    for i in range(3):
        if len(mostchamp) >= (i + 1) * 14:
            draw.text((40, 447 + i * 26), temp[5][i], font=font2, fill=(160, 160, 160))
        else:
            break

    with BytesIO() as image_binary:
        im.save(image_binary, "png")
        image_binary.seek(0)
        out = discord.File(fp=image_binary, filename="image.png")

    return out


def getImage(name):
    url = name
    res = requests.get(url).content
    im = Image.open(BytesIO(res))
    return im.resize((100, 120))
