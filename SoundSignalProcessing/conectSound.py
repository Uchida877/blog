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
    for i in sigList:
        if len(i) > tmpLength:
            maxLength = len(i)
            tmpLength = len(i)

    sig = np.zeros(maxLength)

    sig = sigList[0] + sigList[1] + sigList[2]
    return sig

def fastForward(sig):
    sigFast = []
    for i in range(0, len(sig), 2):
        sigFast.append(sig[i] / 100)

    return sigFast


def parentpath(path=__file__, f=0):
    return str('/'.join(os.path.abspath(path).split('/')[0:-1-f]))



if __name__ == "__main__" :
    argvs = sys.argv
    curDirPath = os.path.dirname(os.path.abspath(__file__))
    wavDataPath = parentpath(__file__,1) + "/output/cocktail"
    millionWavPathList = glob.glob(wavDataPath + "/*.wav")
    print (curDirPath)
    print (wavDataPath)
    print(millionWavPathList)

    filedata = openFile(millionWavPathList[0])
    sig = filedata[0]
    fs = filedata[1]
    channel = filedata[2]

    sigList = []
    z = []
    y = np.zeros(fs*4)
    for i in millionWavPathList:
        y = np.hstack([x,x])
        sigList.append(openFile(i)[0])
    print(sigList)
