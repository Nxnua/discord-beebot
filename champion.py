import discord
import requests
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
        return -1
    if chamdb(name) == -1:
        return -2

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
    line_info = [pic_url, name, line_name, temp]

    iteminfo = soup.select('body > div:nth-child(4) > div > div:nth-child(1) > div:nth-child(12) > div:nth-child(1) > div:nth-child(2) > table > tbody')

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

    for i in range(3):
        if len(temp) >= (i + 1) * 3:
            im.paste(getItemImage(item[0 + i * 3]), (30, i*100+290))
            draw.text((120, i*100+310), "▶", font=font3, fill=(255, 255, 255))
            im.paste(getItemImage(item[1 + i * 3]), (150, i*100+290))
            draw.text((240, i*100+310), "▶", font=font3, fill=(255, 255, 255))
            im.paste(getItemImage(item[2 + i * 3]), (270, i*100+290))
            draw.text((400, i*100+310), temp[0 + i * 3], font=font2, fill=(160, 160, 160))
            draw.text((530, i*100+310), temp[1 + i * 3], font=font2, fill=(160, 160, 160))
            draw.text((660, i*100+310), temp[2 + i * 3], font=font2, fill=(160, 160, 160))
        else:
            break


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



    #embed = discord.Embed(title="더미", description="더미", color=0x62c1cc)
    #return embed


