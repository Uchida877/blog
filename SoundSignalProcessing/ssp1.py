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
        sigList.append(openFile(i)[0])


    sigVB = volumeBoost(sig, fs)
    sigVB = sig / 100
    save(sigVB, fs, 16, argvs[1])

    sigSyn = synthesis(sigList)
    sigSyn = sigSyn / 100
    save(sigSyn, fs, 16, argvs[2])

    sigFast = fastForward(sig)
    sigFast = sigFast
    save(sigFast, fs, 16, argvs[3])
