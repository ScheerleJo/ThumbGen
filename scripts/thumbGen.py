# -*- coding: iso-8859-1 -*-
from PIL import Image, ImageDraw, ImageFont
from icalendar import Calendar
from datetime import datetime, timedelta
import os
import error

fontSize1 = 90
fontSize2 = 90
fontSize3 = 90
fontFamily ='tahoma.ttf'

def nextSunday():
    d = datetime.today()
    days_ahead = 6 - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    nextDate = d + timedelta(days_ahead)
    thumbnailName = getName((nextDate.strftime('%Y-%m-%d')))
    thumbnailDate = nextDate.strftime('%d.%m.%Y')
    return thumbnailName + ' (' + thumbnailDate + ')'

def updateThumbnail(values, show, sunday = None, lesson = None):
    date = values['-DROPDOWN-'].split(' (')     # value consists of: name (date) ---> create array of [0] = date, [1] = name
    if sunday == None:
        sunday = [(date[1]).strip(')'), date[0].upper()]
    lesson = values['-LESSON-'].upper()
    if show == True:
        path = './thumbnails/Thumbnail ' + sunday[0] + '.png'
    else:
        path = './Images/cache/Thumbnail.png'
        
    fs1 = int(values['-SLIDER_ROW1-'])
    fs2 = int(values['-SLIDER_ROW2-'])
    fs3 = int(values['-SLIDER_ROW3-'])
    modifyThumbnail(sunday, lesson, path, show, fs1, fs2, fs3)

def modifyThumbnail(sunday, lesson, path, show, fs1 = 90, fs2 = 90, fs3 = 90):
    nextDate = sunday[0]
    sunday = sunday[1]
    image = Image.open("./Images/thumbnail_raw.png")
    draw = ImageDraw.Draw(image)
    font1 = ImageFont.truetype(fontFamily, fs1)
    font2 = ImageFont.truetype(fontFamily, fs2)
    font3 = ImageFont.truetype(fontFamily, fs3)

    #Write the 3 Lines of Text
    draw.text((654, 515), nextDate, (63, 63, 63), font=font1)
    draw.text((654, 638), sunday, (63, 63, 63), font=font2)
    draw.text((654, 761), lesson, (167, 22, 128), font=font3)

    #save Thumbnail
    image.save(path)
    if show == True:
        print('Thumbnail was successfully generated')
        os.startfile(os.getcwd() + '/thumbnails')



def getName(date):
    i = 0
    for items in getCalFiles():
        g = open(items,'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                if date == str(component.decoded('dtstart')):
                    name = component.get('summary')
                    g.close()
                    return name
        g.close()
    error.message('No matching result was found! Check if the Calendar is up to date.')

def listSundays():
    sundays = []
    for items in getCalFiles():
        g = open(items,'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                calDate= str(component.decoded('dtstart')).split('-')
                date = calDate[2] + '.' + calDate[1] + '.' + calDate[0]
                value = component.get('summary') + " (" + date + ')'
                sundays.append(value)
        g.close()
    return sundays

def getCalFiles():
    f = []
    files = []
    for (dirpath, dirnames, filenames) in os.walk('./'):
        f.extend(filenames)
        break

    for item in f:
        if str(item).endswith(('.ics')):
            if item not in files:
                files.append(item)
    return files