import PySimpleGUI as sg

def gui(title, message):
    window = sg.Window(title=title + '!',layout=[[sg.Text(text=message)]], background_color='#282828', finalize=True, icon='./icon/icon.ico',)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()
def error(text):
    gui('Error', text)
def info(text):
    gui('Information', text)