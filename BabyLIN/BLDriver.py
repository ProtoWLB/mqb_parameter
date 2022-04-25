from __future__ import unicode_literals
import os, sys, argparse, six, time

try:
    from BabyLIN import BabyLIN_library
except ImportError as e:
    six.print_(six.text_type(e))


class BL:
    def __init__(self):
        # create the BabyLIN class contained in BabyLIN_DLL.py
        BabyLIN = BabyLIN_library.create_BabyLIN()

        # inject BabyLIN names into local namespace, so you can, e.g. write
        # BLC_getVersion instead of BabyLIN.BLC_getVersion
        for k, v in BabyLIN.__dict__['_libNames'].items():
            globals()[k] = getattr(BabyLIN, k)



        ports = BLC_getBabyLinPorts(10)
        if not ports:
            six.print_("No BabyLIN found")
            sys.exit(-1)

            # open the device(s)
        conHandle = (BLC_openPort(port) for port in ports)

        # get the device's number of channels
        channelCount = ((BLC_getChannelCount(h), h) for h in conHandle)

        # among these, look for the first LIN channel:
        channelRange = ((range(chNr), h) for chNr, h in channelCount)

        # first, get the corresponding channel handles
        chHandle = ((BLC_getChannelHandle(h, channelIndex), h)
                    for r, h in channelRange for channelIndex in r)

        # for each channel (handle), get the channel info
        chInfo = ((BLC_getChannelInfo(ch), h, ch) for ch, h in chHandle)

        # using the channel info, filter the LIN channels
        # using 'info.type == 0'
        conH_chH = ((h, ch) for info, h, ch in chInfo if info.type == 0)

        for conHandle, chHandle in conH_chH:
            conHandle = conHandle
            chHandle = chHandle

        self.conHandle = conHandle
        self.chHandle = chHandle



    def loadSdf(self, sdfName):
        BLC_loadSDF(self.conHandle, sdfName, 1)

    def startSchedule(self, schedNum):
        commandString = 'start schedule ' + str(schedNum) + ';'
        BLC_sendCommand(self.chHandle, commandString)
        print(commandString)

    def setsig(self, sigNum, Value):
        commandString = 'setsig ' + str(sigNum) + ' ' + str(Value) + ';'
        BLC_sendCommand(self.chHandle, commandString)
        print(commandString)

    def stopSchedule(self):
        '''
        sleep needed becouse if schedule will be stopped wright after other command - this last command will be ignored
        '''
        time.sleep(0.1)
        BLC_sendCommand(self.chHandle, "stop;")

    def dissignal(self, sigNum, Value):
        commandString = 'dissignal ' + str(sigNum) + ' ' + str(Value) + ';'
        BLC_sendCommand(self.chHandle, commandString)

    def readSignal(self, sigNum):
        signalValue = BLC_getSignalValue(self.chHandle, sigNum)
        return signalValue

    def send_command(self, command):
        BLC_sendCommand(self.chHandle, command)

    def macro_exec(self, macro_number):

        commandString = 'macro_exec {};'.format(macro_number)
        BLC_sendCommand(self.chHandle, commandString)



    def closeAll(self):
        BLC_closeAll()

    def reset(self):
        self.closeAll()
        time.sleep(0.1)
        self.__init__()


