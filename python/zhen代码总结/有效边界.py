# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 01:44:05 2016

@author: zdc
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 17:20:39 2016

@author: zdc
"""

import pandas as pd
import numpy as np
import numpy.random as npr
import matplotlib.pyplot as plt
import os
import os.path
import scipy.optimize as sco

data = pd.read_csv('C:\\Users\\hnjyz\\Desktop\\zdc\\资产大类指数.csv',
                    encoding= 'gb2312',index_col = '时间')

rets = np.log(data / data.shift(1))
noa = len(rets.columns)#资产大类数
N = 52#一年52周
Rf = 0.025
rets.corr()
'''
蒙特卡洛模拟
'''
prets = []
pvols = []

for p in range(30000):
    weights = npr.random(noa)
    weights /= np.sum(weights)
    prets.append(np.sum(rets.mean() * weights) * N)
    pvols.append(np.sqrt(np.dot(weights.T,np.dot(rets.cov() * N,weights))))
prets = np.array(prets)
pvols = np.array(pvols)

fontOptions = {'family':'SimHei',#SimHei
               'weight':'bold',
               'size':'10.0'}
axesOptions = {'unicode_minus':'False'}
plt.rc('font',**fontOptions)
plt.rc('figure',figsize=(12,7.5))
plt.rc('axes',**axesOptions)

plt.scatter(pvols,prets,c=prets / pvols,marker='o')
plt.colorbar(label='夏普比率')
    
'''
投资组合优化
'''    
def statistics(weights):
    weights = np.array(weights)
    pret = np.sum(rets.mean() * weights) * N
    pvol = np.sqrt(np.dot(weights.T,np.dot(rets.cov() * N,weights)))
    return np.array([pret,pvol,(pret - Rf) / pvol])
    
def min_func_sharpe(weights):
    '''
    夏普指数最大化
    '''
    return -statistics(weights)[2]

cons = ({'type':'eq','fun':lambda x:np.sum(x) - 1})
bnds = tuple((0,1) for x in range(noa))

opts = sco.minimize(min_func_sharpe,noa * [1. / noa],
                    method = 'SLSQP',bounds = bnds,
                    constraints = cons)
opts['x'].round(3)

statistics(opts['x']).round(3)#预期收益率，波动率，夏普指数

def min_func_variance(weights):
    """
    最小化方差
    """
    return statistics(weights)[1] ** 2

optv = sco.minimize(min_func_variance,noa * [1. / noa,],
                    method = 'SLSQP',bounds = bnds,
                    constraints = cons)

optv['x'].round(3)
statistics(optv['x']).round(3)

"""
有效边界
"""
def min_func_port(weights):
    return statistics(weights)[1]

trets = np.linspace(0.0,statistics(opts['x'])[0],50)
tvols = []
bnds = tuple((0,1) for x in weights)
for tret in trets:
    #tret = trets[1]
    cons = ({'type':'eq',
             'fun':lambda x: statistics(x)[0] - tret},
            {'type':'eq',
             'fun':lambda x: np.sum(x) - 1})
    res = sco.minimize(min_func_port,
                       noa * [1. / noa,],
                       bounds = bnds,
                       method = 'SLSQP',
                       constraints = cons)
    tvols.append(res['fun'])
tvols = np.array(tvols)

fontOptions = {'family':'SimHei',#SimHei
               'weight':'bold',
               'size':'10.0'}
axesOptions = {'unicode_minus':'False'}
plt.rc('font',**fontOptions)
plt.rc('figure',figsize=(12,7.5))
plt.rc('axes',**axesOptions)

plt.scatter(pvols,prets,c=prets / pvols,marker='o')
plt.scatter(tvols,trets,c=trets/tvols,marker='x')
plt.plot(statistics(opts['x'])[1],statistics(opts['x'])[0],
         'r*',markersize = 15.0)
plt.plot(statistics(optv['x'])[1],statistics(optv['x'])[0],
         'y*',markersize = 15.0)
plt.colorbar(label='夏普比率')    


"""
资本市场线
"""
import scipy.interpolate as sci
ind = np.argmin(tvols)
evols = tvols[ind:]
erets = trets[ind:]
tck = sci.splrep(evols,erets)

def f(x):
    return sci.splev(x,tck,der = 0)
def df(x):
    return sci.splev(x,tck,der = 1)

def equations(p,rf = 0.025):
    eq1 = rf - p[0]
    eq2 = rf + p[1] * p[2] - f(p[2])
    eq3 = p[1] - df(p[2])
    return eq1,eq2,eq3
    
opt = sco.fsolve(equations,[0.01,0.5,0.15])#a,b,x

fontOptions = {'family':'SimHei',#SimHei
               'weight':'bold',
               'size':'10.0'}
axesOptions = {'unicode_minus':'False'}
plt.rc('font',**fontOptions)
plt.rc('figure',figsize=(12,7.5))
plt.rc('axes',**axesOptions)

plt.scatter(pvols,prets,c=(prets - 0.025) / pvols,marker = 'o')
plt.colorbar(label = '夏普比率')
plt.scatter(evols,erets,color = 'g',lw = 4.0)
cx = np.linspace(0.0,0.3)
plt.plot(cx,opt[0] + opt[1] * cx,lw = 1.5)
plt.plot(opt[2],f(opt[2]),color = 'r',marker = 'x',markersize = 15.0)
plt.grid(True)
plt.axhline(0,color = 'k',ls = '-',lw = 2.0)
plt.axvline(0,color = 'k',ls = '-',lw = 2.0)





