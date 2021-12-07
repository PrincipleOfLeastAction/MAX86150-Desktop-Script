from scipy.signal import stft
import matplotlib.pyplot as plt
import numpy as np
from load_signal import load_ppg_data

RTime, rSignal, IRTime, irSignal, timeToLog, samplingFreq = \
       load_ppg_data()

f, t, Zxx = stft(rSignal, samplingFreq, nperseg=37, 
                 noverlap=18, nfft=256)

N = len(f) //6

plt.pcolormesh(t, f[:N], np.abs(Zxx)[:N], shading="gouraud")
plt.title("STFT magnitude")
plt.ylabel("Frequency [Hz]")
plt.xlabel("Time [s]")
plt.show()
