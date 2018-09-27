import wave
from pylab import *
import struct


def openFile(filename):
    wf = wave.open(filename , "r" )
    fs = wf.getframerate()  # サンプリング周波数
    x = wf.readframes(wf.getnframes())
    x = frombuffer(x, dtype= "int16") / 32768.0  # -1 - +1に正規化
    printWaveInfo(wf)
    wf.close()
    return x, fs, wf.getnchannels(), wf.getnframes()

def save(data, fs, bit, filename):

    data = [int(v * 32767.0) for v in data]
    data = struct.pack("h" * len(data), *data)


    w = wave.Wave_write(filename + ".wav")
    w.setnchannels(1)
    w.setsampwidth(int(bit/8))
    w.setframerate(fs)
    w.writeframes(data)
    w.close()

def printWaveInfo(wf):
    """WAVEファイルの情報を取得"""
    print ("チャンネル数:", wf.getnchannels())
    print ("サンプル幅:", wf.getsampwidth())
    print ("サンプリング周波数:", wf.getframerate())
    print ("フレーム数:", wf.getnframes())
    print ("パラメータ:", wf.getparams())
    print ("長さ（秒）:", float(wf.getnframes()) / wf.getframerate())
