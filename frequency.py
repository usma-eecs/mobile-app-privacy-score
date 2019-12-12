
import os
dirName = 'NoPerm/'
fileN = 'Averages.txt'

def frequencyCommand(filepath):
    timeList = []
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            if line[0:4] == "DATE":
                timeList.append(line.split(" ")[21])
            line = fp.readline()
    return timeList

def directoryFreq(directory):
    freqList = []
    newList = []
    for filename in os.listdir(directory):
        file = directory + '/' + filename
        newList = frequencyCommand(file)
        for item in newList:
            freqList.append(item)
        newList = []
    freqList.sort()
    #print(freqList)
    return freqList

def diffFunc(startNum, endNum):
    sSplit = startNum.split(":")
    eSplit = endNum.split(":")
    hrs = int(eSplit[0]) - int(sSplit[0])
    if hrs != 0:
        pass
        return None
    else:
        min = int(eSplit[1]) - int(sSplit[1])
        sec = int(eSplit[2]) - int(sSplit[2])
        hTs = hrs*3600
        mTs = min*60
        finalSec = hTs + mTs + sec
        return finalSec

def avgFunc(dirName):
    fullList = directoryFreq(dirName)
    avgList = []
    sum = 0
    i = 0
    while i <= len(fullList) - 2:
        diff = diffFunc(fullList[i], fullList[i+1])
        if diff == None:
            i+=1
        else:
            avgList.append(int(diff))
            i+=1
    for item in avgList:
        sum += item
    if len(avgList) != 0:
        #print (sum/len(avgList), min(avgList), max(avgList), len(avgList))
        return sum/len(avgList), min(avgList), max(avgList), len(avgList)
    else:
        return 0, 0, 0, 0

def writeFunc(dirName, fileN):
    number = avgFunc(dirName)
    nameSplit = dirName.split("/")
    #text = str(number[0]) + "   " + str(number[1])
    toWrite = "{:15}\nAverage Length: {:<12.2f} Min Length: {:<12} Max Length: {:<12} Total Transmissions: {:<12}\n{}\n\n".format(nameSplit[1], number[0], number[1], number[2], number[3], "---"*35)
    #toWrite = dirName +": " + text + "\n"
    #print(text)
    with open(fileN, 'a') as f:
        f.write(toWrite)

for filename in os.listdir(dirName):
    file = dirName + filename
    writeFunc(file, fileN)
