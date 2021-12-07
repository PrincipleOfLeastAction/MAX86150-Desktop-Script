from scipy.fft import fft, fftfreq
from scipy.signal import hilbert
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

# Analytic signal
RAnalyticSignal = hilbert(rSignal)
RAmplitudeEnvelope = np.abs(RAnalyticSignal)

plt.plot(RTime, np.abs(rSignal))
plt.plot(RTime, RAmplitudeEnvelope)
plt.show()
