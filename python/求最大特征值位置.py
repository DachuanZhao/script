# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 20:26:54 2017

@author: hnjyz
"""

import numpy as np

#因素对比矩阵A，只需要改变矩阵A
A = np.matrix([[1,7],[2,4]])
       
#获取指标个数                                   
[m,n]=A.shape            
        
RI=[0,0,0.58,0.90,1.12,1.24,1.32,1.41,1.45,1.49,1.51]

#求判断矩阵的秩; 
R = np.linalg.matrix_rank(A)

#求判断矩阵的特征值和特征向量，V特征值，D特征向量；                   
V,D=np.linalg.eig(A)   

#最大特征值所在位置               
row, col=[np.ceil((np.argmax(D) + 1) / D.ndim),
          (np.argmax(D) + 1 - (np.ceil((np.argmax(D) + 1) / D.ndim) - 1) * D.ndim)] 

#索引从0开始
row = row - 1
col = col - 1