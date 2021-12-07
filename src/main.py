import time

from metadata import *
from ppgCollectData import *
from plottingPPGData import *
import os

""" To do:
Make a metadata file along with the data
To log:
    - Duration
    - Stabilisation time
    - File names for R and IR
    - time of logging
    - distance
    - Date
    - Start time
    - Values lost?
    - Heart rate for both R and IR.
    - 
"""

# Log for n seconds
timeToLog = 60
# Time for sensor to stabilise before logging.
stabilisationTime = 10

#prints duration every 10 sec.
timeToPrint = 10

CollectData = False
calculateHeartRate = True

# For finding peaks. (higher HR requires lower distance)
distance = 58
##distance = 37

# Logging file dir
loggingFileDir = "C:/Users/Mkafahul/Documents/Code/Python/Heart Rate/loggingFiles/"

# File time if not collecting data
#fileTimeMode = "latest"
fileTimeMode = ""
filename = ""
#fileTime = "2020-12-14--15-10-31"
fileTime = "2021-11-28--11-42-34"

if fileTimeMode == "latest":
    loggingFilesList = sorted(
                        list(
                            map(
                            lambda x: x.rstrip("_logs"),
                            os.listdir(loggingFileDir)
                            )
                        )
                       )
    # latest file time.
    fileTime = loggingFilesList[-1]


# COMPORT
# Don't know which comport?
# List them all with the command

# from serial.tools import list_ports
# list(map(lambda x: x.device, list_ports.comports()))

comPort = "COM12"
baudRate = 115200

# override file time if collecting data.
if CollectData:
    fileTime = time.strftime("%Y-%m-%d--%H-%M-%S")

    # Filename for metadata.
    metaDataFileName = f"META--{fileTime}.txt"

rawDataDir = loggingFileDir + f"{fileTime}{filename}_logs/"
RFileName = f"Rlog--{fileTime}{filename}.csv"
IRFileName = f"IRlog--{fileTime}{filename}.csv"


if __name__ == "__main__":
    
    if CollectData:
        # Validate the comport first.
        comPort = comPortValidator(comPort)
        
        # Make a directory to store the logs
        try:
            os.mkdir(rawDataDir)
        except OSError:
            print ("Creation of the directory %s failed" % rawDataDir)
        else:
            print ("Successfully created the directory %s " % rawDataDir)
       
        ###### Meta data file ######
        metaFile = metadata(rawDataDir + metaDataFileName, title="PPG log files")
        metaFile.basicTimeInformation()
        metaFile.createHeader()

        metaFile.insertNewLine()
        metaFile.insertSubsection("Logging Configuration")

        metaFile.logData("time logged", str(timeToLog) + "s")
        metaFile.logData("stabilisationTime", str(stabilisationTime) + "s")
        metaFile.logData("time to print", str(timeToPrint) + "s")
        metaFile.logData("Distance Used", str(distance) + " data points")
        metaFile.writeUserData()

        numErrors, hasError = collectData(comPort, baudRate, rawDataDir + RFileName,
                    rawDataDir + IRFileName, metaFile, timeToLog,
                    stabilisationTime, timeToPrint)

        metaFile.logData("has error", hasError)
        metaFile.logData("number of errors", numErrors)
        metaFile.writeUserData()
        metaFile.closeFile()

    if calculateHeartRate:
        plottingPPGData(rawDataDir + RFileName, 
        rawDataDir + IRFileName,
        timeToLog, distance=distance, mode="dist")

