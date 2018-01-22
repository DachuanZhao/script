# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 23:40:34 2017

@author: hnjyz
"""

import numpy as np
import pandas as pd
import tushare as ts
import statsmodels.stats.anova as anova
from statsmodels.formula.api import ols


def get_ret(code):
    data = ts.get_k_data(code = str(code),
                         start = '2007-01-01',
                         end = '',
                         ktype = 'D',
                         autype = 'qfq',
                         index = True,
                         retry_count = 2,
                         pause = 0.001)
    
    data_close = data['close']
    
    data_close_ret = (data_close.shift(1) / data_close - 1).dropna()
    return data_close_ret

data = ts.get_concept_classified()

data['return']= None
x = 2   
data[data['code'] == "600122"] = x * np.ones_like(data[data['code'] == "600122"]['return'],dtype='float64')