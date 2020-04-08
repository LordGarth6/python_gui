import PySimpleGUI as sg

sg.ChangeLookAndFeel('GreenTan')

column1 = [[sg.Text('Column 1', background_color='#d3dfda', justification='center', size=(10, 1))],      
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],      
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],      
           [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]      
layout = [      
    [sg.Text('All graphic widgets in one window!', size=(30, 1), font=("Helvetica", 25))],      
    [sg.Text('Here is some text.... and a place to enter text')],      
    [sg.InputText('This is my text')],      
    [sg.Checkbox('My first checkbox!'), sg.Checkbox('My second checkbox!', default=True)],      
    [sg.Radio('My first Radio!     ', "RADIO1", default=True), sg.Radio('My second Radio!', "RADIO1")],      
    [sg.Multiline(default_text='This is the default Text should you decide not to type anything', size=(35, 3)),      
     sg.Multiline(default_text='A second multi-line', size=(35, 3))],      
    [sg.InputCombo(('Combobox 1', 'Combobox 2'), size=(20, 3)),      
     sg.Slider(range=(1, 100), orientation='h', size=(34, 20), default_value=85)],      
    [sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(30, 3)),      
     sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=25),      
     sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=75),      
     sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=10),      
     sg.Column(column1, background_color='#d3dfda')],      
    [sg.Text('_'  * 80)],      
    [sg.Text('Choose A Folder', size=(35, 1))],      
    [sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),      
     sg.InputText('Default Folder'), sg.FolderBrowse()],      
    [sg.Submit(), sg.Cancel()]      
]

window = sg.Window('Everything bagel', default_element_size=(40, 1)).Layout(layout)
button, values = window.Read()
sg.Popup(button, values)


import PySimpleGUI as sg
import sys
import CSVSplitterFnFiles

layout = [[sg.Text('CSV Splitter')],
          [sg.Text('Choose your CSV file:')],
          [sg.Input(enable_events=True,key='_INPUT_FILEPATH_'), sg.FileBrowse()],
          [sg.Button('RowCount',key='_BTN_ROWCOUNT_'), sg.Input('',key='_INPUT_ROWCOUNT_',size=(5,5), disabled=True)],
          [sg.Check('Include Header in all Output Files',key='_CHK_INCHEADER_',default=True)],
          #[sg.Check()]
          [sg.Radio('Normal Split','SplitType',enable_events=True, key='_RB1_NS_',default=True)],
          [sg.Text('No. of Records per File: ', size=(20,1),key='_TXT_NORMALSPLIT_',visible=True),
           sg.Input('',size=(7,7),key='_INPUT_NORMALSPLIT_',visible=True,disabled=False)],
          [sg.Radio('Custom Split','SplitType',enable_events=True, key='_RB2_CS_')],
          [sg.Text('Choose output file(s) destination folder :')],
          [sg.Input(key='_INPUT_CUSTSPLIT_OUTFOLDER_',disabled=True), sg.FolderBrowse(key='_BTN_CUSTSPLIT_OUTFOLDER_',disabled=True)],
          [sg.Text('Custom Split items',key='_TXT_CUSTOMSPLIT_',visible=False)],
          [sg.Input(key='_INPUT_CUSTOMSPLIT_',visible=True,disabled=True)],
          [sg.Text('Error : ')],
          [sg.Input('',key='_INPUT_ERRORFIELD_',disabled=True)],
          [sg.Text('Status: '), sg.Input(disabled=True,key='_INPUT_PROGRESS_')],
          [sg.Button('Submit',key='_BTN_SUBMIT_',disabled=True), sg.Button('Clear',key='_BTN_CLEAR_'),
           sg.Button('Exit')]
          ]

window = sg.Window('CSV Splitter - VN',layout).Finalize()

while True:             # Event Loop
    event, values = window.Read()
    if event is None or event == 'Exit':
        break
    elif event == '_INPUT_FILEPATH_':
        print(values)
        fileName, extn = CSVSplitterFnFiles.fileCheck(values)
        window.FindElement('_INPUT_ERRORFIELD_').Update('')
        window.FindElement('_INPUT_ROWCOUNT_').Update('')
        window.FindElement('_INPUT_NORMALSPLIT_').Update(disabled=False)
        window.FindElement('_BTN_SUBMIT_').Update(disabled=False)
        window.FindElement('_BTN_ROWCOUNT_').Update(disabled=False)
        if extn not in ['CSV','csv']:
            window.FindElement('_INPUT_ERRORFIELD_').Update('Invalid File - Not a CSV')
            window.FindElement('_BTN_SUBMIT_').Update(disabled=True)
            window.FindElement('_BTN_ROWCOUNT_').Update(disabled=True)
            window.FindElement('_INPUT_NORMALSPLIT_').Update(disabled=True)
    elif event == '_BTN_ROWCOUNT_':
        rowCount = CSVSplitterFnFiles.rowCount(values)
        window.FindElement('_INPUT_ROWCOUNT_').Update(rowCount)
        
    elif event == '_RB1_NS_':
        window.FindElement('_INPUT_NORMALSPLIT_').Update(disabled=False)
        window.FindElement('_INPUT_CUSTOMSPLIT_').Update(disabled=True)
        window.FindElement('_INPUT_CUSTSPLIT_OUTFOLDER_').Update(disabled=True)
        window.FindElement('_BTN_CUSTSPLIT_OUTFOLDER_').Update(disabled=True)
        
    elif event == '_RB2_CS_':
        window.FindElement('_INPUT_NORMALSPLIT_').Update('')
        window.FindElement('_INPUT_NORMALSPLIT_').Update(disabled=True)
        window.FindElement('_INPUT_CUSTOMSPLIT_').Update(disabled=False)
        window.FindElement('_INPUT_CUSTSPLIT_OUTFOLDER_').Update(disabled=False)
        window.FindElement('_BTN_CUSTSPLIT_OUTFOLDER_').Update(disabled=False)
        
    elif event == '_BTN_SUBMIT_':
        window.FindElement('_BTN_SUBMIT_').Update(disabled=True)
        window.FindElement('_INPUT_PROGRESS_').Update('Please Wait, Splitting is In-progress....')
        status = CSVSplitterFnFiles.fileSplit(values)
        print(event,values)
        if status == 'Completed':
            window.FindElement('_INPUT_PROGRESS_').Update('Splitting Completed!!')
            sg.Popup("Done", "CSV Splitting completed successfully.")
            break
        
    elif event == '_BTN_CLEAR_':
        #window['_INPUT_ROWCOUNT_']('')
        print(event,values)
        window.FindElement('_INPUT_ROWCOUNT_').Update('')
        window.FindElement('_INPUT_FILEPATH_').Update('')
        window.FindElement('_INPUT_NORMALSPLIT_').Update('')
        window.FindElement('_INPUT_ERRORFIELD_').Update('')
        window.FindElement('_INPUT_CUSTSPLIT_OUTFOLDER_').Update('')
        window.FindElement('_INPUT_PROGRESS_').Update('')
        window.FindElement('_CHK_INCHEADER_').Update(True)
        

#print(event,values)
window.Close()
