# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 13:43:41 2016

@author: zdc
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy.random as npr
from datetime import datetime

tableName = ['布伦特原油','恒生指数','黄金','货币基金指数','农产CFCI',
             '中债信用债总财富(总值)指数','中债总财富(总值)指数','中证800']
outputDataFrame = pd.DataFrame()
for tableName_i in tableName:
#    tableName_i='布伦特原油'
    path = 'C:\\Users\\zdc\\Desktop\\work\\资本市场收益率\\csv\\'
    dataRaw = pd.read_csv(path + tableName_i + '.csv',
                          encoding = 'gb2312',index_col = 1,parse_dates=1)
    dataRaw = dataRaw.dropna()
    outputSeries = pd.Series()
    for year in range(2005,2016+1):
        print(year)
        print(tableName_i)
        data = dataRaw[str(year)]['涨跌幅[%]']
        if len(data) == 0:
            mu = None
        else:            
            data[-1] = None
            mu = pd.to_numeric(data).sum()
        outputSeries[str(year)] = mu
    outputDataFrame[tableName_i] = outputSeries 

outputDataFrame.mean()
outputDataFrame.std()
outputDataFrame.min()
outputDataFrame.multiply()
outputDataFrame+1






pd.Series([0.9,1.1,0.9]).prod()
    
plt.plot(outputDataFrame,
         lw = 1.5)
plt.axhline(6) 
plt.legend(outputDataFrame.columns,
           prop={'family':'SimHei','size':'5'},
           loc=0) 
plt.grid(True)
plt.savefig(path+'资本市场收益率.png',
            dpi=1000,
            fontproperties='SimHei')#保存
  
pd.Series(outputDataFrame['布伦特原油'].dropna(),dtype='float64').index
type(outputDataFrame['布伦特原油'].dropna().index.min())
type(outputDataFrame['恒生指数'].dropna().index.min())
int(outputDataFrame['布伦特原油'].dropna().index.min()) - 1

for everyOutput in outputDataFrame.columns:
    print(everyOutput)
    dataUsed = outputDataFrame[everyOutput].dropna()
    plt.plot(dataUsed,
             lw = 1.5)
    plt.xlim([int(dataUsed.index.min())-1,
              int(dataUsed.index.max())+1])
    plt.axhline(6,color='black') 
    plt.title(everyOutput,
              fontproperties='SimHei') 
    plt.grid(True)
    plt.xlabel('年份',fontproperties='SimHei')
    plt.ylabel(everyOutput+'年化收益率%',fontproperties='SimHei')
    for yearUsed in dataUsed.index:
        plt.annotate('('+str(round(dataUsed[yearUsed],3))+')',
                     xy=(yearUsed,dataUsed[yearUsed]),
                     xycoords='data',xytext=(+10, +10),
                     textcoords='offset points',fontsize=6,
                     arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=.2"))
    plt.savefig(path+everyOutput+'-资本市场收益率.png',
                dpi=1000,
                fontproperties='SimHei')#保存
    plt.close()
    
help(plt.plot)
xycoords='data'

round(0.8888,3)