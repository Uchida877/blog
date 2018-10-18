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

def volumeBoost(sig, fs):
    for i in range(len(sig)):
        sig[i] = sig[i] * (1 + i/(fs/8))
    return sig

def synthesis(sigList):
    maxLength = 0
    tmpLength = 0
    tmpArray = []

    for i, data in enumerate(sigList):
        if len(data) > tmpLength:
            maxLength = len(data)
            tmpLength = len(data)
            index = i

    sig = np.zeros(maxLength)

    for i in sigList:
        tmp = i.tolist()
        for data in range(maxLength - len(i)):
            tmp.append(0)

        tmpArray.append(tmp)

    sig = np.array(tmpArray[0]) + np.array(tmpArray[1]) + np.array(tmpArray[2])
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


if __name__ == "__main__" :
    argvs = sys.argv
    curDirPath = os.path.dirname(os.path.abspath(__file__))
    wavDataPath = parentpath(__file__,1) + "/wav/synthesis"
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
        sigList.append(openFile(i)[0])

    print(len(sigList))
    sigSyn = synthesis(sigList)
    sigSyn = np.array(sigSyn)
    #print(sigSyn)
    sigmin = min(sigSyn)
    sigmax = max(sigSyn)
    sigSyn = nomalize(sigSyn, sigmax, sigmin, 1)
    save(sigSyn, fs, 16, argvs[1], 2)
