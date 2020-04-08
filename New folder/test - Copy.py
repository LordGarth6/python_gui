import PySimpleGUI as sg

sg.theme('DarkBlue1')

times = [f'{h}:00' for h in range(6,12)]

col = [[sg.Text('col Row 1')],      
        [sg.Text('col Row 2'), sg.Input('col input 1')],      
        [sg.Text('col Row 3'), sg.Input('col input 2')]]
col2 = [[sg.Text('col Row 1')],      
        [sg.Text('col Row 2'), sg.Input('col input 1')],      
        [sg.Text('col Row 3'), sg.Input('col input 2')]] 
layout = [
            [sg.Text('My Window')],
            [sg.T('Desired date: '),sg.Input('', key='_DATE_'), sg.CalendarButton('Choose Date', target='_DATE_')],
            [sg.Button('Exit'),sg.Column(col),sg.Column(col2)]
         ]

window = sg.Window('Window Title', layout)

while True:             # Event Loop
    event, values = window.Read()
    print(event, values)
    if event in (None, 'Exit'):
        break

window.Close()
