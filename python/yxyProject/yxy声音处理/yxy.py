# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,2,2/0.001) 
x = np.cos(2 * np.pi * t)
y = x + 0.25 * np.random.randn(1,len(t))[0]

plt.plot(t,y)#有噪声的数据

Y = np.fft.fft(y)

Y = np.abs(Y)

Y[50:(len(Y)-50)] = 0

X = np.fft.ifft(Y)

X = np.real(X)

T = np.linspace(0,2,len(X))

plt.plot(T,X)

