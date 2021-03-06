# coding: utf-8
import sys
sys.path.append('../common')  # 親ディレクトリのファイルをインポートするための設定
#sys.path.append('..')
import wave
from pylab import *
import os
import glob
from sound import *
import numpy as np
import matplotlib.pyplot as plt

def volumeBoost(sig, fs):
    for i in range(len(sig)):
        sig[i] = sig[i] * (1 + i/(fs/8))
    return sig

def synthesis(sigList, randList):
    maxLength = 0
    tmpLength = 0

    tmpIndex = 0

    #print("randList", randList)
    """a = np.zeros(1000000)
    k = a + sigList[randList[0]]
    print(type(a))
    print(a.shape)
    print(sigList[randList[0]].shape)
    print(len(a))
    print(type(sigList[randList[0]]))
    sys.exit()"""

    for i in range(3):
        #print(len(sigList[randList[i]]))
        if len(sigList[randList[i]]) > tmpLength:
            maxLength = len(sigList[randList[i]])
            tmpLength = len(sigList[randList[i]])
            tmpIndex = i

    sig1 = np.zeros(maxLength)
    sig2 = np.zeros(maxLength)
    sig3 = np.zeros(maxLength)

    for i in range(len(sig1)):
        if len(sigList[randList[0]]) > i:
            sig1[i] = sigList[randList[0]][i]

    for i in range(len(sig2)):
        if len(sigList[randList[1]]) > i:
            sig2[i] = sigList[randList[1]][i]

    for i in range(len(sig3)):
        if len(sigList[randList[2]]) > i:
            sig3[i] = sigList[randList[2]][i]

    """tmp = randList[i]
    randList[i] = randList[0]
    randList[i] = tmp"""

    #print(randList)

    """for i in range(len(sigList[randList[0]]) - len(sigList[randList[1]])):
        len(sigList[randList[1]]).append(0)

    for i in range(len(sigList[randList[0]]) - len(sigList[randList[2]])):
        len(sigList[randList[2]]).append(0)"""


    """for i in range(1, 3):
        if len(sigList[randList[i]]) > tmpLength:
            maxLength = len(sigList[randList[i]])
            tmpLength = len(sigList[randList[i]])
            tmpIndex = i"""


    """tmp = randList[i]
    randList[i] = randList[1]
    randList[i] = tmp"""




    """for i in sigList:
        if len(i) > tmpLength:
            maxLength = len(i)
            tmpLength = len(i)"""

    sig = np.zeros(maxLength)
    sig = sig1 + sig2 + sig3
    return sig

def fastForward(sig):
    sigFast = []
    for i in range(0, len(sig), 2):
        sigFast.append(sig[i] / 100)

    return sigFast


def parentpath(path=__file__, f=0):
    return str('/'.join(os.path.abspath(path).split('/')[0:-1-f]))

def nomalize(x, xmax, xmin, a):
    min = 1 / 32768.0
    try:
        z = a * (x - xmin) / (xmax - xmin)
    except ZeroDivisionError:
        z = a * (x - xmin) / min
    #print ("1e-7")
    #print (1e-7)
    return z

def simplicityCocktail(sigList, randList):
    #print("simplicityCocktail")
    maxLength = 0
    tmpLength = 0
    for i in sigList:
        if len(i) > tmpLength:
            maxLength = len(i)
            tmpLength = len(i)


    print(maxLength / 16000)
    sig = np.zeros(maxLength*2)
    sigL = np.zeros(maxLength)
    sigR = np.zeros(maxLength)


    sig1 = np.zeros(maxLength)
    sig2 = np.zeros(maxLength)
    sig3 = np.zeros(maxLength)

    for i in range(len(sig1)):
        if len(sigList[randList[0]]) > i:
            sig1[i] = sigList[randList[0]][i]

    for i in range(len(sig2)):
        if len(sigList[randList[1]]) > i:
            sig2[i] = sigList[randList[1]][i]

    for i in range(len(sig3)):
        if len(sigList[randList[2]]) > i:
            sig3[i] = sigList[randList[2]][i]



    sigL = sig1 + sig3
    sigR = sig2 + sig3

    print(len(sig)/16000)
    #print(len(sigL)*2)
    j=0
    for i in range(0, len(sig), 2):
        if j < len(sigL):
            sig[i] = sigL[j]
        if j < len(sigR):
            sig[i+1] = sigR[j]
        j+=1
    print(len(sig)/16000)

    return sig


if __name__ == "__main__" :
    argvs = sys.argv
    curDirPath = os.path.dirname(os.path.abspath(__file__))
    wavDataPath = parentpath(__file__,1) + "/wav/millionTheater"
    millionWavPathList = glob.glob(wavDataPath + "/*.wav")
    print (curDirPath)
    print (wavDataPath)
    print(millionWavPathList)

    filedata = openFile(millionWavPathList[0])
    sig = filedata[0]
    fs = filedata[1]
    L = filedata[2]

    sigList = []
    for i in millionWavPathList:
        sigList.append(openFile(i, 0)[0])

    lenSigList = len(sigList)
    #print(lenSigList)

    parentPath = parentpath(__file__,1)

    for i in range(20):
        print(i)
        randList = np.random.randint(0,lenSigList,3)

        filename = millionWavPathList[randList[0]].split("/")[-1][:-4] + "." + millionWavPathList[randList[1]].split("/")[-1][:-4] + "." + millionWavPathList[randList[2]].split("/")[-1][:-4]
        filepath = parentPath + "/output/synthesis/" + filename
        sigSyn = synthesis(sigList, randList)
        sigmin = min(sigSyn)
        sigmax = max(sigSyn)
        sigSyn = nomalize(sigSyn, sigmax, sigmin, 1)
        sigSyn = sigSyn
        save(sigSyn, fs, 16, filepath)


        filepath = parentPath + "/output/cocktail/" + filename
        sigSyn = simplicityCocktail(sigList, randList)
        sigmin = min(sigSyn)
        sigmax = max(sigSyn)
        sigSyn = nomalize(sigSyn, sigmax, sigmin, 1)
        sigSyn = sigSyn
        save(sigSyn, fs, 16, filepath, channel=2)
        """plt.plot(sigSyn)
        plt.show()"""
        #print(filepath)
        #sys.exit()
