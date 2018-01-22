# -*- coding: utf-8 -*-
"""
Created on Mon May 30 23:29:22 2016

@author: zdc
"""
import numpy as np
import pandas as pd

data = pd.read_table('C:\\Users\\zdc\\Desktop\\table.txt',
                     sep='\s\s',encoding = 'gb2312')

buy=data['现手'].str.endswith('↑')
sell=data['现手'].str.endswith('↓')
buysell = 1*buy + -1*sell

for i in ['↓','↑','--']:
    data['现手']=data['现手'].str.replace(i,'')
    

data['买入']=buysell
data = data.dropna(subset=['现手','笔数'],how='any')

dataselect = data[data['现手'].astype(int)*data['成交'].astype(float) > 500000]

sum(dataselect['成交'].astype(float)*dataselect['现手'].astype(int) \
*dataselect['买入'].astype(float)) \
/  sum(dataselect['现手'].astype(float))

databuy = dataselect[dataselect['买入'].astype(int) == 1]
sum(databuy['成交'].astype(float)*databuy['现手'].astype(int)) \
/  sum(databuy['现手'].astype(float))
