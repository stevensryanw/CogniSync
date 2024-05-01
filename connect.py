from pyOpenBCI import OpenBCICyton
from pylsl import StreamInfo, StreamOutlet
import numpy as np


def record(self):
        SCALE_FACTOR_EEG = (4500000)/24/(2**23-1) #uV/count
        SCALE_FACTOR_AUX = 0.002 / (2**4)
        print("Creating LSL stream for EEG. \nName: OpenBCIEEG\nID: OpenBCItestEEG\n")
        info_eeg = StreamInfo('OpenBCIEEG', 'EEG', 8, 250, 'float32', 'OpenBCItestEEG')
        print("Creating LSL stream for AUX. \nName: OpenBCIAUX\nID: OpenBCItestEEG\n")
        info_aux = StreamInfo('OpenBCIAUX', 'AUX', 3, 250, 'float32', 'OpenBCItestAUX')
        outlet_eeg = StreamOutlet(info_eeg)
        outlet_aux = StreamOutlet(info_aux)
        file_out = open('newest_rename.csv', 'a')
        file_out.truncate(0)
        file_out.write('ch1,ch2,ch3,ch4,ch5,ch6,ch7,ch8,aux1,aux2,aux3,label\n')
        def lsl_streamers(sample):
            file_in = open('tempVal.txt', 'r')
            input = file_in.readline()
            lbl = ''
            if input != '':
                lbl = input
            else:
                lbl = 'norm'
            outlet_eeg.push_sample(np.array(sample.channels_data)*SCALE_FACTOR_EEG)
            outlet_aux.push_sample(np.array(sample.aux_data)*SCALE_FACTOR_AUX)
            #print(sample.channels_data*SCALE_FACTOR_EEG, sample.aux_data*SCALE_FACTOR_AUX, lbl)
            for datai in sample.channels_data:
                file_out.write(str(datai*SCALE_FACTOR_EEG) + ',')
            for dataj in sample.aux_data:
                file_out.write(str(dataj*SCALE_FACTOR_AUX) + ',')
            file_out.write(str(lbl) + '\n')
            file_in.close()
        board = OpenBCICyton()
        board.start_stream(lsl_streamers)
        file_out.close()