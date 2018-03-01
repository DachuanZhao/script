# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 14:21:47 2017

@author: Zhenvest
"""

from WindPy import *
from datetime import *
import time
import pandas as pd
import numpy as np
import os
import os.path
import matplotlib.pyplot as plt

#打开wind数据库
w.start()

#工作路径
txt_path = r'C:\我的坚果云\代码总结'
output_path = r'C:\我的坚果云\代码总结\基金一级池'


#当前日期
current_time = time.strftime('%Y%m%d',time.localtime(time.time()))
delta_time = 366 * 24 * 60 * 60
begin_time = time.strftime('%Y%m%d',time.localtime(time.time() - delta_time))

#新建一个excel
writer = pd.ExcelWriter(output_path + '\\一级池.xlsx')

name_list = ['qdii基金','被动指数型基金','混合型基金','货币市场型基金','另类投资基金','债券型基金']
#保存基金交易所代码的txt
for fund_name in name_list:
    cap_name = '\\' + fund_name + '.txt'
    
    en_to_ch = {'FUND_FULLNAME':'基金名称',
                'FUND_EXISTINGYEAR':'成立年限',
                'FUND_PTMYEAR':'基金存续期',
                'FUND_PTMDAY':'剩余存续期',
                'FUND_BENCHMARK':'业绩比较标准', 
                'FUND_BENCHINDEXCODE':'基准指数代码',
                'FUND_INVESTOBJECT':'投资目标',
                'FUND_INVESTSCOPE':'投资范围',
                'FUND_INVESTMENTREGION':'投资区域',
                'FUND_INVESTINGREGIONDESCRIPTION':'主要投资区域说明',
                'FUND_OPERATEPERIOD_CLS':'封闭运作期',
                'EXPECTEDYIELD':'预期收益率（文字）',
                'FUND_SETUPDATE':'基金成立日',
                'FUND_MATURITYDATE':'基金到期日',
                'FUND_EXPECTEDOPENDAY':'预计下期开放日',
                'FUND_TYPE':'基金类型', 
                'FUND_FIRSTINVESTTYPE':'投资类型（一级分类）',
                'FUND_INVESTTYPE':'投资类型',
                'FUND_MANAGEMENTFEERATIO':'管理人管理费率',
                'FUND_CUSTODIANFEERATIO':'托管费率',
                'FUND_SALEFEERATIO':'销售服务费率',
                'FUND_SUBSCRIPTIONFEE':'认购费率',
                'FUND_PURCHASEFEE':'申购费率',
                'FUND_REDEMPTIONFEE':'赎回费率',
                'FUND_FEEDISCOUNTORNOT':'是否费率优惠',
                'FUND_DQ_STATUS':'申购赎回状态',
                'FUND_PREDFUNDMANAGER':'基金经理（历任）',
                'NAV_ADJ_RETURN':'复权单位净值增长率' + begin_time + '至今',
                'PEER_FUND_AVG_RETURN_PER':'同类基金区间平均排名',
                'FUND_THIRDPARTYFUNDTYPE':'银河基金分类'}
    
    #打开txt文件,并保存在fo中
    fo = open(txt_path + cap_name, 'r')
    
    #读取fo中的内容，并转化为str保存在name中
    name = str(fo.read())
    
    #关闭txt文件
    fo.close()
    
    #获取所有的数据，fund_dq_status为申购赎回状态，ED-90TD为当前日期往前推90个交易日
    wind = w.wsd(name, "fund_dq_status", "ED-90TD", "2017-02-13", "Period=W;PriceAdj=F")
    
    #保存在dataframe里
    data = pd.DataFrame(list(map(list,zip(*wind.Data))),
                        index = wind.Times,
                        columns = wind.Codes)
    
    #将不是开放申购的基金剔除，保存在name_list
    name_list = ','.join(data[(data == '开放申购|开放赎回')].dropna(axis = 1).columns)
    
            
    #获取数据
    wind = w.wss(name_list, "fund_fullname,fund_existingyear,fund_ptmyear,fund_ptmday,fund_benchmark,fund_benchindexcode,fund_investobject,fund_investscope,fund_investmentregion,fund_investingregiondescription,fund_operateperiod_cls,expectedyield,fund_setupdate,fund_maturitydate,fund_expectedopenday,fund_type,fund_firstinvesttype,fund_investtype,fund_thirdpartyfundtype,fund_managementfeeratio,fund_custodianfeeratio,fund_salefeeratio,fund_subscriptionfee,fund_purchasefee,fund_redemptionfee,fund_feediscountornot,fund_dq_status,fund_predfundmanager,NAV_adj_return",
                 "ratingAgency=2;" + \
                 "chargesType=0;tradeDate=" + current_time + \
                 ";startDate=" + begin_time + ";endDate=" + current_time)
    
    #处理列名
    windcolumns = wind.Fields
    
    for i in range(len(windcolumns)):
        windcolumns[i] = en_to_ch[windcolumns[i]]
        
    #以dataframe格式保存数据在data中
    data = pd.DataFrame(list(map(list,zip(*wind.Data))),
                        index = wind.Codes,
                        columns = windcolumns)
    
    data['基金到期日'][data['基金到期日'] == '1899-12-30 00:00:00.005000'] = None
    data['预计下期开放日'][data['预计下期开放日'] == '1899-12-30 00:00:00.005000'] = None
        
    #筛选一直开放的基金
    data_can_buy = data[data[en_to_ch['FUND_DQ_STATUS']]=='开放申购|开放赎回']
    
    data_can_buy_dropna = data_can_buy.dropna(axis = 1 , how = 'all')
    
    data_can_buy_dropna.to_excel(writer,fund_name)
    
writer.save()