from BabyLIN.BLDriver import BL
from frame import SetFrame, ReadFrame

from signals_handler import signalsHandler
from config import frame_config, lin
import time

import os

# get parametrization string
param_string = input('Paste parametrization string\n')

# read or write
action = input('pres S to set or R - to read and confirm with enter\n')

if action.lower() == 's':
    print('save frame')
    # set parameters
    frame_to_send = SetFrame(param_string)
else:
    print('read frame')
    # read parameters
    frame_to_send = ReadFrame(param_string)

print('LEN:{}, SID: {}, DATA: {}'.format(frame_to_send.payload_len, frame_to_send.data[0], frame_to_send.data[1:]))

# initialize BabyLin
BabyLin = BL()

BabyLin.loadSdf(lin.sdf)
BabyLin.startSchedule(lin.schedule_num)  # diagnostic session
BabyLin.macro_exec(lin.extended_session_macro)  # exetended session frame - periodic send

#  signals
signals_handler = signalsHandler(BabyLin, frame_to_send)
signals_handler.assign_signals()

# setup response to 0 - to be able to spot the difference if already correct response
for signal in frame_config.read_range:
    BabyLin.setsig(signal, 0)
    time.sleep(0.01)

# dissignal read signals
for signal in frame_config.read_signals:
    BabyLin.dissignal(signal, 1)
    time.sleep(0.0)

# send frame
BabyLin.macro_exec(lin.parameter_macro)
time.sleep(0.5)

response = []
for signal in frame_config.read_signals:
    response.append(BabyLin.readSignal(signal))
    time.sleep(0.01)


hex_response = ''.join([hex(x)[2:].zfill(2) for x in response])
print(hex_response)  # dec to hex



with open("last_resp.txt", 'w', encoding='utf-8') as f:
    f.write('\n'+str(hex_response))

# close BabyLin
BabyLin.closeAll()

input('Press Enter to close')
