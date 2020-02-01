import factorsDictionariesFunction
import time

def calcFinalScore():
    finalDic = dict()
    time.sleep(5)
    print()
    print()
    print ("-------Frequency Difference------- ")
    print()
    freqDic = factorsDictionariesFunction.printFreqDiff()
    time.sleep(5)
    print()
    print()
    print ("---------Length Difference---------")
    print()
    lenDic = factorsDictionariesFunction.printLenDiff()
    time.sleep(5)
    print()
    print()
    print("---------Content Difference---------")
    print()
    contDic = factorsDictionariesFunction.printContDiff()
    time.sleep(5)
    print()
    print()
    print("---------Final Privacy Score---------")
    print()


    for key, item in freqDic.items():
        len = lenDic[key]
        cont = contDic[key]
        finalDic[key] = [item, len, cont]
    for k, v in finalDic.items():
        finalList = []
        finalScore = None
        for val in v:
            if val == 'N/A':
                finalScore = 'N/A'
                pass
            else:
                if val > 3:
                    intScore = 1
                elif val <= 3 and val > 2.0:
                    intScore = 2
                elif val <= 2.0 and val > 1.5:
                    intScore = 3
                elif val <=1.5 and val > 1.0:
                    intScore = 4
                elif val <= 1:
                    intScore = 5
                finalList.append(intScore)
        if finalScore == None:
            finalScore = finalList[0]*(2/3)+finalList[1]*(2/3)+finalList[2]*(2/3)
            print("{:<15}: {:.2f}".format(k, finalScore))
        else:
            print ("{:<15}: {}".format(k,finalScore))
