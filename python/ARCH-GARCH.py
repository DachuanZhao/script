# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 13:29:14 2016

@author: zdc
"""

import arch
print(dir(arch))

import datetime as dt
import pandas_datareader.data as web
st = dt.datetime(1990,1,1)
en = dt.datetime(2016,1,1)
data = web.get_data_yahoo('^GSPC', start=st, end=en)
returns = 100 * data['Adj Close'].pct_change().dropna()
figure = returns.plot()

from arch import arch_model
am = arch_model(returns)
res = am.fit(update_freq=5)
print(res.summary())

fig = res.plot(annualize='D')