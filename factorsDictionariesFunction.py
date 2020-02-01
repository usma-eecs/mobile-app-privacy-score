import os
import factorStatFileCreator

dirName = 'NoPerms/'
dirName2 = 'AllPerms/'

freqAgentDic = dict()
lenAgentDic = dict()
contAgentDic = dict()

def freqModAvgFunc(dirName):
    fullList = factorStatFileCreator.directoryFreq(dirName)
    UA = dirName.split("/")[1]
    avgList = []
    sum = 0
    i = 0
    while i <= len(fullList) - 2:
        diff = factorStatFileCreator.diffFunc(fullList[i], fullList[i+1])
        if diff == None:
            i+=1
        else:
            avgList.append(int(diff))
            i+=1
    for item in avgList:
        sum += item
    if len(avgList) != 0:
        if UA not in freqAgentDic.keys():
            freqAgentDic[UA] = [sum/len(avgList)]
        else:
            agentList = freqAgentDic[UA]
            agentList.append(sum/len(avgList))
            freqAgentDic[UA] = agentList

def finalFreqFunc(dirName):
    for filename in os.listdir(dirName):
        file = dirName + filename
        freqModAvgFunc(file)

def printFreqDiff():
    finalFreqFunc(dirName)
    finalFreqFunc(dirName2)
    #print (freqAgentDic)
    for keys, vals in freqAgentDic.items():
        if len(vals) > 1 and vals[1] > 0:
            score = vals[0] / vals[1]
            print ("{:<15}: {:.2f}".format(keys,score))
        else:
            score = "N/A"
            print ("{:<15}: {}".format(keys,score))
        freqAgentDic[keys] = score
    return (freqAgentDic)

def avgModFunc(directory):
    sum = 0
    UA = directory.split("/")[1]
    byteList = factorStatFileCreator.directoryLen(directory)
    for item in byteList:
        sum += item
    if len(byteList) != 0:
        if UA not in lenAgentDic.keys():
            lenAgentDic[UA] = [sum/len(byteList)]
        else:
            agentList = lenAgentDic[UA]
            agentList.append(sum/len(byteList))
            lenAgentDic[UA] = agentList

def finalLenFunc(dirName):
    for filename in os.listdir(dirName):
        file = dirName + filename
        avgModFunc(file)

def printLenDiff():
    finalLenFunc(dirName)
    finalLenFunc(dirName2)
    for keys, vals in lenAgentDic.items():
        if len(vals) > 1 and vals[1] > 0:
            score = vals[1] / vals[0]
            print ("{:<15}: {:.2f}".format(keys,score))
        else:
            score = "N/A"
            print ("{:<15}: {}".format(keys,score))
        lenAgentDic[keys] = score
    return lenAgentDic

def directoryModCont(directory):
    contentSet = set()
    newSet = set()
    listHolder = []
    numofReq = 0
    UA = directory.split("/")[1]
    for filename in os.listdir(directory):
        file = directory + '/' + filename
        listHolder = factorStatFileCreator.contentCommand(file)
        #print(newSet)
        newSet = listHolder[0]
        numofReq += len(listHolder[1])
        contentSet = contentSet|newSet
        newSet = set()
    if UA not in contAgentDic.keys():
        contAgentDic[UA] = [numofReq]
    else:
        agentList = contAgentDic[UA]
        agentList.append(numofReq)
        contAgentDic[UA] = agentList
    return contentSet, numofReq

def finalContFunc(dirName):
    for filename in os.listdir(dirName):
        file = dirName + filename
        directoryModCont(file)

def printContDiff():
    finalContFunc(dirName)
    finalContFunc(dirName2)
    for keys, vals in contAgentDic.items():
        if len(vals) > 1 and vals[1] > 0:
            score = vals[0] / vals[1]
            print ("{:<15}: {:.2f}".format(keys,score))
        else:
            score = "N/A"
            print ("{:<15}: {}".format(keys,score))
        contAgentDic[keys] = score
    return contAgentDic
