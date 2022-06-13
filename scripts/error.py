import PySimpleGUI as sg
import thumbGen as tg


def message(text):
    window = sg.Window(title='Error!',layout=[[sg.Text(text=text)]], background_color='#282828', finalize=True, icon='./icon/icon.ico', size=(30, 10))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

    window.close()