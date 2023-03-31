from icalendar import Calendar
from tkinter import messagebox
import os
import json_utility as json

def getSundayName(date):
    i = 0
    for items in getCalFiles():
        g = open(json.getPath('calendarLocation') + items,'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                if date == str(component.decoded('dtstart')):
                    name = component.get('summary')
                    g.close()
                    return name
        g.close()
    # messagebox.showerror('Thumbnail-Generator', 'Es konnte kein Eintrag  in den .ics gefunden werden. Bitte überprüfe den Dateipfad')
    # return ValueError('No Entry could be found. Please check the file location')

def listSundays() -> list:
    """Create a list for the Dropdown-menu in the GUI."""
    # For this it uses all the .ics files found by getCalFiles()
    sundays = []
    calFiles = getCalFiles()
    for file in calFiles:
        g = open(json.getPath('calendarLocation') + file,'rb')
        gcal = Calendar.from_ical(g.read())
        for component in gcal.walk():
            if component.name == "VEVENT":
                # Generate a list with the events in the calendar with name (here: summary) and date (here: dtstart)
                calDate= str(component.decoded('dtstart')).split('-')
                date = calDate[2] + '.' + calDate[1] + '.' + calDate[0]
                value = component.get('summary') + " (" + date + ')'
                sundays.append(value)
        g.close()
    if sundays != []:
        return sundays
    # messagebox.showerror('Thumbnail-Generator', 'D')
    # return ValueError('Empty List')


def getCalFiles() -> list:
    """Search the current directory for .ics files"""
    files = []
    # os.walk to get all objects in the directory
    path =  json.getPath('calendarLocation')
    for (dirpath, dirnames, filenames) in os.walk(path):
        files.extend(filenames)
        break

    length:int = len(files) - 1
    i:int = 0
    while i <= length:
        item = files[i]
        if str(item).endswith(('.ics')) == False:
            files.remove(item)
            length -= 1
        else:
            i += 1
    if files != []:
        return files
    
    # messagebox.showerror('Thumbnail-Generator', 'Es wurde keine Dateien mit Endung .ics gefunden im Pfad:\n' + json.getPath('calendarLocation'))
    # return ValueError('Missing result for search query')