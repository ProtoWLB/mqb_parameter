class ramps:
    csv_file = 'KSE_Silent_Algo_Control_Panel_v1.csv'

    # set signals numbers here
    open_sigs = (135, 184)  # range - first and last (including last)
    close_sigs = (185, 234)  # range - first and last (including last)
    hold_signals = [134]
    response_signals = [235, 236, 237]
    correct_response = [110, 0, 12]  # signal values in decimal

    # do not set signals numbers here
    opening_signals = [i for i in range(open_sigs[0], open_sigs[1]+1)]
    closing_signals = [i for i in range(close_sigs[0], close_sigs[1]+1)]

class lin:
    sdf = '.\BabyLin\kse_param.sdf'
    schedule_num = 2  # diagnostic session
    ramps_macro = 0  # macro sending ramps definition with diagnostics
    max_macro_repeats = 5