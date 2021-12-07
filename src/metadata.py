import time
import os.path

class metadata:
    # subsections
    
    def __init__(self, filename, title="logfile"):
        self.title = title
        self.generatedData = {}
        self.userData = {}
        self.errorLogs = {}
        self.metafile = self.__createFile(filename)
        self.dataNotSaved = False
        self.buffer = ""
                
    def __createFile(self, filename):
        filename = self.__getUniqueFilename(filename)
        return open(filename, "w")
    
    def closeFile(self, checkForUserData=True):
        if (checkForUserData and self.dataNotSaved):
            print("Warning some user data has not been saved.")
            return
        else:
            self.metafile.close()
        
    def __getUniqueFilename(self, filename):
        i = 2
        index = ""
        while True:
            # filename doesn't exist.
            if not os.path.exists(filename + index):
                filename += index
                break
            # index is blank string.
            elif not index:
                index = "(1)"
            # increment in counter
            else:
                index = "(" + str(i) + ")"
                i += 1
        return filename
            
    def insertSubsection(self, subsectionName):
        self.metafile.write(f"####### {subsectionName} #######\n")
    
    def insertNewLine(self):
        self.metafile.write("\n")
    
    def bufferSubsection(self, subsectionName):
        self.buffer = subsectionName
    
    def writeSubsectionBuffer(self):
        self.insertSubsection(self.buffer)
    
    def logData(self, fieldName, data):
        self.userData[str(fieldName)] = str(data)
           
    def logError(self, fieldName, data):
        self.errorLogs[str(fieldName)] = str(data)
    
    def writeErrorLogs(self):
        for field, data in self.errorLogs.items():
            line = field + " = " + data
            self.metafile.write(line + "\n")
        self.errorLogs = {}
    
    def basicTimeInformation(self, timeFormat="%I:%M:%S %p", dateFormat="%d/%b/%Y %a %Z gmt%z"):
        # current time in this format '02:10:08 PM'
        currentTime = time.strftime(timeFormat)
        # Current data in this format:
        # '25/Nov/2020 Wed AUS Eastern Daylight Time gmt+1100'
        currentDate = time.strftime(dateFormat)
        self.generatedData["script start date"] = currentDate
        self.generatedData["script start time"] = currentTime
        
    def createHeader(self):
        self.metafile.write(f"########## {self.title} ########## \n")
        for name, data in self.generatedData.items():
            line = name + " = " + data
            self.metafile.write(line + "\n")
            
    def writeUserData(self):
        for field, data in self.userData.items():
            line = field + " = " + data
            self.metafile.write(line + "\n")
        self.userData = {}