from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
import json


def nextSunday():
    d = datetime.today()
    days_ahead = 6 - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return (d + timedelta(days_ahead)).strftime('%d.%m.%Y')


def createThumbnail(sunday:str, lesson:str):
    nextDate = nextSunday()
    image = Image.open("./thumbnail_raw.png")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("tahoma.ttf", 90)

    #Write the 3 Lines of Text
    draw.text((654, 515), nextDate, (63, 63, 63), font=font)
    draw.text((654, 638), sunday, (63, 63, 63), font=font)
    draw.text((654, 761), lesson, (167, 22, 128), font=font)

    #save Thumbnail
    path = "./Thumbnail " + nextDate + ".png"
    image.save(path)

with open('./thumbnail.json') as f:
    data = json.load(f)
createThumbnail(data['name'], data['lesson'])