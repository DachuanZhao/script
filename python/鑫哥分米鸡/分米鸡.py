# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 23:40:15 2017

@author: Administrator
"""

from statsmodels.multivariate.pca import PCA
import statsmodels.api as sm
import os.path
import pandas as pd
import numpy as np

#路径
workdir = os.path.join(r"C:\Users\Administrator\Desktop\分米鸡")
y_excel_dir = os.path.join(workdir,"SCL-90总体描述（表）.xlsx")
x_excel_dir = os.path.join(workdir,
                           "新生生活状况调查成功样本数据 161208.xlsx")
y_sheet = "各样本SCL-90总分与9因子均值得分"
x_sheet = ["原始数据","清洗"]

#读因变量
#跳过第一行
y_df = pd.read_excel(y_excel_dir,y_sheet,skiprows=[0])
#做EXCEL的人没学过数据库，用两行表示列名
_ = []
c6 = ["学院","姓名","学号","性别","手机号","生源地","SCL-90总分"]
for column,item in enumerate(y_df.columns):
    if(column < 7):
        _.append(c6[column])
    else:
        _.append(item)
y_df.columns = _

#最终需要的因变量
y_df_f = y_df.loc[:,["学号","SCL-90总分"]]

#读自变量
x_raw = pd.read_excel(x_excel_dir,x_sheet[0])	
x_clean = pd.read_excel(x_excel_dir,x_sheet[1])

#主成分分析最终需要的自变量
x_raw_pca = x_raw.iloc[:,3:]
x_clean_pca = x_clean.iloc[:,3:]



#x_raw_f主成分分析，使用相关矩阵
pca_x_raw = PCA(x_raw_pca.iloc[:,1:], standardize=True)

#前五十个因子碎石图，从结果可以看出保留4个主成分即可
pca_x_raw.plot_scree(ncomp = 50)

#4个主成分的贡献率
pca_x_raw.eigenvals[0:4].sum()/pca_x_raw.eigenvals.sum()

#主成分载荷矩阵,即4个主成分与Q3到Q121的系数
pca_x_raw.loadings.iloc[:,0:4]

#每个样本的主成分得分
pca_x_raw.scores.iloc[:,0:4]

#最终得分与主成分的系数
lamda = np.sqrt(pca_x_raw.eigenvals[0:4])
pca_x_coef = lamda / lamda.sum()
    
#最终得分
x_raw_score = np.dot(pca_x_raw.scores.iloc[:,0:4],pca_x_coef)



#x_clean_f主成分分析，使用相关矩阵
pca_x_clean = PCA(x_clean_pca.iloc[:,1:], standardize=True)

#前五十个因子碎石图，从结果可以看出保留4个主成分即可
pca_x_clean.plot_scree(ncomp = 50)

#4个主成分的贡献率
pca_x_clean.eigenvals[0:4].sum()/pca_x_clean.eigenvals.sum()

#主成分载荷矩阵,即4个主成分与Q3到Q121的系数
pca_x_clean.loadings.iloc[:,0:4]

#每个样本的主成分得分
pca_x_clean.scores.iloc[:,0:4]

#最终得分与主成分的系数
lamda = np.sqrt(pca_x_clean.eigenvals[0:4])
pca_x_coef = lamda / lamda.sum()
    
#最终得分
x_clean_score = np.dot(pca_x_clean.scores.iloc[:,0:4],pca_x_coef)



#下面开始回归
x_raw_reg = pd.DataFrame(columns=["学号","主成分得分"],
                         data=np.array([x_raw_pca.loc[:,"Q2"].tolist(),
                               x_raw_score.tolist()]).transpose())
y_x_raw_df = pd.merge(y_df_f,x_raw_reg)

#回归,F统计量0.07，回归个吊
y_x_raw_rg = sm.OLS(y_x_raw_df.loc[:,"SCL-90总分"],y_x_raw_df.loc[:,"主成分得分"])
y_x_raw_result = y_x_raw_rg.fit()
print(y_x_raw_result.summary())



x_clean_reg = pd.DataFrame(columns=["学号","主成分得分"],
                         data=np.array([x_clean_pca.loc[:,"Q2"].tolist(),
                               x_clean_score.tolist()]).transpose())
y_x_clean_df = pd.merge(y_df_f,x_clean_reg)
'''
#上面那个查询没有结果，回归个吊
y_x_clean_rg = sm.OLS(y_x_clean_df.loc[:,"SCL-90总分"],y_x_clean_df.loc[:,"主成分得分"])
y_x_clean_result = y_x_clean_rg.fit()
print(y_x_clean_result.summary())
'''

#原因分析:相关矩阵里没有大于0.5的，证明相关性很弱，所以你告诉我怎么用PCA？？？
x_raw_pca.iloc[:,1:].corr()
