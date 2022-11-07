from BabyLIN.BLDriver import BL
from frame import SetFrame, ReadFrame
import pyperclip
from signals_handler import signalsHandler
from config import frame_config, lin, all_sets, all_reads, vw_lin_signals
import time

# Functions
def send_parameter_frame(action, parameter_string):
    """
    build frame
    send frame
    read response
    return: response
    """
    if action.lower() == 's':
        # set parameters
        frame_to_send = SetFrame(parameter_string)
    else:
        # read parameters
        frame_to_send = ReadFrame(parameter_string)

    #  signals
    signals_handler = signalsHandler(BabyLin, frame_to_send)
    signals_handler.assign_signals()

    # setup response to 0 - to be able to spot the difference if already correct response
    for signal in frame_config.read_range:
        BabyLin.setsig(signal, 0)
        time.sleep(0.01)

    # send frame
    BabyLin.macro_exec(lin.parameter_macro)
    time.sleep(0.5)

    response = []
    for signal in frame_config.read_signals:
        response.append(BabyLin.readSignal(signal))
        time.sleep(0.01)

    # if read skip first 3 bytes
    if not action.lower() == 's':
        response = response[3:]

    return response

def setup_parametrization():
    BabyLin.startSchedule(lin.schedule_num)  # diagnostic session

def run_massage():
    BabyLin.startSchedule(0)
    time.sleep(0.1)

    # global setup
    BabyLin.setsig(63,2)  # ustawia domyślnie czas trwania na 10 minut
    BabyLin.setsig(252, 1)  # ustawia bit zapłonu na 1
    BabyLin.setsig(77, 1)
    time.sleep(0.1)
    BabyLin.setsig(62, 1)
    time.sleep(1)
    BabyLin.setsig(62, 0)
    time.sleep(0.5)

    # massage setup
    BabyLin.setsig(vw_lin_signals.massage_prog, 5)
    BabyLin.setsig(vw_lin_signals.massage_intens, 3)
    BabyLin.setsig(vw_lin_signals.massage_status, 1)
    print('massage started')
    time.sleep(25)
    BabyLin.setsig(vw_lin_signals.massage_status, 0)
    print('massage stopped')





# initialize BabyLin
BabyLin = BL()

BabyLin.loadSdf(lin.sdf)
setup_parametrization()
print('prefill wait start')
time.sleep(25)  # wait for prefil function
print('prefill wait stop')
BabyLin.macro_exec(lin.extended_session_macro)  # exetended session frame - periodic send
# dissignal read signals
for signal in frame_config.read_signals:
    BabyLin.dissignal(signal, 1)
    # time.sleep(0.0)


for one_set, one_read in zip(all_sets, all_reads):

    set_response = send_parameter_frame('s', one_set)
    time.sleep(0.5)
    num_of_bytes = int(len(one_read)/2)  # get number of bytes in response
    # analyze response
    read_response = send_parameter_frame ('r', '0119')[:num_of_bytes]
    read_response = [hex(int(x)) for x in read_response]
    read_response = [x[2:].zfill(2) for x in read_response]
    read_response = ''.join(read_response)
    print(read_response)
    # check if ok
    parametr_succced = read_response.lower() == one_read.lower()
    print('Parametrisation for request: {} {}'.format(one_read, 'succedded' if parametr_succced else 'failed'))
    if not parametr_succced:
        break
    # run massage
    time.sleep(1)
    run_massage()
    time.sleep(0.1)
    # run diagnostic
    setup_parametrization()
    time.sleep(0.1)

    # todo ??if not run parametrization again




# close BabyLin
BabyLin.closeAll()

input('Press enter to close')