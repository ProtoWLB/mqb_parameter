class open_conf:
    service_len = '67'
    select_option = '2e'
    did_num = 'fd03'


class close_conf:
    service_len = '67'
    select_option = '2e'
    did_num = 'fd04'


class frameData:

    def __init__(self, ramp):
        self.ramp = [hex(x)[2:] for x in ramp]

    def build_data(self, conf):

        return '{}{}{}{}'.format(
            conf.service_len,
            conf.select_option,
            conf.did_num,
            ''.join(self.ramp)
        )


    def get_opening_frame(self):
        frame_data = self.build_data(open_conf)
        return frame_data

    def get_closing_frame(self):
        frame_data = self.build_data(close_conf)
        return frame_data

# # CHECK
# ramp03 = [40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
#
# fr = frameData(ramp03)
#
# print(fr.get_opening_frame())
# print(fr.get_closing_frame())