from mitmproxy import io
from mitmproxy.exceptions import FlowReadException
import pprint
import sys
import os

logfile = open("NoPermissions", "rb")
freader = io.FlowReader(logfile)
#name = "hello"
#writeFile = open(name+".txt", "w")
#writeFile.write("hello2")
#writeFile.close()

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
    #request = str(flow.request)
    #string += str("%-20s: %s" % ("LENGTH", len(request)))+"\n"
    for k,v in flow.request.headers.items():
        if k.upper() == "USER-AGENT":
            userAgent = str(v).replace("/", "_")
            userAgent = userAgent.replace(":","_")
            #print(v)
        if k.upper() == "CONTENT-LENGTH":
            requestLength.append(v)
            #print("request: ", v)
        string += str("%-20s: %s" % (k.upper(), v))+"\n"
    string += ("-"*50 + "response headers:")+ "\n"
    try:
        for k,v in flow.response.headers.items():
            if k.upper() == "CONTENT-LENGTH":
                responseLength.append(v)
                #print("response: ", v)
            string += str("%-20s: %s" % (k.upper(), v))+"\n"
            string += str("-"*50 + "response headers:")+"\n"
    except:
        pass
    if os.path.exists(userAgent[0:10]+".txt"):
        writeFile = open(userAgent[0:10]+".txt", "a+")
    else:
        writeFile = open(userAgent[0:10]+".txt", "w+")
    writeFile.write(string)
    writeFile.close()
    string=''
print(requestLength)
print ("\n")
print(responseLength)
    #print(string)
    #print(userAgent)





'''
    print("")
    print("=")
    print(flow.request.method + " " + flow.request.path + " " + flow.request.http_version)

    print("-"*50 + "request headers:")
    for k,v in flow.request.headers.items():
      if k.upper() == "USER-AGENT":
        print(k.upper())
      else:
        print("%-20s: %s" % (k.upper(), v))

    print("-"*50 + "response headers:")
    for k, v in flow.response.headers.items():
      print("%-20s: %s" % (k.upper(), v))
      print("-"*50 + "request headers:")
'''
