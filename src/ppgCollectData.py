import serial
import time
from math import ceil
import serial.tools.list_ports 

from scipy.signal import find_peaks

from metadata import *

class NoComPortFoundError(Exception):
    pass

def collectData(comPort, baudRate, RFileName, IRFileName, metaFile, 
                timeToLog, stabilisationTime, timeToPrint, 
                sampleRate=100, prominence=1000):
    # Open the file
    RFile = open(RFileName, "w")
    IRFile = open(IRFileName, "w")
    
    hasError = False
    errorString = []
    errorLine = 0
    # Open serial
    with serial.Serial(comPort, baudRate, timeout=1) as ser:
        # Let the data stabilize and then reset the buffer.
        startTime = time.time()
        print("Stabilising...")
        while time.time() - startTime < stabilisationTime:
            continue
        ser.reset_input_buffer()
        # Remove ser.readline() until we get to I prefix.
        while True:
            line = ser.readline()
            try:
                decodedStr = line.decode("utf-8").rstrip()                
            except UnicodeDecodeError:
                print(f"Decode error {line}")
                hasError = True
                errorLine += 1
                metaFile.errorLogs[str(errorLine)] =  \
                                 decodedStr
                continue
            if (decodedStr[0] == "I"):
                break
        print("Logging beginning...")

        # Begin logging our PPG rate.
        dataPointsLogged = 0
        # Add time header to the logs. 
        metaFile.insertNewLine()
        metaFile.insertSubsection("Logging beginning")
        timeFormat="%I:%M:%S %p"
        dateFormat="%d/%b/%Y %a %Z gmt%z"
        loggingStartTime = time.strftime(timeFormat)
        loggingStartDate = time.strftime(dateFormat)

        metaFile.logData("Logging start Time", loggingStartTime)
        metaFile.logData("Logging start date", loggingStartDate)
        
        metaFile.writeUserData()
        
        # Used for temporary logs for instant HR feedback.
        RArray = []
        IRArray = []
        
        # Log the data coming in via serial
        while time.time() - (startTime + stabilisationTime) < timeToLog:
            durationSoFar = time.time() - (startTime + stabilisationTime)
            # Every 10 seconds, we print the time to go.
            if durationSoFar > timeToPrint:
                print(f"{ceil(timeToLog - durationSoFar)}s to go.")
                timeToPrint += 10
                
                # Calculate the heart rate for last 10 seconds
                # 10s * samplesPerSec = samples
                samplesToInclude = 10 * sampleRate
                if len(RArray) < samplesToInclude:
                    samplesToInclude = len(RArray)
                
                rPeaks, _ = find_peaks(RArray[-samplesToInclude:], prominence=prominence)
                irPeaks, _ = find_peaks(IRArray[-samplesToInclude:], prominence=prominence)
                print(f"##### HR R : {len(rPeaks) /10 * 60} bpm #####")
                print(f"##### HR IR: {len(irPeaks)/10 * 60} bpm #####")
                
            # Read a line from serial and then decode it by stripping
            # newline character.
            line = ser.readline()
##            print(line.decode("utf-8").rstrip())
            try:
                decodedStr = line.decode("utf-8").rstrip()                
            except UnicodeDecodeError:
                print(f"Decode error {line}")
                hasError = True
                errorLine += 1
                metaFile.errorLogs[str(errorLine)] =  \
                                 decodedStr
                continue
            # Ensure the line we got is a string. If not print
            # the non-int data into terminal.
            try:
                int(decodedStr[1:])
            except ValueError:
                print(f"Removed String '{decodedStr}'")
                hasError = True
                errorLine += 1
                metaFile.errorLogs[str(errorLine)] = \
                                 decodedStr
                continue
            # Write the string data into file.
            if decodedStr[0] == "R":
                RFile.write(decodedStr[1:] + "\n")
                RArray.append(int(decodedStr[1:]))
                dataPointsLogged += 1
            elif decodedStr[0] == "I":
                IRFile.write(decodedStr[1:] + "\n")
                IRArray.append(int(decodedStr[1:]))

            elif decodedStr[0] == "W":
                print(f"values lost {decodedStr[1:]}")
    loggingEndTime = time.strftime(timeFormat)
    loggingEndDate = time.strftime(dateFormat)

    metaFile.logData("Logging end Time", loggingEndTime)
    metaFile.logData("Logging end date", loggingEndDate)
    metaFile.logData("Data points captured",
                     str(dataPointsLogged) + " points")
    metaFile.writeUserData()
    
    # New section for errors caught.
    metaFile.insertNewLine()
    metaFile.insertSubsection("Errors")
    metaFile.writeErrorLogs()
    
    # Close the file
    RFile.close()
    IRFile.close()
    print("Logging Complete")
    return errorLine, hasError

def comPortValidator(comPort):
    # Check if comport exists
    lstPorts = serial.tools.list_ports.comports()
    if (not lstPorts):
        raise NoComPortFoundError
    if (not comPort in map(lambda p: p.device, lstPorts)):
        print(f"{comPort} not found.")
        print("Choose available com port below:")
        print("-----------------------------------")
        for i, p in enumerate(lstPorts):
            print(f"{i+1}: {p}")
        try:
            comPortIndex = int(input("Select index of com port: "))
        except ValueError:
            raise ValueError("Input must be a number")

    # Check if the index is within bound.
    if comPortIndex > len(lstPorts) or comPortIndex < 1:
        raise ValueError(f"Index out of bound. Choose between 1-{len(lstPorts)}")
    # Redefine the comport if one isn't found.
    comPort = lstPorts[comPortIndex-1]
    return comPort.device
