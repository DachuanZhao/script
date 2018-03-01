# -*- coding: utf-8 -*-
"""
Created on Fri Dec  9 14:22:26 2016

@author: Zhenvest
"""

from random import gauss, seed
import numpy as np
import pandas as pd 
import numpy.random as npr
import matplotlib.pyplot as plt

a = [1]
b = [1]
c = [1]
n = 365 * 13 
seed(1000000)
for i in range(n):
    if i < (365 * 5): 
        a.append(a[i] + 0.1 + gauss(0,1))
        b.append(b[i] + 0.03 + gauss(0.1,1))
        c.append(c[i] + 0.05 + gauss(0,1))
    elif i < (365 * 5 + 90):
        print(i)
        a.append(a[i] - 0.55 + gauss(0,1))
        b.append(b[i] - 0.3 + gauss(0,1))
        c.append(c[i] - 0.5 + gauss(0,1))
    else:
        a.append(a[i] + 0.06 + gauss(0,1))
        b.append(b[i] + gauss(0.12,1))
        c.append(c[i] + 0.04 + gauss(0.01,1))  


pd.Series(a).plot()
pd.Series(b).plot()
pd.Series(c).plot()

a = pd.Series(np.array(a),pd.date_range('1/6/2003',periods = n+1))
b = pd.Series(np.array(b),pd.date_range('1/6/2003',periods = n+1))
c = pd.Series(np.array(c),pd.date_range('1/6/2003',periods = n+1))

foo = pd.DataFrame()
foo['经典平衡型'] = c
foo['耶鲁模型'] = a
foo['前天候模型'] = b


fontOptions = {'family':'SimHei',#SimHei
               'weight':'bold',
               'size':'14.0'}
axesOptions = {'unicode_minus':'False'}
plt.rc('font',**fontOptions)
plt.rc('figure',figsize=(8,5))
plt.rc('axes',**axesOptions)
foo.plot()

foo.to_csv('C:\\Users\\Zhenvest\\Desktop\\zdc\\再平衡.csv')
