import os

dirName = 'AllPerm/'
fileN = "Averages.txt"

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

finalLenFunc(dirName, fileN)
