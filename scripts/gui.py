import PySimpleGUI as sg
import thumbGen as tg

dropValues = tg.listSundays()
current = tg.nextSunday()
imgSource = './cache/Thumbnail.png'
startup = False

#      Style and content of the GUI
properties_column = [
    [sg.Text('Optionen', background_color='#282828')],
    [sg.Checkbox('Spezial', default=False,background_color='#282828', key='-SPECIAL-', enable_events=True)],
    [
        sg.Text('Datum:', size=(8, 1), background_color='#282828', key="-DATE-"),
        sg.In(key='-SP_DATE-', size=(16, 1)),
        sg.CalendarButton('Datum ändern', size=(12, 1), key='-DATE_BT-', close_when_date_chosen=True, target='-SP_DATE-', format='%d.%m.%Y', no_titlebar=True, button_color='#640000', begin_at_sunday_plus=1,)
    ],
    [
        sg.Text('Event:', size=(8, 1), background_color='#282828'),
        sg.Combo(values=dropValues, default_value=current, size=(30, 1), key='-DROPDOWN-', readonly=True, enable_events=True, button_background_color='#640000'),
        sg.In(key='-SP_EVENT-', size=(32, 1)),
    ],
    [
        sg.Text('Bibelstelle:', size=(8, 1), background_color='#282828'),
        sg.In(key='-LESSON-', size=(32, 1)),
    ],
    [sg.Text('', background_color='#282828')],
    [sg.Text('Schriftgröße:', background_color='#282828')],
    [sg.Slider(range=(10, 90), default_value=90, resolution=1, enable_events=True, key='-SLIDER_ROW1-', orientation='h', size=(34,10), background_color='#282828', trough_color='#640000')],
    [sg.Slider(range=(10, 90), default_value=90, resolution=1, enable_events=True, key='-SLIDER_ROW2-', orientation='h', size=(34,10), background_color='#282828', trough_color='#640000')],
    [sg.Slider(range=(10, 90), default_value=90, resolution=1, enable_events=True, key='-SLIDER_ROW3-', orientation='h', size=(34,10), background_color='#282828', trough_color='#640000')],
    [sg.Text(background_color='#282828')],
    [sg.Button('Vorschau', key='-PREVIEW-', size=(38, 1),button_color='#640000')],
    [sg.Button('Erstellen', key='-CREATE-', size=(38, 1),button_color='#640000')],
]
preview_column = [
    [sg.Text('Vorschau:', background_color='#282828')],
    [sg.Image(source=imgSource, size=(640, 360),key='-IMAGE-', subsample=3)],
]
layout= [
    [
        sg.Column(layout=properties_column, background_color='#282828', vertical_alignment='top'),
        sg.VSeparator(),
        sg.Column(layout = preview_column, background_color='#282828'),
    ]
]

window = sg.Window(title='Thumbnail-Generator',layout=layout, background_color='#282828', finalize=True, icon='./icon/icon.ico')

#   Code after Startup to show next Sunday as img in cache
date = current.split(' (')
tg.modifyThumbnail([(date[1]).strip(')'), date[0].upper()], '', './cache/Thumbnail.png', False)
window['-IMAGE-'].update(imgSource, subsample=3)

window['-DATE-'].update(visible=False)
window['-SP_DATE-'].update(visible=False)
window['-DATE_BT-'].update(visible=False)
window['-DROPDOWN-'].update(visible=True)
window['-SP_EVENT-'].update(visible=False)

#   Main-Loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    elif event == '-CREATE-':
        if values['-SPECIAL-'] == True:
            tg.updateThumbnail(sunday=[spDate, spName], values=values, show=True)
        tg.updateThumbnail(values, True)

    elif event == '-PREVIEW-' or event == '-DROPDOWN-':
        if values['-SPECIAL-'] == True:
            spDate = values['-SP_DATE-']
            spName = values['-SP_EVENT-'].upper()
            tg.updateThumbnail(sunday=[spDate, spName], values=values, show=False)
        else:
            tg.updateThumbnail(values, False)
        window['-IMAGE-'].update(imgSource, subsample=3)

    elif event == '-SPECIAL-':
        if values['-SPECIAL-'] == True:
            window['-DATE-'].update(visible=True)
            window['-SP_DATE-'].update(visible=True)
            window['-DATE_BT-'].update(visible=True)
            window['-DROPDOWN-'].update(visible=False)
            window['-SP_EVENT-'].update(visible=True)
        else:
            window['-DATE-'].update(visible=False)
            window['-SP_DATE-'].update(visible=False)
            window['-DROPDOWN-'].update(visible=True)
            window['-SP_EVENT-'].update(visible=False)
            window['-DATE_BT-'].update(visible=False)

window.close()