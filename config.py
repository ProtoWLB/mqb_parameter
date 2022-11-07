from ramps import frame_data, opening, closing


class frames_config:
    read_sid = 0x22
    read_len = 0x03


class frame_config:
    csv_file = 'KSE_Silent_Algo_Control_Panel_v1.csv'

    # set signals numbers here
    set_range = (277, 381)  # range - first and last (including last)
    read_range = (383, 463)  # range - first and last (including last)
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


class vw_lin_signals:
    massage_intens = 66
    massage_prog = 68
    massage_status = 72
    massage_read_status = 181



# # set frames
# filepath = 'stringi_silentalgo.txt'
# file = open(filepath, 'r')
# all_sets = file.readlines()
# file.close()
# for index, line in enumerate(all_sets):
#    all_sets[index] = line[:-1]  # append line without \n sign
#

all_sets = [frame_data.frameData(x).get_opening_frame() for x in opening.ramps]

print(all_sets)
# read frames
filepath = 'READ_silentalgo.txt'
file = open(filepath, 'r')
all_reads = file.readlines()
file.close()
for index, line in enumerate(all_reads):
   all_reads[index] = line[:-1]  # append line without \n sign

#
# print(all_reads)

