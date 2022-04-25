from config import ramps

class signalsHandler():
    def __init__(self, BabyLin, ramps_values):
        self.BabyLin = BabyLin
        self.ramps_values = ramps_values

    def assign_signals(self):
        """
        set signals for hold and  open and close ramps
        :return:
        """
        self.BabyLin.setsig(ramps.hold_signals[0], self.ramps_values.hold[0])  # one signal
        self.set_ramp_signals(ramps.opening_signals, self.ramps_values.opening)
        self.set_ramp_signals(ramps.closing_signals, self.ramps_values.closing)


    def set_ramp_signals(self, signals, ramp):
        """
        set signals for given values
        :param signals: signals numbers
        :param ramp: signals values
        :return: None
        """
        for sig, value in zip(signals, ramp):
            self.BabyLin.setsig(sig, value)
            # todo check if should be delay between or some verification
