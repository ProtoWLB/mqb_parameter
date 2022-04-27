from config import frame_config

class signalsHandler():
    def __init__(self, BabyLin, frame):
        self.BabyLin = BabyLin
        self.frame = frame

    def assign_signals(self):
        """
        set frmaes signals
        :return:
        """
        self.BabyLin.setsig(frame_config.request_len, self.frame.payload_len)
        self.set_multiple_signals(frame_config.set_signals, self.frame.data)


    def set_multiple_signals(self, signals, ramp):
        """
        set signals for given values
        :param signals: signals numbers
        :param ramp: signals values
        :return: None
        """
        for sig, value in zip(signals, ramp):
            self.BabyLin.setsig(sig, value)

