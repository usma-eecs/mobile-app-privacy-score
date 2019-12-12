import os
dirName = 'NoPerm/'
dirName2 = 'AllPerm/'
fileN1 = 'FreqAvg NP.txt'
fileN2 = 'LenAvg NP.txt'
fileN3 = 'FreqAvg AP.txt'
fileN4 = 'LenAvg AP.txt'

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

def freqAvgFunc(dirName):
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

def freqWriteFunc(dirName, fileN):
    number = freqAvgFunc(dirName)
    nameSplit = dirName.split("/")
    #text = str(number[0]) + "   " + str(number[1])
    toWrite = "{:15}\nAverage Frequency: {:<12.2f} Min Length: {:<12} Max Length: {:<12} Total Transmissions: {:<12}\n{}\n\n".format(nameSplit[1], number[0], number[1], number[2], number[3], "---"*37)
    #toWrite = dirName +": " + text + "\n"
    #print(text)
    with open(fileN, 'a') as f:
        f.write(toWrite)

def finalFreqFunc(dirName, fileN):
    for filename in os.listdir(dirName):
        file = dirName + filename
        freqWriteFunc(file, fileN)

def lengthCommand(filepath):
    lengthList = []
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            #print (line[0:13])
            if line[0:14] == "CONTENT-LENGTH":
                num = line.split(" ")[7]
                lengthList.append(num[:-1])
            line = fp.readline()
    #print(lengthList)
    return lengthList
#lengthCommand("Amazon/Amazon_267.txt")

def directoryLen(directory):
    lenList = []
    newList = []
    for filename in os.listdir(directory):
        file = directory + '/' + filename
        newList = lengthCommand(file)
        for item in newList:
            lenList.append(int(item))
        newList = []
    #print(lenList)
    return lenList

def avgFunc(directory):
    sum = 0
    byteList = directoryLen(directory)
    for item in byteList:
        sum += item
    if len(byteList) != 0:
        #print(sum/len(byteList), min(byteList), max(byteList), len(byteList))
        return sum/len(byteList), min(byteList), max(byteList), len(byteList)
    else:
        return 0,0,0,0

def writeFunc(dirName, fileN):
    data = avgFunc(dirName)
    nameSplit = dirName.split("/")
    #print(nameSplit)
    #text = "Average Length: " + str(data[0]) + " Min Length: " + str(data[1]) + " Max Length: " + str(data[2]) + " Total Trans: " + str(data[3])
    toWrite = "{:15}\nAverage Length: {:<12.2f} Min Length: {:<12} Max Length: {:<12} Total Transmissions: {:<12}\n{}\n\n".format(nameSplit[1], data[0], data[1], data[2], data[3], "---"*35)
    #print(text)
    #toWrite = dirName + ":"+ "\n" + text + "\n" + "--"*30 + "\n"
    with open(fileN, 'a') as f:
        f.write(toWrite)
#writeFunc("Amazon", "average.txt")
def finalLenFunc(dirName, fileN):
    for filename in os.listdir(dirName):
        file = dirName + filename
        writeFunc(file, fileN)

finalFreqFunc(dirName, fileN1)
finalLenFunc(dirName, fileN2)
finalFreqFunc(dirName2, fileN3)
finalLenFunc(dirName2, fileN4)
