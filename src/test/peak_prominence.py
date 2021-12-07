from scipy.signal import argrelmax, peak_prominences, \
    find_peaks
import matplotlib.pyplot as plt
import numpy as np
from load_signal import load_ppg_data

RTime, rSignal, IRTime, irSignal, timeToLog, samplingFreq = \
       load_ppg_data()

width = np.linspace(0, timeToLog, num=117)

peak_indicies_argrel = argrelmax(rSignal, order=37)[0]
peak_indicies, _ = find_peaks(rSignal, prominence=1000)

print(f"Heart Rate = {len(peak_indicies)/timeToLog * 60}")

prominences, L, R = peak_prominences(rSignal, peak_indicies_argrel)
print(prominences)

plt.plot(RTime, rSignal, 'r')
plt.plot(RTime[peak_indicies], rSignal[peak_indicies], "xb")
plt.show()

