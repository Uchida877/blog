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

    for i in range(2):
        #print(len(sigList[randList[i]]))
        if len(sigList[randList[i]]) > tmpLength:
            maxLength = len(sigList[randList[i]])
            tmpLength = len(sigList[randList[i]])
            tmpIndex = i

    sig1 = np.zeros(maxLength)
    sig2 = np.zeros(maxLength)

    for i in range(len(sig1)):
        if len(sigList[randList[0]]) > i:
            sig1[i] = sigList[randList[0]][i]

    for i in range(len(sig2)):
        if len(sigList[randList[1]]) > i:
            sig2[i] = sigList[randList[1]][i]

    sig = np.zeros(maxLength)
    sig = sig1 + sig2
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
    maxLength = 0
    tmpLength = 0
    for i in sigList:
        if len(i) > tmpLength:
            maxLength = len(i)
            tmpLength = len(i)


    sig = np.zeros(maxLength*2)
    sigL = np.zeros(maxLength)
    sigR = np.zeros(maxLength)


    sig1 = np.zeros(maxLength)
    sig2 = np.zeros(maxLength)

    for i in range(len(sig1)):
        if len(sigList[randList[0]]) > i:
            sig1[i] = sigList[randList[0]][i]

    for i in range(len(sig2)):
        if len(sigList[randList[1]]) > i:
            sig2[i] = sigList[randList[1]][i]



    sigL = sig1
    sigR = sig2

    j=0
    for i in range(0, len(sig), 2):
        if j < len(sigL):
            sig[i] = sigL[j]
        if j < len(sigR):
            sig[i+1] = sigR[j]
        j+=1

    return sig

def monoral2stereo(sigL, sigR=[]):

    stereo = []
    if len(sigR) == 0:
        for i in range(len(sigL)):
            stereo.append(sigL[i])
            stereo.append(sigL[i])

    else:
        for i in range(len(sigL)):
            stereo.append(sigL[i])
            stereo.append(sigR[i])

    return stereo


def itd(sig, fs):

    itdParam = int(fs*(1/10000))
    outLength = int(len(sig) + itdParam)

    sigL = np.zeros(outLength)
    sigR = np.zeros(outLength)

    for i, data in enumerate(sig):
        sigL[i+itdParam] = data
        sigR[i] = data

    return sigL, sigR


if __name__ == "__main__" :
    argvs = sys.argv
    curDirPath = os.path.dirname(os.path.abspath(__file__))
    wavDataPath = parentpath(__file__,1) + "/wav/millionTheater"
    millionWavPathList = glob.glob(wavDataPath + "/*.wav")
    print (curDirPath)
    print (wavDataPath)
    print(millionWavPathList)

    filedata = openFile(millionWavPathList[0], 0)
    sig = filedata[0]
    fs = filedata[1]
    L = filedata[2]

    sigList = []
    for i in millionWavPathList:
        sigList.append(openFile(i, 0)[0])

    lenSigList = len(sigList)
    #print(lenSigList)

    parentPath = parentpath(__file__,1)

    for i, sig in enumerate(sigList):

        sigL, sigR = itd(sig, fs)

        stereo = monoral2stereo(sigL, sigR)

        filename = millionWavPathList[i].split("/")[-1].split(".")[0]
        filepath = parentPath + "/output/itd/" + filename
        save(stereo, fs, 16, filepath, 2)
        #sys.exit()
