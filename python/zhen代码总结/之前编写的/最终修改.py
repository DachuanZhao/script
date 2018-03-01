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

class Capital(object):
   
    def __init__(self,weight):
        '''
        position:仓位
        cost:成本
        data:数据
        N:基金的个数
        '''
        self.__position = pd.DataFrame()
        self.__cost = pd.DataFrame()
        self.__data = pd.DataFrame()
        self.__raw_data = pd.DataFrame()
        self.__weight = weight
        
    def set_data(self,
                 txtPath,
                 beginTime="2010-12-01",
                 endTime=datetime.now().strftime('%Y-%m-%d'),
                 deltaTime="Period=W;Days=Alldays"):#初始化数据
        w.start()
        fo = open(txtPath, 'r')
        capName = str(fo.read())
        fo.close()
        print(capName[0:10])
        capWind = w.wsd(str(capName),"NAV_adj",str(beginTime), str(endTime), str(deltaTime))
        cap = pd.DataFrame(np.array(capWind.Data).T,
                           index = capWind.Times,
                           columns = capWind.Codes)
        na = []
        for column in cap.columns:
            #column = '000043.OF'
            if cap[column].iloc[0] != cap[column].iloc[0]:#判断是否为nan
                na.append(column)
        self.__raw_data = cap.drop(na,axis = 1)
        
    #def set_cost(self):
        
    #def set_position(self):  
    def initialize_pc(self):
        self.__position = pd.DataFrame()
        self.__cost = pd.DataFrame()
        
    def initialize_data(self,data,raw_data,weight):
        self.__data = data
        self.__raw_data = raw_data
        self.__weight = weight
               
    def get_w(self):
        return self.__weight
        
    def get_raw_data(self):
        return self.__raw_data
        
    def get_data(self):
        return self.__data
    
    def get_position(self):
        return self.__position
    
    def get_cost(self):
        return self.__cost
    
    def get_total_cost(self):
        return self.__cost.sum(axis=1,skipna = False)
        
    def get_market_cap(self,date):
        return (self.__position.iloc[-1] * self.__data.loc[date]).sum()
        
    def select_fund_reversal(self,N,weekN):
        index = (self.__raw_data.iloc[weekN] / self.__raw_data.iloc[0] - 1).order().iloc[0:N].index
        self.__data = self.__raw_data[index]
        
    def adjust_position(self,date,w,money):
        '''
        date:日期
        w:分配金额的权重
        cash:闲置资金
        '''
        #检查date是否为时间标签，权重是否小于0，现金留存是否小于0
        if type(date) != pd.tslib.Timestamp and type(date) != datetime:
            raise ValueError('date is not pd.tslib.Timestamp or datetime.datetime')
        else:
            if w.any() <= 0:
                raise ValueError('权重小于等于0')
                print('权重小于等于0')
            else:
                if money <= 0:
                    raise ValueError('钱数小于等于0')
                    print('钱数小于等于0')
                else:
                    if len(self.__position) == 0:
                        self.__position = pd.DataFrame(np.floor(money * w / self.__data.loc[date]),
                                                      index = [date],
                                                      columns = self.__data.columns)
                        self.__position.loc[date] = np.floor(money * w / self.__data.loc[date])
                        self.__cost = pd.DataFrame(np.floor(money * w / self.__data.loc[date]),
                                                  index = [date],
                                                  columns = self.__data.columns)
                        self.__cost.loc[date] = self.__position.loc[date] * self.__data.loc[date]
                        return money - self.__cost.loc[date].sum()
                    else:
                        getMarketCap = (self.__position.iloc[-1] * self.__data.loc[date]).sum()
                        w = w / w.sum()#归一化
                        if money > getMarketCap:
                            deltaMoney = money - getMarketCap#用来加仓的钱
                            deltaPosition = np.floor((deltaMoney * w) / self.__data.loc[date])#增加的仓位
                            self.__position.loc[date] = self.__position.iloc[-1] + deltaPosition #更新仓位
                            leftMoney = money - (self.__position.loc[date] * self.__data.loc[date]).sum()#多余的钱，需要return
                            self.__cost.loc[date] = self.__cost.iloc[-1] + deltaPosition * self.__data.loc[date]#调整成本
                            return leftMoney
                        else:
                            deltaMoney = getMarketCap - money#用来减仓的钱
                            deltaPosition = np.ceil((deltaMoney * w) / self.__data.loc[date])#减少的仓位
                            self.__position.loc[date] = self.__position.iloc[-1] - deltaPosition#更新仓位
                            leftMoney = money - (self.__position.loc[date] * self.__data.loc[date]).sum()#多余的钱
                            self.__cost.loc[date] = self.__cost.iloc[-1] - deltaPosition * self.__data.loc[date]#调整成本
                            return leftMoney
                            
    def not_change_position(self,date):
        self.__position.loc[date] = self.__position.iloc[-1]
        self.__cost.loc[date] = self.__cost.iloc[-1]
    
