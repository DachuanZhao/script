# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 18:58:42 2017

@author: hnjyz
"""
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

filepath = r'D:\python3.x\yxy'

def step1():
    samplerate = 11025
    duration = 3
    t = np.linspace(0,duration,duration * samplerate)
    amplification = 1
    sig = amplification * np.sin(2 * np.sin(2 * np.pi * 440 * t) * np.sin(2 * np.pi * t))
    print(sig)
    sf.write(filepath +'\\la440.wav',sig,samplerate)
    plt.plot(t,sig)
    
def step5():
    sig,samplerate = sf.read(filepath +'\\la440.wav')
    FFT_signal = 1 / samplerate * np.fft.rfft(sig) 
    FFT_signal2 = np.real(np.fft.irfft(FFT_signal)) * 11025
    sf.write(filepath +'\\la441.wav',FFT_signal2,samplerate)
    plt.plot(FFT_signal2)
    plt.plot(FFT_signal)
    
step1()
step5()

