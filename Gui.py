import PySimpleGUI as sg
from ImageSteganography import ImageSteganography
import sys

sg.ChangeLookAndFeel('GreenTan')

def insertion():
    layout = [
        [sg.Text('Steganography', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
        [sg.Frame(layout=[
        [sg.Checkbox('Encrypt', default=True)]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN)],
        [sg.InputOptionMenu(('LSB', 'BPCS'))],
        [sg.InputOptionMenu(('Sequential', 'Random'))],
        [sg.Text('Your Image', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText(''), sg.FileBrowse()],
        [sg.Text('Your File', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText(''), sg.FileBrowse()],
        [sg.Text('Your Key', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText('')],
        [sg.Submit(), sg.Cancel()]
    ]


    window = sg.Window('Steganography', layout, default_element_size=(40, 1), grab_anywhere=False)

    while True:
        event, values = window.read(0)
        if values[0] == True:
            window[5].update(disabled=False)
        else:
            window[5].update(disabled=True)

        if event == 'Cancel':
            break

        elif event == 'Submit':
            if values[1] == 'LSB':
                if values[2] == 'Sequential':
                    ImageSteganography.hide_message('11', values[3], values[4], values[5])
            if values[1] == 'BPCS':
                if values[2] == 'Sequential':
                    ImageSteganography.bpcs_encode(values[3], values[4], values[5])

    window.close()

def extraction():
    layout = [
            [sg.Text('Steganography', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
            [sg.InputOptionMenu('LSB', 'BPCS')],
            [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('Steganography', layout, default_element_size=(40, 1), grab_anywhere=False)
    event, values = window.read()
    window.close()

layout = [
    [sg.Text('Steganography', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.InputOptionMenu(('Penyisipan Pesan', 'Ekstraksi Pesan'))],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('Steganography', layout, default_element_size=(40, 1), grab_anywhere=False)

event, values = window.read()

if event == 'Submit':
    if values[0] == 'Penyisipan Pesan':
        insertion()
    elif values[0] == 'Ekstraksi Pesan':
        extraction()

window.close()
