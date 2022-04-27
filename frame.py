import textwrap
from config import frames_config


class Frame:
    def __init__(self):
        self.payload_len = 0
        self.data = []

    def string_to_frame(self, data):
        payload = textwrap.wrap(data, 2)  # divide string to bytes
        self.data = [int('0x{}'.format(i), 0) for i in payload]  # string bytes to hex string -> ints

class SetFrame(Frame):
    def __init__(self, data: str):
        super().__init__()
        self.string_to_frame(data)  # parse string to list of ints
        self.payload_len = self.data[0]
        self.data = self.data[1:]

class ReadFrame(Frame):
    def __init__(self, data: str):
        super().__init__()
        self.payload_len = frames_config.read_len
        self.string_to_frame(data)  # parse string to list of ints
        self.data.insert(0, frames_config.read_sid)




