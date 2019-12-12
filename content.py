import os

dirName = 'AllPerm/'
fileN = 'Content AP.txt'
dirName2 = 'NoPerm/'
fileN2 = 'Conent NP.txt'

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
                    #print (otherSplit[1:])
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
        #print(newSet)
        newSet = listHolder[0]
        numofReq += len(listHolder[1])
        contentSet = contentSet|newSet
        newSet = set()
    #print(numofReq)
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
    #print(toWrite)
    #toWrite = "{}\n{}\n{}\n{}\n".format(dirName, string, data[1],"--"*20)
    with open(fileN, 'a') as f:
        f.write(toWrite)
#contentWrite("Amazon", "average.txt")
def finalContFunc(dirName, fileN):
    for filename in os.listdir(dirName):
        file = dirName + filename
        contentWrite(file, fileN)

finalContFunc(dirName, fileN)
finalContFunc(dirName2, fileN2)
#contentWrite('Amazon', 'average.txt')

#contentWrite("Amazon", "content.txt")
#directoryCont("Amazon")
