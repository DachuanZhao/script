# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 00:16:32 2016

@author: zdc
"""

import numpy as np
import numpy.random as npr
import pandas as pd
import pandas.io.data as web
import matplotlib.pyplot as plt
%matplotlib inline

symbols = ['AAPL','MSFT','YHOO','DB','GLD']
noa = len(symbols)

data= pd.DataFrame()

for sym in symbols: 
    data[sym] = web.DataReader(sym,data_source='yahoo',end='2014-09-12')['Adj Close']
data.columns = symbols

(data / data.ix[0] * 100).plot(figsize=(8,5))

rets = np.log(data / data.shift(1)) #数据向后移一位

rets.mean() * 252#252个交易日，年化收益率

rets.cov() * 252#年化协方差矩阵

weights = npr.random(noa) #随机生成权重
weights /= np.sum(weights) #标准化权重和为1

np.sum(rets.mean() * weights ) * 252


