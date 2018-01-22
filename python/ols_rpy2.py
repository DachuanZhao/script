# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 23:46:49 2016

@author: zdc
"""

from rpy2 import robjects
from rpy2.robjects import Formula, Environment
from rpy2.robjects.vectors import IntVector, FloatVector
from rpy2.robjects.lib import grid
from rpy2.robjects.packages import importr, data
from rpy2.rinterface import RRuntimeError
import warnings

r = robjects.r
base     = importr('base')
stats    = importr('stats')
graphics = importr('graphics')
car = importr('car')
datasets = importr('datasets')

'''
#ggplot2()通用
import math, datetime
import rpy2.robjects.lib.ggplot2 as ggplot2
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
base = importr('base')

mtcars = data(datasets).fetch('mtcars')['mtcars']

pp = ggplot2.ggplot(mtcars) + \
     ggplot2.aes_string(x='wt', y='mpg', col='factor(cyl)') + \
     ggplot2.geom_point() + \
     ggplot2.geom_smooth(ggplot2.aes_string(group = 'cyl'),
                         method = 'lm')
pp.plot()
'''


print(a)

states = base.as_data_frame(state.x77[,c('Murder','Population',
                                    'Illiteracy','Income','Frost')])
states = '''
states<- as.data.frame(state.x77[,c('Murder','Population',
                                    'Illiteracy','Income','Frost')])
'''
car.scatterplotMatrix()
#多元线性回归
states<- as.data.frame(state.x77[,c('Murder','Population',
                                    'Illiteracy','Income','Frost')])
#相关性可视化
cor(states)
library(car)
scatterplotMatrix(states,spread=F,lty.smooth=2,main='Scatter Plot Matrix')#
library(corrgram)
corrgram(states,order=T,lower.panel=panel.shade,
         upper.panel=panel.pie,text.panel=panel.txt)

fit<-lm(Murder~Population+Illiteracy+Income+Frost,data=states)
summary(fit)

#模型诊断
library(car)#正态性
qqPlot(fit,labels=row.names(states),
       id.method='identify',simulate=TRUE,main='QQ plot')

#独立性
library(car)
durbinWatsonTest(fit)

#线性
library(car)
 

#同方差性
library(car)
ncvTest(fit)
spreadLevelPlot(fit)#次幂接近1
