# -*- coding: utf-8 -*-
"""
Spyder Editor
hnjyzdc

"""
from WindPy import *
from datetime import *
import pandas as pd
import numpy as np
import os
import os.path
import matplotlib.pyplot as plt

#定义一个capital，用来保存资产大类：债券型基金，被动指数基金，和其他
class Capital(object):
    

    
    def __init__(self,weight):
        '''
        position:仓位，index是时间，columns是基金代码
        cost:成本，index是时间，columns是基金代码
        data:数据，index是时间，columns是基金代码
        raw_data：所有可买基金的数据，index是时间，columns是基金代码
        N：每种资产大类的份数，总共按10份算
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
                 deltaTime="Period=W;Days=Alldays"):
        '''
        函数作用：
        初始化数据，剔除基金的数据，最终输出原始数据
        
        txtPath：保存基金名称txt的路径,注意：txt中基金代码需要用逗号分隔
        beginTime：开始提取数据的时间，默认为"2010-12-01"
        endTime：停止提取数据的时间，默认为最新日期
        deltaTime：时间间隔，默认为周
        '''
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

        

    #def set_position(self):  
    def initialize_pc(self):
        '''
        函数作用：初始化position和cost,用来避免Wind数据库网络繁忙时得重新运行代码
        '''
        self.__position = pd.DataFrame()
        self.__cost = pd.DataFrame()
 
        
        
    def initialize_data(self,data,raw_data,weight):
        '''
        函数作用：初始化data,raw_data和weight
        '''
        self.__data = data
        self.__raw_data = raw_data
        self.__weight = weight

        
               
    def get_w(self):
        '''
        函数作用：获得权重w
        '''
        return self.__weight
 
     
        
    def get_raw_data(self):
        '''
        函数作用：获得初始数据
        '''
        return self.__raw_data
 
     
        
    def get_data(self):
        '''
        函数作用：获得挑选后的基金的数据
        '''
        return self.__data
 
      
        
    def get_position(self):
        '''
        函数作用：获得挑选后的基金的数据
        '''
        return self.__position
   
     
        
    def get_cost(self):
        '''
        函数作用：获得cost持仓成本的时间序列
        '''
        return self.__cost
  
        
        
    def get_total_cost(self):
        '''
        函数作用：获得总成本的时间序列
        '''
        return self.__cost.sum(axis=1,skipna = False)
    
        
        
    def get_market_cap(self,date):
        '''
        函数作用：获得时间结点date的总市值
        '''
        return (self.__position.iloc[-1] * self.__data.loc[date]).sum()
        
        
        
    def select_fund_reversal(self,N,weekN):
        '''
        函数作用：初始化data，策略为根据开始提取数据时间一直到第weekN周的收益率进行晒圈
        ，选取排名最靠后的N支
        
        N：挑选的基金个数
        weekN：业绩计算截至周数
        '''
        index = (self.__raw_data.iloc[weekN] / self.__raw_data.iloc[0] - 1).order().iloc[0:N].index
        self.__data = self.__raw_data[index]
        
        
        
    def adjust_position(self,date,w,money):
        '''
        函数作用：调仓函数，会返回调仓之后剩余的cash
        
        date:日期
        w:分配金额的权重
        money：资产大类需要调整到多少钱
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
        '''
        函数作用：不调仓
        '''        
        self.__position.loc[date] = self.__position.iloc[-1]
        self.__cost.loc[date] = self.__cost.iloc[-1]
  
        

        
        
#回测开始
#设置参数

#总资金
totalMoney = 10000000

#建仓周数
openWeek = 4

#初始闲置资金
cash = 0

#每年提取的比例
adminiExpense = 0.06 / 4

#初始化权重
weight = np.ones(selectN) / selectN

#创建三类资产
cap1N = 2
cap2N = 6
cap3N = 2

cap1 = Capital(cap1N)
cap2 = Capital(cap2N)
cap3 = Capital(cap3N)


#初始化数据
dataPath = 'C:\\我的坚果云\\研究员资料\\最终回测数据\\'
targetPath = 'C:\\Users\\Zhenvest\\Desktop\\代码总结\\'
cap1.set_data(dataPath + '混合型基金.txt',beginTime="2012-01-01")
cap2.set_data(dataPath + '债券型基金.txt',beginTime="2012-01-01")
cap3.set_data(dataPath + '被动指数型基金.txt',beginTime="2012-01-01")

