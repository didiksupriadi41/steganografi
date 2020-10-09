import PySimpleGUI as sg
from ImageSteganography import ImageSteganography
import videoSteganography
import sys

sg.ChangeLookAndFeel('GreenTan')

def insertion():
    layout = [
        [sg.Text('Steganography Insertion', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
        [sg.Frame(layout=[
        [sg.Checkbox('Encrypt', default=False)]], title='Options0',title_color='red', relief=sg.RELIEF_SUNKEN)],
        [sg.InputOptionMenu(('LSB', 'BPCS'), key="SteganographyMethod")],
        [sg.Frame(layout=[
        [sg.Checkbox('PixelSequential', default=False, key="PixelSequential")]], title='Options1',title_color='red', relief=sg.RELIEF_SUNKEN)],
        [sg.Text('Your Image', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText(key="image"), sg.FileBrowse()],
        [sg.Text('Your Message File', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText(key="message"), sg.FileBrowse()],
        [sg.Text('Your Key', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText(key="key")],
        [sg.Frame(layout=[
        [sg.Checkbox('VideoSteganography', default=False, key="VideoSteganography")]], title='Options2',title_color='red', relief=sg.RELIEF_SUNKEN)],
        [sg.Frame(layout=[
        [sg.Checkbox('FrameSequential', default=False, key="FrameSequential")]], title='Options3',title_color='red', relief=sg.RELIEF_SUNKEN)],
        [sg.Text('Your Video', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText(key="video"), sg.FileBrowse()],

        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('Steganography', layout, default_element_size=(40, 1), grab_anywhere=False)

    while True:
        event, values = window.read(0)
        print(values)
        # if values[0] == True:
        #     window[4].update(disabled=False)
        # else:
        #     window[4].update(disabled=True)

        if event == 'Cancel':
            break

        elif event == 'Submit':
            if values['VideoSteganography']:
                videoSteganography.encode(input_video=values['video'], frame_dir="temp", message=values['message'], key="didik", frameSequential=values['FrameSequential'], pixelSequential=values['PixelSequential'], encrypted=True, from_file=True, output_video="stegomovie.mov")
            else:
                if values["SteganographyMethod"] == 'LSB':
                    ImageSteganography.hide_message('11', values['image'], values['message'], values['key'], pixelSequential=values['PixelSequential'], from_file=True, encrypt=values[0])
                    # if values[2] == 'Sequential':
                    #     ImageSteganography.hide_message('11', values[3], values[4], values[5], pixelSequential=True, from_file=True, encrypt=values[0])
                    # else:
                    #     ImageSteganography.hide_message('11', values[3], values[4], values[5], pixelSequential=False, from_file=True, encrypt=values[0])
                if values["SteganographyMethod"] == 'BPCS':
                    if values['PixelSequential']:
                        ImageSteganography.bpcs_encode(values['image'], values['message'], values['key'])

    window.close()

def extraction():
    layout = [
            [sg.Text('Steganography Extraction', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
            #[sg.InputOptionMenu(('LSB', 'BPCS'))],
            [sg.Frame(layout=[
            [sg.Checkbox('VideoSteganography', default=False, key="VideoSteganography")]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN)],
            [sg.Text('Your Stego Video', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText(key="video"), sg.FileBrowse()],
            [sg.Text('Your Key', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText(key="key")],
            [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('Steganography', layout, default_element_size=(40, 1), grab_anywhere=False)
    event, values = window.read()

    while True:
        event, values = window.read(0)
        print(values)
        # if values[0] == True:
        #     window[4].update(disabled=False)
        # else:
        #     window[4].update(disabled=True)

        if event == 'Cancel':
            break

        elif event == 'Submit':
            if values['VideoSteganography']:
                videoSteganography.decode(frame_dir="temp2", input_video=values['video'], key=values['key'],  output_message="decodedMessage.txt")
    window.close()

def psnr():
    layout = [
            [sg.Text('Steganography PSNR', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
            #[sg.InputOptionMenu(('LSB', 'BPCS'))],
            [sg.Frame(layout=[
            [sg.Checkbox('VideoSteganography', default=False, key="VideoSteganography")]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN)],
            [sg.Text('Your Original File', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText(key="input_file"), sg.FileBrowse()],
            [sg.Text('Your Stego File', size=(15, 1), auto_size_text=False, justification='right'),
            sg.InputText(key="output_file"), sg.FileBrowse()],
            [sg.Text('PSNR:'), sg.Text(size=(30,1), key='PSNR')],
            [sg.Submit(), sg.Cancel()]
    ]
    window = sg.Window('Steganography', layout, default_element_size=(40, 1), grab_anywhere=False)
    event, values = window.read()

    while True:
        event, values = window.read(0)
        print(values)
        # if values[0] == True:
        #     window[4].update(disabled=False)
        # else:
        #     window[4].update(disabled=True)

        if event == 'Cancel':
            break

        elif event == 'Submit':
            if values['VideoSteganography']:
                psnr = videoSteganography.video_psnr(input_video=values['input_file'],input_dir="temp",output_video=values['output_file'],output_dir="temp2", output_psnr_txt="psnr.txt")
                window['PSNR'].update(str(psnr))
    window.close()

layout = [
    [sg.Text('Steganography', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    [sg.InputOptionMenu(('Penyisipan Pesan', 'Ekstraksi Pesan', 'PSNR'))],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('Steganography', layout, default_element_size=(40, 1), grab_anywhere=False)

event, values = window.read()

if event == 'Submit':
    if values[0] == 'Penyisipan Pesan':
        insertion()
    elif values[0] == 'Ekstraksi Pesan':
        extraction()
    elif values[0] == 'PSNR':
        psnr()

window.close()
