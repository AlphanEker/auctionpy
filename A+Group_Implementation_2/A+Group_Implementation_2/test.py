import PySimpleGUI as sg

selection_button_text_data = [
    'Like a Rolling Stone',
    'Bob Dylan',
    'The Sound of Silence',
    'Simon & Garfunkel',
    'Respect',
    'Aretha Franklin',
    'A Day In The Life','The Beatles',
]

layout =[
    [sg.Button(selection_button_text_data[i], key=f'BTN{i}')] for i in range(4)
]
window = sg.Window('Window Title', layout)
event, values = window.read()
if event != sg.WINDOW_CLOSED:
    print(window[event].get_text())
window.close()