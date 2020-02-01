import os

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
        return sum/len(avgList), min(avgList), max(avgList), len(avgList)
    else:
        return 0, 0, 0, 0

def freqWriteFunc(dirName, fileN):
    number = freqAvgFunc(dirName)
    nameSplit = dirName.split("/")
    toWrite = "{:15}\nAverage Frequency: {:<12.2f} Min Frequency: {:<12} Max Frequency: {:<12} Total Transmissions: {:<12}\n{}\n\n".format(nameSplit[1], number[0], number[1], number[2], number[3], "---"*37)
    with open(fileN, 'a') as f:
        f.write(toWrite)

def lengthCommand(filepath):
    lengthList = []
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            if line[0:14] == "CONTENT-LENGTH":
                num = line.split(" ")[7]
                lengthList.append(num[:-1])
            line = fp.readline()
    return lengthList

def directoryLen(directory):
    lenList = []
    newList = []
    for filename in os.listdir(directory):
        file = directory + '/' + filename
        newList = lengthCommand(file)
        for item in newList:
            lenList.append(int(item))
        newList = []
    return lenList

def avgFunc(directory):
    sum = 0
    byteList = directoryLen(directory)
    for item in byteList:
        sum += item
    if len(byteList) != 0:
        return sum/len(byteList), min(byteList), max(byteList), len(byteList)
    else:
        return 0,0,0,0

def writeFunc(dirName, fileN):
    data = avgFunc(dirName)
    nameSplit = dirName.split("/")
    toWrite = "{:15}\nAverage Length: {:<12.2f} Min Length: {:<12} Max Length: {:<12} Total Transmissions: {:<12}\n{}\n\n".format(nameSplit[1], data[0], data[1], data[2], data[3], "---"*35)
    with open(fileN, 'a') as f:
        f.write(toWrite)

def contentCommand(filepath):
    contentSet = set()
    contentList = []
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            if line[0:4] == "GET " or line[0:4]=="PUT " or line[0:4]=="POST":
                lineSplit = line.split(" ")
                if "&" in lineSplit[1]:
                    otherSplit = lineSplit[1].split("&")
                    for item in otherSplit[1:]:
                        if "%" not in item and len(item.split("=")[0]) > 3:
                            contentSet.add(item.split("=")[0])
                        contentList.append(item)
            line = fp.readline()
    return contentSet, contentList

def directoryCont(directory):
    contentSet = set()
    newSet = set()
    listHolder = []
    numofReq = 0
    for filename in os.listdir(directory):
        file = directory + '/' + filename
        listHolder = contentCommand(file)
        newSet = listHolder[0]
        numofReq += len(listHolder[1])
        contentSet = contentSet|newSet
        newSet = set()
    return contentSet, numofReq

def contentWrite(dirName, fileN):
    data = directoryCont(dirName)
    string = ""
    nameSplit = dirName.split("/")
    toWrite = str(nameSplit[1]).upper() + "\n"
    cnt = 0
    i = 0
    for item in data[0]:
        if cnt != 3:
            string += "{:<45}".format(item)
            if i == len(data[0])-1:
                toWrite += string + "\n"
        else:
            toWrite += string + "\n"
            string = "{:<45}".format(item)
            cnt = 0
        cnt += 1
        i +=1
    toWrite += "Total Info: {}\n{}\n\n".format(data[1],"---"*40)
    with open(fileN, 'a') as f:
        f.write(toWrite)

def finalFunc(dirName, perms):
    for filename in os.listdir(dirName):
        file = dirName + filename
        freqWriteFunc(file, "FreqAVG_"+perms +".txt")
        writeFunc(file, "LenAVG_"+perms +".txt")
        contentWrite(file, "ContAVG_"+perms +".txt")
