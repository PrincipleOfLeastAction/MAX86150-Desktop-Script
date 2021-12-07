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

