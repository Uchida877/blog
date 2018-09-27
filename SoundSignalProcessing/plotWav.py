# coding: utf-8
import sys
sys.path.append('../common')  # 親ディレクトリのファイルをインポートするための設定
import wave
from pylab import *
import os
import glob
from sound import *
import numpy as np
import matplotlib.pyplot as plt

def plotWav(filename):
    wf = wave.open(filename  , "r" )
    buf = wf.readframes(wf.getnframes())

    # バイナリデータを整数型（16bit）に変換
    data = np.frombuffer(buf, dtype="int16")

    # グラフ化
    plt.plot(data)
    plt.grid()
    plt.show()

if __name__ == "__main__" :
    argvs = sys.argv

    plotWav(argvs[1])
