# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 15:21:17 2016

@author: zdc
"""
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    
    if 0 <= x <=2000:
        return 0
    elif 2000 < x <= 2475:
        return -(x-2000) * 0.05/(1-0.05)
    elif 2475 < x <= 3500:
        return -((x-2000) * 0.1 - 25)/(1-0.1)
    elif 3500 < x <= 3825:
        return ((x-3500) * 0.03)/(1-0.03) - ((x-2000) * 0.1 - 25)/(1-0.1)
    elif 3825 < x <= 4955:
        return ((x-3500) * 0.03)/(1-0.03) - ((x-2000) * 0.15 - 125)/(1-0.15)
    elif 4955 < x <= 6375:
        return ((x-3500) * 0.1 - 105)/(1-0.1) - ((x-2000) * 0.15 - 125)/(1-0.15)
    elif 6375 < x <= 7655:
        return ((x-3500) * 0.1 - 105)/(1-0.1) - ((x-2000) * 0.2 - 375)/(1-0.2)
    elif 7655 < x <= 11255:
        return ((x-3500) * 0.2 - 555)/(1-0.2) - ((x-2000) * 0.2 - 375)/(1-0.2)
    elif 11255 < x <= 18375:
        return ((x-3500) * 0.25 - 1005)/(1-0.25) - ((x-2000) * 0.2 - 375)/(1-0.2)
    elif 18375 < x <= 30755:
        return ((x-3500) * 0.25 - 1005)/(1-0.25) - ((x-2000) * 0.25 - 1375)/(1-0.25)
    elif 30755 < x <= 33375:
        return ((x-3500) * 0.3 - 2755)/(1-0.3) - ((x-2000) * 0.25 - 1375)/(1-0.25)
    elif 33375 < x <= 44755:
        return ((x-3500) * 0.3 - 2755)/(1-0.3) - ((x-2000) * 0.3 - 3375)/(1-0.3)
    elif 44755 < x <= 47375:
        return ((x-3500) * 0.35 - 5505)/(1-0.35) - ((x-2000) * 0.3 - 3375)/(1-0.3)
    elif 47375 < x <= 60375:
        return ((x-3500) * 0.35 - 5505)/(1-0.35) - ((x-2000) * 0.35 - 6375)/(1-0.35)
    elif 60375 < x <= 61005:
        return ((x-3500) * 0.35 - 5505)/(1-0.35) - ((x-2000) * 0.4 - 10375)/(1-0.4)
    elif 61005 < x <= 72375:
        return ((x-3500) * 0.45 - 13505)/(1-0.45) - ((x-2000) * 0.4 - 10375)/(1-0.4)
    elif x > 72375:
        return ((x-3500) * 0.45 - 13505)/(1-0.45) - ((x-2000) * 0.45 - 15375)/(1-0.45)

x = np.arange(72375)
y = np.arange(72375)

for i in range(len(x)):
    print(x[i])
    y[i] = f(x[i])
    

discontinuity_point_x = np.array([2000,2475,3500,3825,4955,6375,7655,11255,
                                  18275,30755,44755,47375,60375,61005,72375])
discontinuity_point_y = np.array([2000,2475,3500,3825,4955,6375,7655,11255,
                                  18275,30755,44755,47375,60375,61005,72375])

for i in range(len(discontinuity_point_x)):
    discontinuity_point_y[i]=f(discontinuity_point_x[i])
    

    

plt.plot(x,y,color='blue')
plt.scatter(discontinuity_point_x,discontinuity_point_y, 3, color='red')#标点
plt.plot([discontinuity_point_x,discontinuity_point_x],
         [np.zeros(len(discontinuity_point_x)),discontinuity_point_y], 
          color='blue', linewidth=0.5, linestyle="--")#划线
for i in range(len(discontinuity_point_x)):
    if i<=6:
        plt.annotate('('+str(discontinuity_point_x[i])+','+str(discontinuity_point_y[i])+')',
                             xy=(discontinuity_point_x[i],discontinuity_point_y[i]),
                             xycoords='data',xytext=(-30, max(-4*i-4,-22)),
                             textcoords='offset points',fontsize=5,
                             arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=.2"))
    elif i == len(discontinuity_point_x)-1:
        plt.annotate('('+str(discontinuity_point_x[i])+','+str(discontinuity_point_y[i])+')',
                             xy=(discontinuity_point_x[i],discontinuity_point_y[i]),
                             xycoords='data',xytext=(-30, 5),
                             textcoords='offset points',fontsize=5,
                             arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=.2"))
        
    else:
        plt.annotate('('+str(discontinuity_point_x[i])+','+str(discontinuity_point_y[i])+')',
                     xy=(discontinuity_point_x[i],discontinuity_point_y[i]),
                     xycoords='data',xytext=(+5, -max(30-2.5*i,12)),
                     textcoords='offset points',fontsize=5,
                     arrowprops=dict(arrowstyle="->",connectionstyle="arc3,rad=.2"))   
plt.grid(True)
plt.xlabel('X',fontsize='xx-large')
plt.ylabel('T',rotation='horizontal',fontsize='xx-large')
plt.title('税收冲击',fontproperties='SimHei',fontsize='xx-large')
plt.savefig('D:\\weizhenzhen.png',dpi=1000)


help(plt.plot)
help(plt.title)
help(plt.savefig)
help(plt.ylabel)
help(plt.annotate)


((60374-3500) * 0.35 - 5505)/(1-0.35) - ((60374-2000) * 0.35 - 6375)/(1-0.35)
((47376-3500) * 0.35 - 5505)/(1-0.35) - ((47376-2000) * 0.35 - 6375)/(1-0.35)