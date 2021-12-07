from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np

# File names
filename = ""
fileTime = "2020-12-11--14-11-56"

dirName = ""
rawDataDir = f"../../loggingFiles/{dirName}{fileTime}{filename}_logs/"
RFileName = f"Rlog--{fileTime}{filename}.csv"
IRFileName = f"IRlog--{fileTime}{filename}.csv"

samplingFreq = 100

timeToLog = 60

rSignal = np.loadtxt(rawDataDir + RFileName)
irSignal = np.loadtxt(rawDataDir + IRFileName)

# Remove DC term
rSignalXDC = rSignal - np.mean(rSignal)
irSignalXDC = irSignal - np.mean(irSignal)

# Time
RTime = np.linspace(0, timeToLog, num=len(rSignal))
IRTime = np.linspace(0, timeToLog, num=len(irSignal))

# fft
Rfft = fft(rSignalXDC)
IRfft = fft(irSignalXDC)

Rfreq = fftfreq(len(rSignal), d=1/samplingFreq)
IRFreq = fftfreq(len(irSignal), d=1/samplingFreq)

# Plot
N = len(rSignal) // 8
plt.plot(Rfreq[:N], np.abs(Rfft)[:N])
plt.show()
