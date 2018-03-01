# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 13:50:10 2016

@author: Zhenvest
"""
import numpy as np

sum = 0
a = np.array([1.00 
,1.08 
,1.08 
,1.17 
,1.13 
,1.09 
,1.10 
,1.23 
,1.34 
,1.77 
,2.30 
,1.57 
,2.02 
,1.62 
,1.65 
,1.69 
,1.69 
])
for i in range(len(a)):
    if a[i] > 1.075:
        sum += (a[i] - 1.075) * 0.1 + (1.075 - 1) * 0.8
        a[i:] = a[i:] -((a[i] - 1.075) * 0.1 + (1.075 - 1) * 0.8)
    elif a[i] > 1:
        sum += (a[i] - 1) * 0.8
        a[i:] = a[i:] - (a[i] - 1) * 0.8
    if sum >= 0.06:
        x = sum - 0.06
        sum = 0.06
        a[i:] = a[i:] + x
        if a[i] > 1.075:
            a[i:] = a[i:] - (a[i] - 1.075) * 0.1
    if i%4 == 0:
        sum = 0
        
pd.Series(a).to_csv('C:\\Users\\Zhenvest\\Desktop\\图\\a.csv')
    
p