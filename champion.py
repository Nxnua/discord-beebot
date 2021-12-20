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
    pic = soup.find("div", attrs={"class" : "champ_solo"})
    pic_url = pic.find('img').get('src')
    icon_url = lineinfo.find('img').get('src')
    line_name = line
    temp = lineinfo.find('span').get_text()
    temp = temp.split("\n")
    del temp[0]
    del temp[3]
    temp[0] = "픽률 " + temp[0]
    print(pic_url)
    line_info = [pic_url, name, line_name, temp]
    print(line_info)

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

    im = Image.new("RGBA", (800, 600), (30, 32, 44, 1000))
    table2 = Image.new("RGBA", (560, 178), (54, 54, 61, 1000))
    table3 = Image.new("RGBA", (760, 360), (66, 67, 76, 1000))
    table4 = Image.new("RGBA", (760, 100), (54, 54, 61, 1000))
    draw = ImageDraw.Draw(im)
    im.paste(getChampImage(line_info[0]), (20, 20))
    im.paste(table2, (220, 21))
    font = ImageFont.truetype("malgunbd.ttf", 35)
    font2 = ImageFont.truetype("malgunbd.ttf", 30)
    font3 = ImageFont.truetype("malgunbd.ttf", 23)
    draw.text((240, 45), line_info[1], font=font, fill=(255, 255, 255))
    im.paste(getIconImage(line_info[2]), (240, 110))
    draw.text((320, 117), line_info[2], font=font2, fill=(160, 160, 160))
    draw.text((580, 40), line_info[3][0], font=font2, fill=(160, 160, 160))
    draw.text((580, 90), line_info[3][1], font=font2, fill=(160, 160, 160))
    draw.text((580, 140), line_info[3][2], font=font2, fill=(160, 160, 160))
    im.paste(table3, (20, 220))
    im.paste(table4, (20, 280))
    im.paste(table4, (20, 480))

    draw.text((145, 230), "템트리", font=font2, fill=(255, 255, 255))
    draw.text((400, 230), "픽률", font=font2, fill=(255, 255, 255))
    draw.text((530, 230), "승률", font=font2, fill=(255, 255, 255))
    draw.text((660, 230), "표본", font=font2, fill=(255, 255, 255))

    im.paste(getItemImage(item[0]), (30, 290))
    draw.text((120, 310), "▶", font=font3, fill=(255, 255, 255))
    im.paste(getItemImage(item[1]), (150, 290))
    draw.text((240, 310), "▶", font=font3, fill=(255, 255, 255))
    im.paste(getItemImage(item[2]), (270, 290))
    draw.text((400, 310), temp[0], font=font2, fill=(160, 160, 160))
    draw.text((530, 310), temp[1], font=font2, fill=(160, 160, 160))
    draw.text((660, 310), temp[2], font=font2, fill=(160, 160, 160))

    im.paste(getItemImage(item[3]), (30, 390))
    draw.text((120, 410), "▶", font=font3, fill=(255, 255, 255))
    im.paste(getItemImage(item[4]), (150, 390))
    draw.text((240, 410), "▶", font=font3, fill=(255, 255, 255))
    im.paste(getItemImage(item[5]), (270, 390))
    draw.text((400, 410), temp[3], font=font2, fill=(160, 160, 160))
    draw.text((530, 410), temp[4], font=font2, fill=(160, 160, 160))
    draw.text((660, 410), temp[5], font=font2, fill=(160, 160, 160))

    im.paste(getItemImage(item[6]), (30, 490))
    draw.text((120, 510), "▶", font=font3, fill=(255, 255, 255))
    im.paste(getItemImage(item[7]), (150, 490))
    draw.text((240, 510), "▶", font=font3, fill=(255, 255, 255))
    im.paste(getItemImage(item[8]), (270, 490))
    draw.text((400, 510), temp[6], font=font2, fill=(160, 160, 160))
    draw.text((530, 510), temp[7], font=font2, fill=(160, 160, 160))
    draw.text((660, 510), temp[8], font=font2, fill=(160, 160, 160))

    with BytesIO() as image_binary:
        im.save(image_binary, "png")
        image_binary.seek(0)
        out = discord.File(fp=image_binary, filename="image.png")

    return out


def getItemImage(name):
    url = name
    res = requests.get("http:" + url).content
    im = Image.open(BytesIO(res))
    return im.resize((80, 80))

def getChampImage(name):
    url = name
    res = requests.get("http:" + url).content
    im = Image.open(BytesIO(res))
    return im.resize((180, 180))

def getIconImage(name):
    if name == "탑":
        res = requests.get("https://ww.namu.la/s/0dc95182a4e2a4f3c97be3ac9909c1492fa0c5f7be6f36d1175ba57789f3bfe90c276c4a9402318b85c5e0b8496359246c449c157d7877613d8ddca92312c45b8d5cb375e54e9ef5439e2af902db67e5efe30c1e6221fb1aafbfe2ce881dcfae").content
    elif name == "미드":
        res = requests.get("https://w.namu.la/s/1b6270f98f05664ec13bbceff94bbf79fc45013afd587f80bf13ef4c863d4f2cf9e85c11470aef1ed95aac82856a8245940a583a1d2165ec6bd84a2bfb2c1b638d202ceb8381bfaf3c70e0be9b861717b132b5c831bf95bb844267e7ead0c08a").content
    elif name == "정글":
        res = requests.get("https://ww.namu.la/s/305ed8a606058e624a75b072b443973b7282faed5926447c6d3d6d465d14b1f428be251d3158b1d5bbd388dbd394eae6f2a00cbf32d7b5407b4e80fdcd1d18dff845327c001e6d972770cace6c9bd4747688ccae727c085ce576c5099e9a120a").content
    elif name == "원딜":
        res = requests.get("https://w.namu.la/s/7f916b343072a3f9ea7eb9ddefc3f6e3017afe24da3d0c1d039c87ce3906deb627973515e12626a9dd618d7fabee42ee9afbf3427fff1fd51a430aeb80a0a1b5d9dcf9cb10a8e401084f4ac8e5ea5d7f40a3a4f4644cdb4781374bca700dd6cd").content
    else:
        res = requests.get("https://w.namu.la/s/b151ed5a28ee76f5155075d591fd6fda9d3a20f33ce96b493054af61e4655310cf18353afb0b85755501cc130c0b38a3844baaad9fff71ec3e20ff542e5a0641eb24c77381d52999c7b5579802bc0b877fc4b1cb24492980bed88d9ab69b6377").content
    im = Image.open(BytesIO(res))
    return im.resize((60, 60))


    """
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
   """
    #embed = discord.Embed(title="더미", description="더미", color=0x62c1cc)
    #return embed


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