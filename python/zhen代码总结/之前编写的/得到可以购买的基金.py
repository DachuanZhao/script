# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import numpy.random as npr
import pandas as pd
from datetime import datetime

b = pd.read_csv('C:\\Users\\Zhenvest\\Desktop\\zdc\\回测说明\\净值表.csv',
                encoding = 'gb2312',sep='\t',index_col='时间')
                
a = pd.DataFrame(b.values,index=pd.to_datetime(b.index),columns = b.columns)


b = a['总收益率'] - a['总收益率'].shift(1)

b.hist(bins = 50)

bb = npr.normal(b.mean(),b.std(),50000)

np.percentile(bb,10)

(b < 0).sum() / len(b)

b = pd.read_csv('C:\\Users\\Zhenvest\\Desktop\\zdc\\回测说明\\指数行情序列.csv',
                encoding = 'gb2312',index_col='时间')
                
a = pd.DataFrame(b.values,index=pd.to_datetime(b.index),columns = b.columns)
a.corr()

