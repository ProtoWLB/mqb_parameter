from BabyLIN.BLDriver import BL
from frame import SetFrame, ReadFrame
import pyperclip
from signals_handler import signalsHandler
from config import frame_config, lin
import time
from barka import barka_lyrics
import json

import os

global nad

# initialize BabyLin
BabyLin = BL()

BabyLin.loadSdf(lin.sdf)
BabyLin.startSchedule(lin.schedule_num)  # diagnostic session
BabyLin.macro_exec(lin.extended_session_macro)  # exetended session frame - periodic send
nad = 64

with open('nads.json') as f:
    data = json.load(f)
versions = {int(k):v for k,v in data.items()}
versions[2137] =  'Barka'
print(versions)
# versions = {
#     64: 'MQB',
#     65: 'RSA',
#     87: 'NIO',
#     119: 'MissX-MVB',
#     118: 'MissX-IVB',
#     2137: 'Barka'
#
# }
print_versions = [f'{v}:{k}' for k,v in versions.items() if k != 2137]


def get_version_name(nad):
    try:
        result = versions[nad]
        if result == 'Barka':
            nad = 64
            print(barka_lyrics)
            return versions[nad]
        print('-------------------')
        print(result)
        return result
    except KeyError:
        return(f'unknown NAD {nad}')


# dissignal read signals
for signal in frame_config.read_signals:
    BabyLin.dissignal(signal, 1)
    time.sleep(0.01)

last_set_len = 0
while True:

    # read or write
    skip = False
    action = input(f'Selected version: {get_version_name(nad)}.\nPress:\n - S to set\n - R - to read\n - N - to set NAD  \n - Q - to quit \nThan confirm with enter\n')
    if action.lower() == 'q':
        break

    elif action.lower() == 'n':
        # get parametrization string
        print(print_versions)
        nad = int(input('Paste NAD value\n'))
        print(f'Selected version: {get_version_name(nad)}')
        BabyLin.setsig(lin.nad_signal, nad)
        skip = True

    elif action.lower() == 's':
        # get parametrization string
        param_string = input('Paste parametrization string\n')
        print('save frame')
        # set parameters
        frame_to_send = SetFrame(param_string)
        last_set_len = frame_to_send.payload_len

    elif action.lower() == 'r':
        # get parametrization string
        param_string = input('Paste read string\n')
        print('read frame')
        # read parameters
        frame_to_send = ReadFrame(param_string)

    else:
        print('Wrong selection')
    
    # print('LEN:{}, SID: {}, DATA: {}'.format(frame_to_send.payload_len, frame_to_send.data[0], frame_to_send.data[1:]))
    
    if not skip:
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


        with open("last_resp.txt", 'w', encoding='utf-8') as f:
            f.write('\n'+str(hex_response))

        # if read copy answer to clipboard
        if action.lower() == 'r':
            if last_set_len:
                pyperclip.copy(short_hex_response)
                print(f'\nDone. Response:\n\n{short_hex_response}\n')
            else:
                pyperclip.copy(hex_response)
                print(f'\nDone. Response:\n\n{hex_response}\n')
        else:
            print(f'\nDone. Response:\n\n{hex_response}\n')


# close BabyLin
BabyLin.closeAll()