'''
getMarketCap = (cap1.__position.iloc[-1] * self.__data.loc[date]).sum()
w = w / w.sum()#归一化
if money > getMarketCap:
    deltaMoney = money - getMarketCap#用来加仓的钱
    deltaPosition = np.floor((deltaMoney * w) / self.__data.loc[date])#增加的仓位
    self.__position.loc[date] = self.__position.iloc[-1] + deltaPosition #更新仓位
    leftMoney = money - (self.__position.loc[date] * self.__data.loc[date]).sum()#多余的钱，需要return
    self.__cost.loc[date] = self.__cost.iloc[-1] + deltaPosition * self.__position.loc[date]#调整成本
    return leftMoney
else:
    deltaMoney = getMarketCap - money#用来减仓的钱
    deltaPosition = np.ceil((deltaMoney * w) / self.__data.loc[date])#减少的仓位
    self.__position.loc[date] = self.__position.iloc[-1] - deltaPosition#更新仓位
    leftMoney = money - (self.__position.loc[date] * self.__data.loc[date]).sum()#多余的钱
    self.__cost.loc[date] = self.__cost.iloc[-1] - deltaPosition * self.__position.loc[date]#调整成本
    return leftMoney







np.floor(1000/a1.iloc[0]).T.values
a = pd.DataFrame()
a = pd.DataFrame(np.floor(1000/a1.iloc[0]),
                 index=[datetime(2010,12,5)],
                 columns=a1.columns)
a.loc[datetime(2010,12,5)] = np.floor(1000/a1.iloc[0])


pd.DataFrame(np.floor(10000 / cap1._Capital__data.loc[date]),
             index = [date],
             columns = cap1._Capital__data.columns)

cap1.get_market_cap(date)

'''

dataPath = 'C:\\Users\\Zhenvest\\Desktop\\最终回测数据\\'
targetPath = 'C:\\Users\\zdc\\Desktop\\work\\回测\\回测最终2014-2016固定Bond加入提取80%固收为6.5比82-22'
totalMoney = 10000000#总资金
selectN = 10
selectWeek = 4
openWeek = 4
cash = 0
adminiExpense = 0.06 / 4



weigt = np.ones(selectN) / selectN


cap1 = Capital(4)
cap2 = Capital(4)
cap3 = Capital(2)
cap1.set_data(dataPath + 'qdii基金.txt',beginTime="2010-12-01")
cap2.set_data(dataPath + '债券型基金.txt',beginTime="2010-12-01")
cap3.set_data(dataPath + '被动指数型基金.txt',beginTime="2010-12-01")

cap1.select_fund_reversal(selectN,selectWeek)
cap2.select_fund_reversal(selectN,selectWeek)
cap3.select_fund_reversal(selectN,selectWeek)
'''


a1 = cap1.get_raw_data()
a2 = cap2.get_raw_data()
a3 = cap3.get_raw_data()

c1 = cap1.get_data()
c2 = cap2.get_data()
c3 = cap3.get_data()

b1 = cap1.get_position()
b2 = cap2.get_position()
b3 = cap3.get_position()
d1 = cap1.get_cost()
d2 = cap2.get_cost()
d3 = cap3.get_cost()

(a1.index == a2.index).all() == True
(a2.index == a3.index).all() == True



cap1 = Capital(4)
cap2 = Capital(4)
cap3 = Capital(2)

cap1.initialize_data(c1,a1,4)
cap2.initialize_data(c2,a2,4)
cap3.initialize_data(c3,a3,2)

cap1.initialize_pc()
cap2.initialize_pc()
cap3.initialize_pc()


'''
sumW = cap1.get_w() + cap2.get_w() + cap3.get_w()
proportion = np.array([(cap1.get_w() + cap2.get_w()) / sumW,
                      (cap1.get_w() + cap2.get_w() - 0.5) / sumW],dtype = 'float16')

