# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 14:42:55 2018

@author: Administrator
"""
import numpy as np
import matplotlib.pyplot as plt
import os.path

from sklearn.cluster import KMeans

#文件路径
file_dir = r"C:\Users\Administrator\Desktop"
#文件名
file_name = r"人文中国数据.txt"

#读取txt，文件分隔符太混乱了，只能逐行读取（摊手）
file = open(os.path.join(file_dir,file_name), 'r')
file_lines = file.readlines()
file_list = []
for num,line in enumerate(file_lines):
    #删掉第一行
    if num != 0 and num != 1:
        #删除第一列
        file_list.append(line.split()[1:])
#转换变量类型：list->array
file_arr = np.array(file_list)

#生成中心的随机种子
random_state = 170
#分类的个数
n_clusters = 5

# Incorrect number of clusters
y_pred = KMeans(n_clusters=n_clusters,
                random_state=random_state).fit_predict(file_arr)

#按照前两个变量画出散点图
plt.scatter(file_arr[:, 0], file_arr[:, 1], c=y_pred)
plt.title("Incorrect Number of Blobs")



#未完待续
import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis






