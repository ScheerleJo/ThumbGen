# -*- coding: iso-8859-1 -*-
from PIL import Image, ImageDraw, ImageFont
from icalendar import Calendar
from datetime import datetime, timedelta
import os
import sys

def nextSunday():
    d = datetime.today()
    days_ahead = 6 - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    nextDate = d + timedelta(days_ahead)
    thumbnailName = getName((nextDate.strftime('%Y-%m-%d')))
    thumbnailDate = nextDate.strftime('%d.%m.%Y')
    return thumbnailDate, thumbnailName

def modifyThumbnail(lesson):
    nextDate = nextSunday()[0]
    sunday = nextSunday()[1]
    image = Image.open("./thumbnail_raw.png")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("tahoma.ttf", 90)

    #Write the 3 Lines of Text
    draw.text((654, 515), nextDate, (63, 63, 63), font=font)
    draw.text((654, 638), sunday, (63, 63, 63), font=font)
    draw.text((654, 761), lesson, (167, 22, 128), font=font)

    #save Thumbnail
    path = './Thumbnail ' + nextDate + '.png'
    image.save(path)
    print('Thumbnail was successfully generated')
    os.startfile(os.getcwd())

def createCurrentThumbnail():
    lesson = input('Enter the lesson for this Sunday: ')
    modifyThumbnail(lesson.upper())

def getName(date):
    g = open('kirchenjahr-evangelisch.ics','rb')
    gcal = Calendar.from_ical(g.read())
    for component in gcal.walk():
        if component.name == "VEVENT":
            if date == str(component.decoded('dtstart')):
                name = component.get('summary').upper()
                g.close()
                return name
    g.close()
    print('No matching result was found! Check if the Calendar is up to date.')
    input('Press any key to close the application...')
    sys.exit()

createCurrentThumbnail()

# for a future version make the filename of the calendar dynamic
#f = []
#os.walk(dirpath, dirnames)