from BabyLIN.BLDriver import BL
from frame import SetFrame, ReadFrame
import pyperclip
from signals_handler import signalsHandler
from config import frame_config, lin
import time

import os


# initialize BabyLin
BabyLin = BL()

BabyLin.loadSdf(lin.sdf)
BabyLin.startSchedule(lin.schedule_num)  # diagnostic session
BabyLin.macro_exec(lin.extended_session_macro)  # exetended session frame - periodic send


# dissignal read signals
for signal in frame_config.read_signals:
    BabyLin.dissignal(signal, 1)
    time.sleep(0.01)

last_set_len = 0
while True:

    # read or write
    action = input('press:\n - S to set\n - R - to read \n - Q - to quit \nThan confirm with enter\n')
    if action.lower() == 'q':
        break

    # get parametrization string
    param_string = input('Paste parametrization string\n')


    if action.lower() == 's':
        print('save frame')
        # set parameters
        frame_to_send = SetFrame(param_string)
        last_set_len = frame_to_send.payload_len

    else:
        print('read frame')
        # read parameters
        frame_to_send = ReadFrame(param_string)
    
    # print('LEN:{}, SID: {}, DATA: {}'.format(frame_to_send.payload_len, frame_to_send.data[0], frame_to_send.data[1:]))
    
    
    #  signals
    signals_handler = signalsHandler(BabyLin, frame_to_send)
    signals_handler.assign_signals()
    
    # setup response to 0 - to be able to spot the difference if already correct response
    for signal in frame_config.read_signals:
        BabyLin.setsig(signal, 0)
        time.sleep(0.01)
    
    # send frame
    BabyLin.macro_exec(lin.parameter_macro)
    time.sleep(0.5)
    
    response = []
    short_resp = []
    for signal in frame_config.read_signals:
        response.append(BabyLin.readSignal(signal))
        time.sleep(0.01)
    
    # if read skip first 3 bytes
    if not action.lower() == 's':
        response = response[3:]
        short_resp = response[0:last_set_len-3]
    hex_response = ''.join([hex(x)[2:].zfill(2) for x in response])
    short_hex_response = ''.join([hex(x)[2:].zfill(2) for x in short_resp])
    print(f'\nDone. Response:\n\n{hex_response}\n')
    
    with open("last_resp.txt", 'w', encoding='utf-8') as f:
        f.write('\n'+str(hex_response))
    
    # if read copy answer to clipboard
    if not action.lower() == 's':
        if last_set_len:
            pyperclip.copy(short_hex_response)
        else:
            pyperclip.copy(hex_response)


# close BabyLin
BabyLin.closeAll()
