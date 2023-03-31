from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timedelta
import ical_utility as ical
import os
from tkinter import messagebox

fontSize1:int = 90
fontSize2:int = 90
fontSize3:int = 90
fontFamily:str ='tahoma.ttf'

values: tuple = []

def setValues(guiValues:tuple):
    values = guiValues

def splitString(input:str):
    date = input.split(' (')     # value consists of: name (date) ---> create array of [0] = date, [1] = name
    return (date[1]).strip(')'), date[0]

def nextSunday():
    d = datetime.today()
    days_ahead = 6 - d.weekday()
    if days_ahead < 0: # Target day already happened this week
        days_ahead += 7
    nextDate = d + timedelta(days_ahead)
    thumbnailName = ical.getSundayName((nextDate.strftime('%Y-%m-%d')))
    thumbnailDate = nextDate.strftime('%d.%m.%Y')
    return thumbnailName + ' (' + thumbnailDate + ')'

def checkForSpecialEvent():
    if(values['-SPECIAL-'] == False):
        sunday = splitString(values['-DROPDOWN-'])
    else :
        sunday = [values['-SP_DATE-'], values['-SP_EVENT-']]
    return sunday

def createVideoContent():
    """Create the videotitle and description for standard livestreams"""
    lesson=values['-LESSON-']
    preacher=values['-PREACHER-']
    theme=values['-THEME-']
    # dropdown | spdate & spevent, special, lesson, preacher, theme 
    sunday = checkForSpecialEvent(values)

    url = 'https://www.bibleserver.com/LUT/' + lesson
    title = theme + ' - ' + 'Gottesdienst am ' + sunday[0]
    description = 'Livestream vom Gottesdienst am Sonntag, ' + sunday[0] + ' aus der Kirche der evangelischen Kirchengemeinde Hohenhaslach.\nPrediger ist ' + preacher + ', der zum Thema "' + theme + '" spricht.\nDen Bibeltext ' + lesson +' zum nachlesen gibt es hier: ' + url + '\n\nVielen Dank an alle, die mitgeholfen haben, dass dieser Gottesdienst stattfinden kann!\n\n'
    return title, description

def gatherThumbnailInfo(saveThumbnail:bool):
    """Gahter all required information to create a thumbnail"""
    sunday = checkForSpecialEvent(values)

    lesson = values['-LESSON-'].upper()
    
    fs1 = int(values['-SLIDER_ROW1-'])
    fs2 = int(values['-SLIDER_ROW2-'])
    fs3 = int(values['-SLIDER_ROW3-'])
    modifyThumbnail(sunday, lesson, saveThumbnail, fs1, fs2, fs3)

def modifyThumbnail(sunday:tuple, lesson:str = '', saveThumbnail:bool = False, fs1:int = 90, fs2:int = 90, fs3:int = 90):
    """Manipulate the template to create a new thumbnail for either cache or the end-use"""
        
    nextDate = sunday[0]
    sunday = sunday[1].upper()
    image = Image.open("./Images/thumbnail_raw.png")
    draw = ImageDraw.Draw(image)
    font1 = ImageFont.truetype(fontFamily, fs1)
    font2 = ImageFont.truetype(fontFamily, fs2)
    font3 = ImageFont.truetype(fontFamily, fs3)

    #Write the 3 Lines of Text
    draw.text((654, 515), nextDate, (63, 63, 63), font=font1)
    draw.text((654, 638), sunday, (63, 63, 63), font=font2)
    draw.text((654, 761), lesson, (167, 22, 128), font=font3)

    #save Thumbnail to use it or stash it in a temporary cache
    if saveThumbnail == True:
        path = './thumbnails/Thumbnail ' + nextDate + '.png'
        os.startfile(os.getcwd() + '/thumbnails')
    else:
        path = 'C:/Windows/Temp/TumbGen_CacheData.png'

    image.save(path)

