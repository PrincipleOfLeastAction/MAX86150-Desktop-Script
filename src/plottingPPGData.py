
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

def plottingPPGData(RFileName, IRFileName, timeToLog, distance=58, prominence=1000, mode="dist"):       
    # Read the file back in.
    rSignal = np.loadtxt(RFileName)
    irSignal = np.loadtxt(IRFileName)

    # Remove outliers more than 10 standard deviations
    # away from average
    rSignal = rejectOutliers(rSignal)
    irSignal = rejectOutliers(irSignal)

    # Get the peaks.
    if mode == "dist":
        rPeaks, _ = find_peaks(rSignal, distance=distance)
    ##    rPeaks, _ = find_peaks(rSignal, width=20, prominence=500)
    
        irPeaks, _ = find_peaks(irSignal, distance=distance)
    ##    irPeaks, _ = find_peaks(irSignal, width=20, prominence=500)
    elif mode == "prominence":
        rPeaks, _ = find_peaks(rSignal, prominence=prominence)
        irPeaks, _ = find_peaks(irSignal, prominence=prominence)

    rTroughs, _ = find_peaks(-rSignal, distance=distance)
    irTroughs, _ = find_peaks(-irSignal, distance=distance)

    # Unfortunately SpO2 requires calibration that I cannot do. :(    
    ##    print(rPeaks)
    ##    print(rTroughs)
    ##    print(f"rSignal={rPeaks[2]}")
    ##    print(f"rClosest = {min(rTroughs, key=lambda x: abs(x-rPeaks[2]))}")
    ##    R_dIntensityStart = rSignal[rPeaks[2]] - \
    ##        rSignal[min(rTroughs, key=lambda x: abs(x-rPeaks[2]))]
    ##    IR_dIntensityStart = irSignal[irPeaks[2]] - \
    ##        rSignal[min(irTroughs, key=lambda x: abs(x-irPeaks[2]))]
    ##    # SpO2 using calculation Here
    ##    # https://www.hindawi.com/journals/cmmm/2017/9468503/
    ##    # SpO2 = A * (dI'/I'_max)/(dI)
    ##    print(R_dIntensityStart)
    ##    print(IR_dIntensityStart)

    ##    SPO2_Start = 
    ##    SPO2_Middle
    ##    SPO2_End

    print(f"Heart rate from  R LED is {len(rPeaks)/timeToLog * 60} per minute")
    print(f"Heart rate from IR LED is {len(irPeaks)/timeToLog * 60} per minute")

    RTime = np.linspace(0, timeToLog, num=len(rSignal))
    IRTime = np.linspace(0, timeToLog, num=len(irSignal))

    # Plot the signal for manual review.
    plt.plot(RTime, rSignal, "r", label="Red")
    plt.plot(IRTime, irSignal, "k", label="Infrared")
    plt.legend()
    plt.plot(RTime[rPeaks], rSignal[rPeaks], "xb")
    #plt.plot(rTroughs, rSignal[rTroughs], "*b")
    plt.plot(IRTime[irPeaks], irSignal[irPeaks], "xg")
    #plt.plot(irTroughs, irSignal[irTroughs], "*g")

    
    plt.xlabel("Time [s]")
    plt.ylabel("Absorbance (Rel)")
    plt.title("PPG signal")
    plt.show()

# Reject all data that is more than nSD standard
# deviations away from the average
def rejectOutliers(data, nSD=10):
    return data[abs(data- np.mean(data)) < nSD * np.std(data)]
    
