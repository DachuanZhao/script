# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 13:49:53 2016

@author: zdc
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dataRaw = pd.read_csv('C:\\Users\\zdc\\Desktop\\work\\债券型基金\\复权单位净值增长率和评级.csv',
                      index_col=0,encoding='gb2312')             
dataName = '复权单位净值增长率\r\n[起始交易日期] 截止日3年前\r\n[截止交易日期] 最新\r\n[单位] %'

dataRaw = dataRaw.ix[pd.notnull(dataRaw[dataName]),:]

dataN = 1#数据开始的列数-1（因为是从0开始）
investTpye=pd.Series(dataRaw.ix[:,'投资类型(二级分类)'].unique()).dropna()#基金类型
columnsName=np.array(dataRaw.columns[dataN:])
replaceNameList = ['\r','\n',' ']
histN = 20
csv=pd.DataFrame(index=investTpye)
def replaceName(x,replaceNameList):
    for i in replaceNameList:
        x=x.replace(i,'')
    return x
    
dataGroup = -((dataRaw.columns == np.str('投资类型(二级分类)')) + \
            (dataRaw.columns == np.str(dataName)) + \
            (dataRaw.columns == np.str('证券简称')))
data = dataRaw
dataTable=[]
for dataName_i in dataRaw.columns[dataGroup]:             
a=dataRaw.ix[:,datagroup].groupby(by=[dataRaw['投资类型(二级分类)'],dataRaw[dataName]])
b=pd.DataFrame(a.mean())
b=dataRaw.ix[:,datagroup]

for investTpye_i in investTpye:
    path = 'C:\\Users\\zdc\\Desktop\\work\\债券型基金'
    new_path = os.path.join(path, investTpye_i)
    if not os.path.isdir(new_path):#增加新路径
        os.makedirs(new_path)
    data = dataRaw.ix[dataRaw.ix[:,'投资类型(二级分类)']==investTpye_i,:]
    
    ('中长期纯债型基金', 13.612993)
    
    
    
    for columnsName_i in columnsName:
        investTpye_i=investTpye[0]
        columnsName_i=columnsName[0]
        outName=replaceName(columnsName_i,replaceNameList)#输出csv名称
        outNameTime = outName[(outName.find('级'))+1:]

        plt.hist(data[columnsName_i].dropna(),
                 normed = True,
                 bins=histN)#画直方图
        plt.title(outNameTime+'  平均值='+str(mu)+' '+'标准差='+str(std),
                  fontproperties='SimHei')#标题
        plt.xlabel('r,基金数量='+str(data[columnsName_i].dropna().size),
                    fontproperties='SimHei')#x轴
        plt.ylabel('概率密度',fontproperties='SimHei')#y轴
        plt.savefig('C:\\Users\\zdc\\Desktop\\work\\债券型基金\\'+
                    investTpye_i+'\\'+outName+'.png',
                    dpi=1000,
                    fontproperties='SimHei')#保存
        plt.close()