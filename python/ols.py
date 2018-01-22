# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 23:47:28 2016

@author: zdc
"""

import numpy as np
import numpy.random as npr
import pandas as pd
import matplotlib.pyplot as plt

epsilon = npr.normal(0,1,300)
x = npr.uniform(0,100,300)
y = x + epsilon

model = pd.ols(y=pd.Series(y),x=pd.Series(x))#注意转化数据类型

#help(model)

#系数和截距
model.beta

#自由度   
model.df

model.df_model#未知

model.df_resid

#统计量的值
model.f_stat

model.nobs
model.nw_lags

#P值
model.p_value

#R方
model.r2

#调整的R方
model.r2_adj

#模型的epsilon
model.resid

#均方根误差
model.rmse

#标准误差
model.std_err

model.summary
model.summary_as_matrix
model.t_stat
model.var_beta

model.y_fitted
model.y_predict

plt.plot(x,y,'r.')
ax = plt.axis()
x1 = np.linspace(ax[0],ax[1] + 0.01)
plt.plot(x1,model.beta[1] + model.beta[0] * x1,'b',lw=2)
plt.grid(True)
plt.axis('tight')