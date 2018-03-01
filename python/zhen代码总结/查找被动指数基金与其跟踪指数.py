# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from WindPy import *
from datetime import *
import pandas as pd
import numpy as np
import os
import os.path
import matplotlib.pyplot as plt

#打开wind数据库
w.start()

#工作路径
txtPath = r'C:\我的坚果云\代码总结'

#保存基金交易所代码的txt
capName = '\\被动指数型基金.txt'

#打开txt文件,并保存在fo中
fo = open(txtPath + capName, 'r')

#读取fo中的内容，并转化为str保存在name中
name = str(fo.read())

#关闭txt文件
fo.close()

#获取数据，index为基金交易所代码，sec_name为中文名，fund_trackindexcode为跟踪指数交易所代码
wind = w.wss(name, "sec_name,fund_trackindexcode")

#将读取的数据保存在dataframe内
data = pd.DataFrame(list(map(list,zip(*wind.Data))),
                    index = wind.Codes,
                    columns = wind.Fields)

#将跟踪指数转化为str结构
j=0
for i in data.dropna()['FUND_TRACKINDEXCODE'].unique():
    j += 1
    if i != None:
        if j == 1:
            nameStr = i + ','
        elif j != len(data.dropna()['FUND_TRACKINDEXCODE'].unique()):
            nameStr = nameStr + i + ','
        else:
            nameStr = nameStr + i
 
#读取跟踪指数代码的中文名称以及解释说明，sec_name为中文名称，repo_briefing为解释说明
nameChi = w.wss(str(nameStr),"sec_name,repo_briefing")

#保存为dataframe格式
datajoin = pd.DataFrame(list(map(list,zip(*nameChi.Data))),
                        index = nameChi.Codes,
                        columns = nameChi.Fields)

#将被动指数基金与其跟踪代码保存在一个dataframe
datafin = pd.merge(data,datajoin,
                   how='left',
                   left_on='FUND_TRACKINDEXCODE',
                   right_index=True,
                   sort = False)

#输出dataframe
datafin.to_excel('C:\\Users\\Zhenvest\\Desktop\\'+'可以购买的被动指数型基金.xlsx')
