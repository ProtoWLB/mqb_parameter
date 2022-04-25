from BabyLIN.BLDriver import BL
from csv_handler import kseCsvHandler
from signals_handler import signalsHandler
from config import ramps, lin
import time

# handle CSV
csv_handler = kseCsvHandler(ramps.csv_file)
csv_handler.load_csv()

# initialize BabyLin
BabyLin = BL()
BabyLin.loadSdf(lin.sdf)
BabyLin.startSchedule(lin.schedule_num)
for signal in ramps.response_signals:
    BabyLin.dissignal(signal, 1)

#  signals
signals_handler = signalsHandler(BabyLin, csv_handler)
signals_handler.assign_signals()

# setup response to 0 - to be able to spot the difference if already correct response
for signal in ramps.response_signals:
    BabyLin.setsig(signal, 0)

# repeat send frames till respons is correct
for i in range(lin.max_macro_repeats):
    # send frame
    BabyLin.macro_exec(lin.ramps_macro)
    time.sleep(1)  # enough to run macro and write response
    # read response
    response = []
    result = False
    for signal in ramps.response_signals:
        response.append(BabyLin.readSignal(signal))
    if response == ramps.correct_response:  # if response OK - break
        print('\nSUCCEEDED (loop: {})\n'.format(i+1))
        result = True
        break
    else:  # if wrong response repeat
        # print('loop: {} - NOK'.format(i))
        print('ramp update in progress...')

if not result:
    print('\nFAILED\n')

# close BabyLin
BabyLin.closeAll()