year = cap1.get_data().resample('12M',how = 'sum').index
yearList = []
for i in range(1,len(year)):
    yearList.append(str(year[i])[0:4])
year = []
for date in yearList:
    #date = '2011'
    for i in [3,6,9,12]:
        #i = 3
        date = date +'-' + str(i)
        year.append(cap1.get_data().loc[date].index[-1])
        date = date[0:4]
              
for date in cap1.get_data().index[openWeek:]:
    #date = cap1.get_data().index[9]
    print('date=',date)
    print('cash=',cash)
    #date = cap1.get_data().index[openWeek]
    loc = np.where(cap1.get_data().index==date)[0].sum() #返回位置
    if date < datetime(2011,2,1) and loc <= (openWeek + selectWeek - 1):
        loca = loc - 4
        print('loca+1=',loca+1)
        cash += cap1.adjust_position(date,weigt,cap1.get_w() / sumW * totalMoney / openWeek * (loca+1))
        cash += cap2.adjust_position(date,weigt,cap2.get_w() / sumW * totalMoney / openWeek * (loca+1))
        cash += cap3.adjust_position(date,weigt,cap3.get_w() / sumW * totalMoney / openWeek * (loca+1))
    else:
        marketCap = cap1.get_market_cap(date) + cap2.get_market_cap(date) + cap3.get_market_cap(date)        
        if ((cap1.get_market_cap(date) + cap2.get_market_cap(date)) / marketCap < proportion.min() or \
            (cap1.get_market_cap(date) + cap2.get_market_cap(date)) / marketCap > proportion.max()):
                marketCap = marketCap + cash
                cash = 0
                cash += cap1.adjust_position(date,weigt,marketCap * proportion.mean() / 2)
                cash += cap2.adjust_position(date,weigt,marketCap * proportion.mean() / 2)
                cash += cap3.adjust_position(date,weigt,marketCap * (1-proportion.mean()))
        else:
            cap1.not_change_position(date)
            cap2.not_change_position(date)
            cap3.not_change_position(date) 
'''
    if (pd.to_datetime(year) == date).any() == True:
        marketCap = cap1.get_market_cap(date) + cap2.get_market_cap(date) + cap3.get_market_cap(date) + cash - \
                    totalMoney * adminiExpense 
        cash = 0
        cash += cap1.adjust_position(date,weigt,marketCap * proportion.mean() / 2)
        cash += cap2.adjust_position(date,weigt,marketCap * proportion.mean() / 2)
        cash += cap3.adjust_position(date,weigt,marketCap * (1-proportion.mean()))
'''            
'''
date = cap1.get_data().index[4]

'''
a = (cap1.get_position() * cap1.get_data().iloc[openWeek:]).sum(axis = 1) /  cap1.get_cost().sum(axis = 1)
b = (cap2.get_position() * cap2.get_data().iloc[openWeek:]).sum(axis = 1) /  cap2.get_cost().sum(axis = 1) 
c = (cap3.get_position() * cap3.get_data().iloc[openWeek:]).sum(axis = 1) /  cap3.get_cost().sum(axis = 1)  

d1 = (cap1.get_position() * cap1.get_data().iloc[openWeek:]).sum(axis = 1)             
d2 = (cap2.get_position() * cap2.get_data().iloc[openWeek:]).sum(axis = 1)  
d3 = (cap3.get_position() * cap3.get_data().iloc[openWeek:]).sum(axis = 1)         
d = (d1 + d2 + d3) / totalMoney

zhenvest = pd.DataFrame()
zhenvest['qdii'] = a
zhenvest['bond'] = b
zhenvest['index'] = c
zhenvest['total'] = d

fontOptions = {'family':'SimHei',#SimHei
               'weight':'bold',
               'size':'10.0'}
axesOptions = {'unicode_minus':'False'}
plt.rc('font',**fontOptions)
plt.rc('figure',figsize=(12,7.5))
plt.rc('axes',**axesOptions)
zhenvest.plot()

               
