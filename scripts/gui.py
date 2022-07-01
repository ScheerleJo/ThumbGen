from ast import Return
import PySimpleGUI as sg
import thumbGen as tg

dropValues = tg.listSundays()
current = tg.nextSunday()
imgSource = './Images/cache/Thumbnail.png'


def visibleElements(visible:bool):
    """Handle visibility for the 'special Event' functionality"""
    components = ['-DATE-','-SP_DATE-', '-SP_EVENT-', '-DATE_BT-', '-DATE_CONTENT-','-SP_DATE_CONTENT-', '-SP_EVENT_CONTENT-', '-DATE_BT_CONTENT-']
    window['-DROPDOWN-'].update(visible=(not visible))
    window['-DROPDOWN_CONTENT-'].update(visible=(not visible))
    for element in components:
        window[element].update(visible=visible)
    window['-SPECIAL-'].update(value=visible)
    window['-SPECIAL_CONTENT-'].update(value=visible)

def synconizeTabs():
    """Handle the syncronisation between the two tabs for common elements"""
    components = [ '-DROPDOWN', '-LESSON', '-SP_DATE', '-SP_EVENT']
    for element in components:
        window[element + '-'].update(value=values[element + '_CONTENT-'])
        window[element + '_CONTENT-'].update(value=values[element + '-'])

def createContent():
    if values['-SPECIAL-'] == True:
        content = tg.createVideoContent(values, True)
    else :
        content = tg.createVideoContent(values)
    window['-TITLE-'].update(value=content[0])
    window['-DESCRIPTION-'].update(value=content[1])

# region Style and content of the GUI
properties_column = [
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
    [sg.Text('', background_color='#303030')],
    [sg.Text('Schriftgröße:', background_color='#303030')],
    [sg.Slider(range=(10, 90), default_value=90, resolution=1, enable_events=True, key='-SLIDER_ROW1-', orientation='h', size=(34,10), background_color='#303030', trough_color='#640000')],
    [sg.Slider(range=(10, 90), default_value=90, resolution=1, enable_events=True, key='-SLIDER_ROW2-', orientation='h', size=(34,10), background_color='#303030', trough_color='#640000')],
    [sg.Slider(range=(10, 90), default_value=90, resolution=1, enable_events=True, key='-SLIDER_ROW3-', orientation='h', size=(34,10), background_color='#303030', trough_color='#640000')],
    [sg.Text(background_color='#303030')],
    [sg.Button('Vorschau', key='-PREVIEW-', size=(38, 1),button_color='#640000')],
    [sg.Button('Erstellen', key='-CREATE-', size=(38, 1),button_color='#640000')],
]
preview_column = [
    [sg.Text('Vorschau:', background_color='#303030')],
    [sg.Image(size=(640, 360),key='-IMAGE-', subsample=3)],
]
content_properties_layout = [
    [sg.Text('Optionen', background_color='#303030')],
    [sg.Checkbox('Spezial', default=False,background_color='#303030', key='-SPECIAL_CONTENT-', enable_events=True)],
    [
        sg.Text('Datum:', size=(8, 1), background_color='#303030', key="-DATE_CONTENT-"),
        sg.In(key='-SP_DATE_CONTENT-', size=(16, 1)),
        sg.CalendarButton('Datum ändern', size=(12, 1), key='-DATE_BT_CONTENT-', close_when_date_chosen=True, target='-SP_DATE_CONTENT-', format='%d.%m.%Y', no_titlebar=True, button_color='#640000', begin_at_sunday_plus=1,)
    ],
    [
        sg.Text('Event:', size=(8, 1), background_color='#303030'),
        sg.Combo(values=dropValues, default_value=current, size=(30, 1), key='-DROPDOWN_CONTENT-', readonly=True, enable_events=True, button_background_color='#640000'),
        sg.In(key='-SP_EVENT_CONTENT-', size=(32, 1)),
    ],
    [
        sg.Text('Bibelstelle:', size=(8, 1), background_color='#303030'),
        sg.In(key='-LESSON_CONTENT-', size=(32, 1), enable_events=True),
    ],
    [
        sg.Text('Prediger:', size=(8, 1), background_color='#303030'),
        sg.In(key='-PREACHER-', size=(32, 1), enable_events=True),
    ],
    [
        sg.Text('Thema:', size=(8, 1), background_color='#303030'),
        sg.In(key='-THEME-', size=(32, 1), enable_events=True),
    ],
    [sg.Button('Erstellen', key='-CREATE_CONTENT-', size=(38, 1),button_color='#640000')],
]
content_preview_layout = [
    [
        sg.Text('Titel:', background_color='#303030'),
        sg.In(default_text='', key='-TITLE-', size=(66, 1))
    ],
    [sg.Text('Videobeschreibung:', background_color='#303030')],
    [sg.Multiline(default_text='', key='-DESCRIPTION-', size=(70, 10), sbar_background_color='#640000')]
]
layout= [
    [
        sg.TabGroup([
            [
                sg.Tab('Thumbnail', [
                    [
                        sg.Column(layout = properties_column, background_color='#303030', vertical_alignment='top'),
                        sg.VSeparator(),
                            sg.Column(layout = preview_column, background_color='#303030'),
                    ]
                ], background_color='#303030'),
                sg.Tab('Video Content', [
                    [
                        sg.Column(layout=content_properties_layout, background_color='#303030', vertical_alignment='top'),
                        sg.VSeperator(),
                        sg.Column(layout=content_preview_layout, background_color='#303030', vertical_alignment='top'),
                    ]
                ], background_color='#303030')
            ]
            ], key='-group1-', tab_location='top', selected_title_color='#640000', background_color='#282828', border_width=1, tab_background_color='#444444', selected_background_color='#444444', title_color='#FFFFFF')
    ]
]
# endregion

window = sg.Window(title='Thumbnail-Generator',layout=layout, background_color='#282828', finalize=True, icon='./Images/icon.ico')

#   Code after Startup to show next Sunday as img in cache
tg.modifyThumbnail(tg.splitString(current))
window['-IMAGE-'].update(imgSource, subsample=3)


visibleElements(False)
#   Main-Loop
while True:
    event, values = window.read()

    spDate = values['-SP_DATE-']
    spName = values['-SP_EVENT-']
    
    synconizeTabs()

    if event == sg.WIN_CLOSED:
        break

    match event:
        case '-CREATE-':
            if values['-SPECIAL-'] == True:
                tg.updateThumbnail(sunday=[spDate, spName], values=values, show=True)
            tg.updateThumbnail(values, True)
        case '-PREVIEW-':
            if values['-SPECIAL-'] == True:
                tg.updateThumbnail(values, [spDate, spName], show = False)
            else:
                tg.updateThumbnail(values, False)
            window['-IMAGE-'].update(imgSource, subsample=3)

        case '-CREATE_CONTENT-':
            createContent()


        case '-DROPDOWN-':
            tg.updateThumbnail(values, False)
            window['-IMAGE-'].update(imgSource, subsample=3)

        case '-SPECIAL-':
            if values['-SPECIAL-'] == True:
                visibleElements(True)
            else:
                visibleElements(False)
        case '-SPECIAL_CONTENT-':
            if values['-SPECIAL_CONTENT-'] == True:
                visibleElements(True)
            else:
                visibleElements(False)

window.close()
