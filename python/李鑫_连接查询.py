# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
filePath = r'E:\桌面'
data = pd.read_excel(filePath + '\\清洗后数据.xlsx',encoding = 'gb18030')
dataA81 = list(data['A81'].unique())

#pd.DataFrame(dataA81,index = list(range(len(dataA81))),columns = ['A81']).to_excel(filePath + "\\所有专业.xlsx")

dataA81Tran = pd.read_excel(filePath + '\\所有专业.xlsx',encoding = 'gb18030')

dataNew = pd.merge(data,dataA81Tran,left_on = 'A81',right_on = 'A81')

dataNew.to_excel(filePath + '\\最终数据.xlsx')

