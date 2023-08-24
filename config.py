
class frames_config:
    read_sid = 0x22
    read_len = 0x03


class frame_config:
    csv_file = 'KSE_Silent_Algo_Control_Panel_v1.csv'

    # set signals numbers here
    set_range = (277, 376)  # range - first and last (including last)
    read_range = (378, 458)  # range - first and last (including last)
    request_len = 276

    # do not set signals numbers here
    set_signals = [i for i in range(set_range[0], set_range[1]+1)]
    read_signals = [i for i in range(read_range[0], read_range[1]+1)]

class lin:
    sdf = '.\BabyLin\mqb_parameter.sdf'
    schedule_num = 2  # diagnostic session
    parameter_macro = 0  # macro sending ramps definition with diagnostics
    extended_session_macro = 1
    max_macro_repeats = 5
    nad_signal = 273