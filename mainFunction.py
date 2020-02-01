from mitmproxy import io
from mitmproxy.exceptions import FlowReadException
import pprint
import sys
import os
import factorStatFileCreator
import printFinalFactorAndScore
UserDic = {"Amazon": ["Amazon_267", "AmazonWebV", "Arcus-iOS_", "aws-sdk-iO", "mShop___Te"], "Apple": ["AppleCoreM","geod_1 CFN","itunesstor","MobileAsse","Mozilla_5.","SafariSafe","StoreKitUI"], "Bitmoji": ["imoji_10.7"],"CashApp": ["Cash_30400"], "FaceBook":["FBiOSSDK.4","FBiOSSDK.5"], "Gmail":["Gmail_6.0.","Google Gma"],"GoogleChrome": ["Chrome IOS","Chrome_79."],"GooglePhotos":["Google%20P"], "Netflix" : ["Argo_12.13","Argo_2925 "], "Pandora": ["Pandora_19","Pandora_21"], "Spotify": ["Spotify_8.", "Spotify_85"], "TikTok": ["TikTok_141"], "Twitter": ["Twitter_8."],"Uber":["com.uberca","Uber_3.382"], "Wish": ["Wish_4.24.","Wish_1109 "], "YouTube": ["com.google", "YouTube_14"] }
#logfile = open("NoPermissions", "rb")
#freader = io.FlowReader(logfile)
#name = "hello"
#writeFile = open(name+".txt", "w")
#writeFile.write("hello2")
#writeFile.close()
NP = input("Enter the name of the file that contains the traffic for apps with NO PERMISSIONS: ")
logfileNP = open(str(NP), "rb")
AP = input("Enter the name of the file that contains the traffic for apps with ALL PERMISSIONS: ")
logfileAP = open(str(AP), "rb")
pwd = str(os.getcwd())
pathNP = pwd + "/NoPerms"
pathAP = pwd + "/AllPerms"
os.mkdir(pathNP)
os.mkdir(pathAP)
dirName = 'NoPerms/'
dirName2 = 'AllPerms/'

def directoryFunc(logfile, path):
    freader = io.FlowReader(logfile)
    string=''
    requestLength = []
    responseLength = []
    responseTime = []
    requestTime = []
    for flow in freader.stream():
        string += "\n"
        string += "=\n"
        string += str(flow.request.method + " " + flow.request.path + " " + flow.request.http_version)+"\n"
        string += str("-"*50 + "request headers:")+"\n"
        for k,v in flow.request.headers.items():
            if k.upper() == "USER-AGENT":
                userAgent = str(v).replace("/", "_")
                userAgent = userAgent.replace(":","_")
                #print(v)
            if k.upper() == "CONTENT-LENGTH":
                requestLength.append(v)
            string += str("%-20s: %s" % (k.upper(), v))+"\n"
        string += ("-"*50 + "response headers:")+ "\n"
        try:
            for k,v in flow.response.headers.items():
                if k.upper() == "CONTENT-LENGTH":
                    responseLength.append(v)
                string += str("%-20s: %s" % (k.upper(), v))+"\n"
                string += str("-"*50 + "response headers:")+"\n"
        except:
            pass
        for key, value in UserDic.items():
            if userAgent[0:10] in value:
                UserFile = str(key)
                break
            else:
                UserFile = None
        if UserFile == None:
            UserFile = input ("What UserAgent does " + userAgent + " belong to?: ")
            if UserFile in UserDic.keys():
                dicList = UserDic[UserFile]
                dicList.append(userAgent[0:10])
                UserDic[UserFile] = dicList
            else:
                UserDic[UserFile] = [userAgent[0:10]]
        if os.path.exists(path+"/"+UserFile+"/"+UserFile+".txt"):
            writeFile = open(path+"/"+UserFile+"/"+UserFile+".txt", "a+")
        else:
            os.mkdir(path+"/"+UserFile)
            writeFile = open(path+"/"+UserFile+"/"+UserFile+".txt", "w+")
        writeFile.write(string)
        writeFile.close()
        string=''

directoryFunc(logfileNP, pathNP)
print ("Almost Done Separating Network traffic By User Agents")
directoryFunc(logfileAP, pathAP)
print ("All network traffic has been separated by User Agents")
print ("Calculating Scores...")
factorStatFileCreator.finalFunc(dirName, "NP")
factorStatFileCreator.finalFunc(dirName2, "AP")
printFinalFactorAndScore.calcFinalScore()
