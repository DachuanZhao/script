# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import pandas as pd


def fuck(df1,df_list):
    if len(df_list) == 0:
        print(df1)
        return df1
    else:
        df2 = df_list[0]        
        df1_new = df1[df1>=df2]
        df1_new[np.isnan(df1_new)] = 0
        df2_new = df2[df2>df1]
        df2_new[np.isnan(df2_new)] = 0
        fuck(df1_new+df2_new,df_list[1:])
        
df1 = pd.DataFrame([[1,2],[3,4]])
df2 = pd.DataFrame([[3,4],[1,2]])
df3 = pd.DataFrame([[5,5],[5,5]])

fuck(df1,[df2,df3])     

