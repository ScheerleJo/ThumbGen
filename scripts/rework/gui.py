import PySimpleGUI as sg
import thumb_gen as tg
import read_word as rw
import ical_utility as ical
import clipboard_utility as clipboard

dropValues = ical.listSundays()
current = tg.nextSunday()
imgSource = 'C:/Windows/Temp/TumbGen_CacheData.png'

def visibleSpecialElements(visible:bool, dropdownvalue = ""):
    """Handle visibility for the 'special Event' functionality"""
    components = ['-DATE-','-SP_DATE-', '-SP_EVENT-', '-DATE_BT-']
    for element in components:
        window[element].update(visible=visible)

    window['-SPECIAL-'].update(value=visible)
    window['-DROPDOWN-'].update(visible=(not visible))

    if visible == True:
        currentEvent = tg.splitString(dropdownvalue)
        window['-SP_DATE-'].update(value=(currentEvent[0]))
        window['-SP_EVENT-'].update(value=(currentEvent[1]))

def createContent(saveThumbnail:bool):
    """Create Thumbnail, Title and Videodescription"""

    tg.gatherThumbnailInfo(saveThumbnail)

    content = tg.createVideoContent()
    window['-TITLE-'].update(value=content[0])
    window['-DESCRIPTION-'].update(value=content[1])

def readWordFile(initial:bool = False):
    #For Lesson and Theme:
    combinedData = rw.getContentInTable(2, "Predigt", current=initial)
    if combinedData != None:
        lessonData = combinedData.splitlines()
        window['-LESSON-'].update(value=lessonData[0])
        window['-THEME-'].update(value=lessonData[1])

    #For Preacher:
    preacherData = rw.getContentInTable(1, "Prediger", current=initial)
    window['-PREACHER-'].update(value=preacherData)

def copyData(content:str):
    clipboard.setData(content)
    window['-SUCC_COPY-'].update(visible=(clipboard.checkData(content)))

# region Style and content of the GUI
thumbnail_properties_column = [
    [sg.Text('Optionen', background_color='#303030')],
    [sg.Checkbox('Spezial', default=False,background_color='#303030', key='-SPECIAL-', enable_events=True)],
    [
        sg.Text('Datum:', size=(8, 1), background_color='#303030', key="-DATE-"),
        sg.In(key='-SP_DATE-', size=(16, 1)),
        sg.CalendarButton('Datum ändern', size=(12, 1), key='-DATE_BT-', close_when_date_chosen=True, target='-SP_DATE-', format='%d.%m.%Y', no_titlebar=True, button_color='#640000', begin_at_sunday_plus=1,)
    ],
    [
        sg.Text('Event:', size=(8, 1), background_color='#303030'),
        sg.Combo(values=dropValues, default_value=current, size=(30, 1), key='-DROPDOWN-', readonly=True, enable_events=True, button_background_color='#640000'),
        sg.In(key='-SP_EVENT-', size=(32, 1)),
    ],
    [
        sg.Text('Bibelstelle:', size=(8, 1), background_color='#303030'),
        sg.In(key='-LESSON-', size=(32, 1), enable_events=True),
    ],
        [
        sg.Text('Prediger:', size=(8, 1), background_color='#303030'),
        sg.In(key='-PREACHER-', size=(32, 1), enable_events=True),
    ],
    [
        sg.Text('Thema:', size=(8, 1), background_color='#303030'),
        sg.In(key='-THEME-', size=(32, 1), enable_events=True),
    ],
    [sg.Text('', background_color='#303030')],
    [sg.Text('Schriftgröße:', background_color='#303030')],
    [sg.Slider(range=(10, 90), default_value=90, resolution=1, enable_events=True, key='-SLIDER_ROW1-', orientation='h', size=(34,10), background_color='#303030', trough_color='#640000')],
    [sg.Slider(range=(10, 90), default_value=90, resolution=1, enable_events=True, key='-SLIDER_ROW2-', orientation='h', size=(34,10), background_color='#303030', trough_color='#640000')],
    [sg.Slider(range=(10, 90), default_value=90, resolution=1, enable_events=True, key='-SLIDER_ROW3-', orientation='h', size=(34,10), background_color='#303030', trough_color='#640000')],
    [sg.Text(background_color='#303030')],
    [sg.Button('Vorschau', key='-PREVIEW-', size=(38, 1),button_color='#640000')],
    [sg.Button('Erstellen', key='-CREATE-', size=(38, 1),button_color='#640000')],
]
thumbnail_preview_column = [
    [sg.Text('Vorschau:', background_color='#303030')],
    [sg.Image(key='-IMAGE-',source=imgSource , subsample=3)],
    [
        sg.Column([[sg.Text('Titel:               ', background_color='#303030'),]], background_color='#303030', pad=0),
        sg.Column([[sg.In(default_text='', key='-TITLE-', size=(66, 1)),]], background_color='#303030', pad=0),
        sg.Column([[sg.Button('Kopieren', key='-COPY_TITLE-', button_color='#640000')]], background_color='#303030', pad=0),
    ],
    [
        sg.Column([[sg.Text('Beschreibung: ', background_color='#303030', justification='top')]], vertical_alignment='top', background_color='#303030', pad=0),
        sg.Column([[sg.Multiline(default_text='', key='-DESCRIPTION-', size=(64, 7), sbar_background_color='#640000')]], background_color='#303030', pad=0),
        sg.Column([
            [sg.Button('Kopieren', key='-COPY_DESCRIPTION-', button_color='#640000')],
            [sg.Text(background_color='#303030')],
            [sg.Text(background_color='#303030')],
            [sg.Text(background_color='#303030')],
            [sg.Text('Kopiert!', key='-SUCC_COPY-', background_color='#303030', text_color='#00FF00')],
        ], vertical_alignment='top', background_color='#303030', pad=0),
    ],
]
layout= [
    [
        [
            sg.Column(layout = thumbnail_properties_column, background_color='#303030', vertical_alignment='top'),
            sg.VSeparator(),
            sg.Column(layout = thumbnail_preview_column, background_color='#303030'),
        ]
    ]
]
# endregion

window = sg.Window(title='Thumbnail-Generator',layout=layout, background_color='#303030', finalize=True, icon='./Images/icon.ico')

# Code after Startup to show next Sunday as img in cache
visibleSpecialElements(False)
window['-SUCC_COPY-'].update(visible=False)

event, values = window.read(timeout=50)
tg.setValues(values)
readWordFile(True)
    # Short Timeout for the script to be able to load the data given from the .ics and .docx files
event, values = window.read(timeout=100)
    # Create the Thumbnail and Content (Title and Videodescription) initially to preview it and check for errors in the data
    # tg.setValues() needs to be set twice because the values change after readWord file
tg.setValues(values)
createContent(False)
window['-IMAGE-'].update(source=imgSource, subsample=3)



#   Main-Loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    window['-SUCC_COPY-'].update(visible=False)

    match event:
        case '-CREATE-':
            tg.setValues(values)
            createContent(True)

        case '-PREVIEW-':
            tg.setValues(values)
            createContent(False)
            window['-IMAGE-'].update(imgSource, subsample=3)

        case '-DROPDOWN-':
            tg.setValues(values)
            tg.gatherThumbnailInfo(False)
            window['-IMAGE-'].update(imgSource, subsample=3)

        case '-SPECIAL-':
            visibleSpecialElements(values['-SPECIAL-'], values['-DROPDOWN-'])

        case '-COPY_DESCRIPTION-':
            copyData(values['-DESCRIPTION-'])

        case '-COPY_TITLE-':
            copyData(values['-TITLE-'])

window.close()