#根据2012年的年收益挑选基金
#2012年数据提取了多少周
selectWeek = len(cap1.get_raw_data()['2012'])

#挑选基金数
selectN = cap1N + cap2N + cap3N

cap1.select_fund_reversal(selectN,selectWeek)
cap2.select_fund_reversal(selectN,selectWeek)
cap3.select_fund_reversal(selectN,selectWeek)
'''
防止错误时的一些备用函数
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

cap1 = Capital(2)
cap2 = Capital(6)
cap3 = Capital(2)

cap1.initialize_data(c1,a1,2)
cap2.initialize_data(c2,a2,6)
cap3.initialize_data(c3,a3,2)

cap1.initialize_pc()
cap2.initialize_pc()
cap3.initialize_pc()
'''

#获得总份数，一般为10
sumW = cap1.get_w() + cap2.get_w() + cap3.get_w()

#获得资产1和2总和的配置比例上下限，即0.75-0.8
proportion = np.array([(cap1.get_w() + cap2.get_w()) / sumW,
                       (cap1.get_w() + cap2.get_w() - 0.5) / sumW],dtype = 'float16')

#获得每一年比较数据的时间
year = cap1.get_data().resample('12M',how = 'sum').index

#用来保存时间
yearList = []

#保存回测年份到yearList
for i in range(1,(len(year) - np.int(selectWeek / 52))):
    yearList.append(str(year[i])[0:4])

#保存每季度末的时间到year    
year = []
for date in yearList:
    #date = '2011'
    for i in [3,6,9,12]:
        #i = 3
        date = date +'-' + str(i)
        year.append(cap1.get_data().loc[date].index[-1])
        date = date[0:4]
        
        
#正式开始回测
#因为提取了2012年的数据，所以从selectWeek开始提取
for date in cap1.get_data().index[selectWeek:]:
    #date = cap1.get_data().index[4]
    print('date=',date)
    print('cash=',cash)
    #date = cap1.get_data().index[openWeek]
    loc = np.where(cap1.get_data().index==date)[0].sum() #返回位置
    #判断是否建仓完成
    if date < cap1.get_data().index[(selectWeek + openWeek)] and loc < (openWeek + selectWeek):
        loca = loc - selectWeek
        print('loca+1=',loca+1)
        cash += cap1.adjust_position(date,weight,cap1.get_w() / sumW * totalMoney / openWeek * (loca+1))
        cash += cap2.adjust_position(date,weight,cap2.get_w() / sumW * totalMoney / openWeek * (loca+1))
        cash += cap3.adjust_position(date,weight,cap3.get_w() / sumW * totalMoney / openWeek * (loca+1))
    else:
        #获得总成本
        marketCap = cap1.get_market_cap(date) + cap2.get_market_cap(date) + cap3.get_market_cap(date)
        #判断是否需要再平衡        
        if ((cap1.get_market_cap(date) + cap2.get_market_cap(date)) / marketCap < proportion.min() or \
            (cap1.get_market_cap(date) + cap2.get_market_cap(date)) / marketCap > proportion.max()):
                marketCap = marketCap + cash
                cash = 0
                cash += cap1.adjust_position(date,weight,marketCap * proportion.mean() / 2)
                cash += cap2.adjust_position(date,weight,marketCap * proportion.mean() / 2)
                cash += cap3.adjust_position(date,weight,marketCap * (1-proportion.mean()))
        else:
            #不许要再平衡，就不改变仓位
            cap1.not_change_position(date)
            cap2.not_change_position(date)
            cap3.not_change_position(date)
    #每季度末提取之后，再进行调仓
    if (pd.to_datetime(year) == date).any() == True:
        marketCap = cap1.get_market_cap(date) + cap2.get_market_cap(date) + cap3.get_market_cap(date) + cash - \
                    totalMoney * adminiExpense 
        cash = 0
        cash += cap1.adjust_position(date,weight,marketCap * proportion.mean() / 2)
        cash += cap2.adjust_position(date,weight,marketCap * proportion.mean() / 2)
        cash += cap3.adjust_position(date,weight,marketCap * (1-proportion.mean()))


          
'''
date = cap1.get_data().index[4]

'''
a = (cap1.get_position() * cap1.get_data().iloc[(selectWeek):]).sum(axis = 1) /  cap1.get_cost().sum(axis = 1)
b = (cap2.get_position() * cap2.get_data().iloc[(selectWeek):]).sum(axis = 1) /  cap2.get_cost().sum(axis = 1) 
c = (cap3.get_position() * cap3.get_data().iloc[(selectWeek):]).sum(axis = 1) /  cap3.get_cost().sum(axis = 1)  

