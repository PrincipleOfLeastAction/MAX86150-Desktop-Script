from scipy.signal import spectrogram
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

rSignal = np.loadtxt(rawDataDir + RFileName)
irSignal = np.loadtxt(rawDataDir + IRFileName)

# Remove DC components
rSignalXDC = rSignal - np.mean(rSignal)
irSignalXDC = irSignal - np.mean(irSignal)

f,t, Sxx = spectrogram(rSignalXDC, fs=samplingFreq, nperseg=37, noverlap=18, nfft=256)

N = len(f) //6

print(t.shape)
print(f.shape)
print(Sxx.shape)

plt.pcolormesh(t, f[:N], Sxx[:N], shading="gouraud")
plt.ylabel("frequency (Hz)")
plt.xlabel("Time (sec)")
plt.show()