d1 = (cap1.get_position() * cap1.get_data().iloc[(selectWeek):]).sum(axis = 1)             
d2 = (cap2.get_position() * cap2.get_data().iloc[(selectWeek):]).sum(axis = 1)  
d3 = (cap3.get_position() * cap3.get_data().iloc[(selectWeek):]).sum(axis = 1)    
     
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
(zhenvest.iloc[openWeek:]-1).plot()

e = (zhenvest.iloc[openWeek:]-1)
f = a.resample('Q-DEC',how='last',closed='left')
f.to_csv(targetPath + '2013开始回测数据262.csv')

(zhenvest.iloc[openWeek:]-1).resample('Q-DEC',how='sum',closed='left') 





for data in [bondFundsData,indexFundsData]:
    #data = indexFundsData
    #i = 2
    if (i == 1):
        name = '债券型基金'
        i += 1
    else:
        name = '被动指数型基金'
    rets = np.log(data / data.shift(1))#周收益率序列
    mu = (data.ix[-1] / data.ix[0]) ** (1 /  len(data.index)) - 1
    rf = 0.025
    noa = len(rets.columns)
    #cov = bondFundsDataRets.cov()
    
    prets = []
    pvols = []
    for p in range(4 ** (noa-1)):
        print(p)
        weights = npr.rand(noa)
        weights /= np.sum(weights)
        prets.append(np.sum(mu * 52 * weights))
        pvols.append(np.sqrt(np.dot(weights.T,np.dot(rets.cov() * 52,weights))))
    #type(bondFundsData.ix[1,1])
    #help(bondFundsData.cov())
    prets = np.array(prets)
    pvols = np.array(pvols)
    
    fontOptions = {'family':'SimHei',#SimHei
                   'weight':'bold',
                   'size':'10.0'}
    axesOptions = {'unicode_minus':'False'}
    plt.rc('font',**fontOptions)
    plt.rc('figure',figsize=(8,5))
    plt.figure(figsize=(8,4))
    plt.scatter(pvols,prets,c=(prets - rf) / pvols,marker = 'o')
    plt.grid(True)
    plt.xlabel('预期波动性')
    plt.ylabel('预期收益')
    plt.colorbar(label='夏普比率')
    
    def statistics(weights,rf=0.05):
        '''返回投资组合估计
        
        参数：
        ======
        weights:向量，不同债券在投资组合中的权重
        Rf:float,无风险年利率
        
        返回值：
        ======
        pret:float
            预期的投资组合收益
        pvol:float
            预期的波动率
        (pret - Rf) / pvol:float
            夏普比率
        '''
        weights = np.array(weights)
        pret = np.sum(mu * 52 * weights)
        pvol = np.sqrt(np.dot(weights.T,np.dot(rets.cov() * 52,weights)))
        return np.array([pret,pvol,(pret - rf) / pvol])
    
    import scipy.optimize as sco
    
    def minFunctionShape(weights):
        return -statistics(weights)[2]
    
    opts = sco.minimize(minFunctionShape,
                        noa * [1. / noa,],
                        method='SLSQP',
                        bounds = tuple((0,1) for x in range(noa)),
                        constraints = ({'type':'eq','fun':lambda x: np.sum(x) - 1}))
    opts['x'].round(3)
    statistics(opts['x']).round(3)
    
    def minFunctionVariance(weights):
        return statistics(weights)[1] ** 2
     
       
    optv = sco.minimize(minFunctionVariance,
                        noa * [1. / noa,],
                        method='SLSQP',
                        bounds = tuple((0,1) for x in range(noa)),
                        constraints = ({'type':'eq','fun':lambda x: np.sum(x) - 1}))
    optv['x'].round(3)
    statistics(optv['x']).round(3)
    
    
    
    #有效边界
    def minfunctionPort(weights):
        return statistics(weights)[1]
        
    trets = np.linspace(prets.min(),prets.max(),20)
    tvols = []
    for tret in trets:
        print(tret)
        cons = ({'type':'eq','fun':lambda x: statistics(x)[0] - tret},
                {'type':'eq','fun':lambda x: np.sum(x) - 1})
        res = sco.minimize(minfunctionPort,
                           noa * [1. / noa,],
                           method='SLSQP',
                           bounds = tuple((0,1) for x in range(noa)),#
                           constraints = cons)
        tvols.append(res['fun'])
    tvols = np.array(tvols)
    
    fontOptions = {'family':'SimHei',#SimHei
                   'weight':'bold',
                   'size':'10.0'}
    axesOptions = {'unicode_minus':'False'}
    plt.rc('font',**fontOptions)
    plt.rc('figure',figsize=(8,5))
    plt.rc('axes',**axesOptions)
    plt.figure(figsize=(8,4))
    plt.scatter(pvols,prets,c=(prets-rf) / pvols,marker = 'o')
    plt.scatter(tvols,trets,c=(trets-rf) / tvols,marker = 'x')
    plt.plot(statistics(opts['x'])[1],statistics(opts['x'])[0],'r*',markersize = 15.0)
    plt.plot(statistics(optv['x'])[1],statistics(optv['x'])[0],'y*',markersize = 15.0)
    '''
    start = int(min(pvols.min(),tvols.min()) / 0.05) * 0.05
    num = int((max(pvols.max(),tvols.max()) - start)  / 0.05)  + 2
    yticks = np.linspace(start=start,
                         stop=start + 0.05 * (num-1),
                         num=num)
    plt.yticks(yticks,["%.0f%%" % number for number in (yticks * 100)])
    '''
    plt.grid(True)
    title = '有限边界，夏普比率最大、波动率最小分别为：(' + str(round(statistics(opts['x'])[1],3)) + ',' + \
            str(round(statistics(opts['x'])[0],3)) + '),(' + str(round(statistics(optv['x'])[1],3)) + ',' + \
            str(round(statistics(optv['x'])[0],3)) + ')'
    plt.title(title)
    plt.xlabel('预期波动性')
    plt.ylabel('预期收益')
    plt.colorbar(label='夏普比率')
    plt.savefig(Targetpath + '\\' + name + '有效边界线.png',
                dpi=1000,
                bbox_inches = 'tight')#保存
    plt.close() 
    
    
    import scipy.interpolate as sci
    ind = np.argmin(tvols)
    evols = tvols[ind:]
    erets = trets[ind:]
    tck = sci.splrep(evols,erets)
    
    def f(x):
        return sci.splev(x,tck,der=0)
        
    def df(x):
        return sci.splev(x,tck,der=1)
    
    def equations(p,Rf=rf):
        eq1 = Rf - p[0]
        eq2 = Rf + p[1] * p[2] - f(p[2])
        eq3 = p[1] - df(p[2])
        return eq1,eq2,eq3
    
    opt = sco.fsolve(equations,[rf,(statistics(optv['x'])[0] - rf) / statistics(optv['x'])[1],statistics(optv['x'])[1]])
    
    np.round(equations(opt),6)
    
    fontOptions = {'family':'SimHei',#SimHei
                   'weight':'bold',
                   'size':'16.0'}
    axesOptions = {'unicode_minus':'False'}
    plt.rc('font',**fontOptions)
    plt.rc('figure',figsize=(8,5))
    plt.figure(figsize=(8,4))
    plt.scatter(pvols,prets,c=(prets-rf) / pvols,marker = 'o')
    plt.plot(evols,erets,'g',lw=4.0)
    '''
    start = int(min(pvols.min(),tvols.min()) / 0.05) * 0.05
    num = int((max(pvols.max(),tvols.max()) - start)  / 0.05)  + 2
    yticks = np.linspace(start=start,
                         stop=start + 0.05 * (num-1),
                         num=num)
    plt.yticks(yticks,["%.0f%%" % number for number in (yticks * 100)])
    '''
    cx = np.linspace(0.0,pvols.max())
    plt.plot(cx,opt[0] + opt[1] * cx,lw=1.5)
    plt.plot(opt[2],f(opt[2]),'r*',markersize = 15.0)
    plt.grid(True)
    plt.axhline(0,color = 'k',ls='-',lw=2.0)
    plt.axvline(0,color = 'k',ls='-',lw=2.0)
    title = '资本市场线,切点为：(' + str(round(float(opt[2]),3)) + ',' + str(round(float(f(opt[2])),3)) + ')'
    plt.title(title)
    plt.xlabel('预期波动性')
    plt.ylabel('预期收益')
    plt.colorbar(label='夏普比率')  
    plt.savefig(Targetpath + '\\' + name + '资本市场线.png',
                dpi=1000,
                bbox_inches = 'tight')#保存
    plt.close()           
