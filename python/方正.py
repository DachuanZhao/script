# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 13:02:54 2018

@author: Administrator
"""

# import module
import cx_Oracle
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
import sys
import os.path
import configparser

def sql_to_df(link,sql):
    try:
        db = cx_Oracle.connect(link)
    # 将异常捕捉，然后e就是抛异常的具体内容
    except Exception as e:  
        print(e)
    else:
        # create cursor
        cr = db.cursor()               
        # execute sql
        cr.execute(sql)     
        # fetch data
        col_name = [elem[0] for elem in cr.description]
        data_tru = cr.fetchall()
        data = pd.DataFrame(columns = col_name,
                            data = data_tru)
        if ("INIT_DATE" in data.columns):
            print(data["INIT_DATE"])
            data["INIT_DATE"] = pd.to_datetime(data["INIT_DATE"],format='%Y%m%d')
            print(data["INIT_DATE"])
            data = data.set_index("INIT_DATE")
        cr.close()
        db.close()
        return data

#找出最大连续子序和
def find_max_sub_list(series):
    maxsum = 0
    maxtmp = 0
    #begin = 0
    #end = 0
    for my_iter,value in enumerate(series):
        if maxtmp <= 0:
            maxtmp = value
            #begin = i
        else:
            maxtmp += value
        if (maxtmp > maxsum):
            maxsum = maxtmp
            #end = i
        #print("maxsum:", maxsum, " maxtmp:", maxtmp,"begin",begin,"end",end)
    return maxsum
    

if __name__ == '__main__':
    #先从本地读取，否则就连接数据库
    client_id = "10000097"
    begin_date = "20180101"
    end_date = "20180131"
    input_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    output_path = input_path
    print("当前的工作路径为：",output_path)
    try:
        fundjour_data = pd.read_csv(os.path.join(input_path,"fundjour.csv"))
        furisktotal_data = pd.read_csv(os.path.join(input_path,"furisktotal_data.csv"))
        fuholddrop_data = pd.read_csv(os.path.join(input_path,"fuholddrop_data.csv"))
    except:
        print("oralce客户端版本：",cx_Oracle.clientversion())
        print("cx_Oralce版本：",cx_Oracle.__version__)
        # connect oracle database
        config = configparser.ConfigParser()
        config.read(os.path.join(input_path,"config.ini"))
        ipaddr = config["oracle"]["ipaddr"]
        username = config["oracle"]["username"]
        password = config["oracle"]["password"]
        oracle_port = config["oracle"]["oracle_port"]
        service_name = config["oracle"]["service_name"]   
        link = username+"/"+password+"@"+ipaddr+":"+oracle_port+"/"+service_name
        # 编辑sql语句
        #出入金；OCCUR_BALANCE：发生金额，POST_BALANCE:后资金额
        fundjour_sql = " ".join(
                ("select CLIENT_ID,INIT_DATE,OCCUR_BALANCE,POST_BALANCE",
                 'from hs_his.his_fundjour',
                 'where client_id =',client_id,
                 'and init_date between',begin_date,'and',end_date,
                 'order by INIT_DATE'))
        #权益；BEGIN_TOTAL_BALANCE：客户上一日权益，TOTAL_BALANCE：客户当前权益
        furisktotal_sql = " ".join(
                ("select CLIENT_ID,INIT_DATE,BEGIN_TOTAL_BALANCE,TOTAL_BALANCE",
                 "from hs_his.his_furisktotal",
                 'where client_id =',client_id,
                 'and init_date between',begin_date,'and',end_date,
                 'order by INIT_DATE'))
        #手续费；TOTAL_FARE:手续费，DROP_INCOME：平仓盯日盈亏
        fuholddrop_sql = " ".join(
                ("select CLIENT_ID,INIT_DATE,TOTAL_FARE,DROP_INCOME",
                 "from hs_his.his_fuholddrop",
                 'where client_id =',client_id,
                 'and init_date between',begin_date,'and',end_date,
                 'order by INIT_DATE'))        
        fundjour_data = sql_to_df(link,fundjour_sql)
        furisktotal_data = sql_to_df(link,furisktotal_sql)
        fuholddrop_data = sql_to_df(link,fuholddrop_sql)
        
        #保存csv到本地
        fundjour_data.to_csv(os.path.join(input_path,"fundjour.csv"))
        furisktotal_data.to_csv(os.path.join(input_path,"furisktotal_data.csv"))
        fuholddrop_data.to_csv(os.path.join(input_path,"fuholddrop_data.csv"))
    else:
        pass
    finally:
        #聚合两个数据库到天
        fundjour_data_gb =  fundjour_data.groupby("INIT_DATE").sum()
        fuholddrop_data_gb = fuholddrop_data.groupby("INIT_DATE").sum()
     
        #用series存储
        results = pd.Series()
        results["开始日期"] = begin_date
        results["结束日期"] = end_date
        results["周期：天"] = (datetime.datetime.strptime(end_date,"%Y%m%d") \
            - datetime.datetime.strptime(begin_date,"%Y%m%d")).days
        results["期初资金"] = furisktotal_data["BEGIN_TOTAL_BALANCE"][furisktotal_data.index.min()]
        results["期末资金"] = furisktotal_data["BEGIN_TOTAL_BALANCE"][furisktotal_data.index.max()]
        results["累计入金"] = (fundjour_data["OCCUR_BALANCE"][fundjour_data["OCCUR_BALANCE"]>0]).sum()
        results["累计出金"] = (fundjour_data["OCCUR_BALANCE"][fundjour_data["OCCUR_BALANCE"]<0]).sum()
        results["最低资金额度"] = min(furisktotal_data["BEGIN_TOTAL_BALANCE"].min(),
               furisktotal_data["TOTAL_BALANCE"].min())
        results["最高资金额度"] = max(furisktotal_data["BEGIN_TOTAL_BALANCE"].max(),
               furisktotal_data["TOTAL_BALANCE"].max())
        results["最大日亏损率"] = (fuholddrop_data_gb["DROP_INCOME"] / furisktotal_data["TOTAL_BALANCE"]).min()
        results["最大日收益率"] = (fuholddrop_data_gb["DROP_INCOME"] / furisktotal_data["TOTAL_BALANCE"]).max()
        results["获利总额"] = fuholddrop_data["DROP_INCOME"].sum()
        results["交易手续费"] = fuholddrop_data["TOTAL_FARE"].sum()
        results["净收益率"] = ((fuholddrop_data_gb["DROP_INCOME"] - fuholddrop_data_gb["TOTAL_FARE"]) \
            / furisktotal_data["TOTAL_BALANCE"]).sum()
        results["净利总额"] = (fuholddrop_data_gb["DROP_INCOME"] - fuholddrop_data_gb["TOTAL_FARE"]).sum()
        results["交易笔数"] = fuholddrop_data.index.size
        results["盈利笔数"] = (fuholddrop_data["DROP_INCOME"] > 0).sum()
        results["持平笔数"] = (fuholddrop_data["DROP_INCOME"] == 0).sum()
        results["亏损笔数"] = (fuholddrop_data["DROP_INCOME"] < 0).sum()
        results["正确率"] = results["盈利笔数"] / results["交易笔数"]
        results["持平率"] = results["持平笔数"] / results["交易笔数"]
        results["亏损率"] = results["亏损笔数"] / results["交易笔数"]
        results["单笔最大盈利"] = fuholddrop_data["DROP_INCOME"].max()
        results["单笔最大亏损"] = fuholddrop_data["DROP_INCOME"].min()    
        results["最大回撤率"] = -find_max_sub_list(
                (fuholddrop_data_gb["DROP_INCOME"] - fuholddrop_data_gb["TOTAL_FARE"]) \
                 / -furisktotal_data["TOTAL_BALANCE"])
        results["平均收益风险比"] = fuholddrop_data["DROP_INCOME"].mean() / fuholddrop_data["DROP_INCOME"].std()
        results["平均每笔盈利"] = (fuholddrop_data["DROP_INCOME"][fuholddrop_data["DROP_INCOME"] > 0]).sum() \
            / results["交易笔数"]
        results["平均每笔亏损"] = (fuholddrop_data["DROP_INCOME"][fuholddrop_data["DROP_INCOME"] < 0]).sum() \
            / results["交易笔数"]
        results.to_csv(os.path.join(output_path,"表格.csv"))
        
        
        
        #作图的一些参数
        #字体，加粗，字号，
        fontOptions = {'family':'SimHei',#SimHei
                       'weight':'bold',
                       'size':'20.0'}
        #显示负号
        axesOptions = {'unicode_minus':'False'}
        plt.rc('font',**fontOptions) 
        plt.rc('axes',**axesOptions)
        #图片大小
        plt.rc('figure',figsize=(13.66*1.5,7.68*1.5))
        
        
        #下面开始画出入金图
        #禁止x轴使用科学计数法，x轴标签
        plt.ticklabel_format(style='plain',axis='x',useOffset=False)
        plt.xticks(fundjour_data_gb.index,rotation=90)
        #标题
        plt.title("出入金统计")
        #做条形图
        plt.bar(fundjour_data_gb.index[fundjour_data_gb["OCCUR_BALANCE"]>0],
                fundjour_data_gb["OCCUR_BALANCE"][fundjour_data_gb["OCCUR_BALANCE"]>0],
                color = "red")
        plt.bar(fundjour_data_gb.index[fundjour_data_gb["OCCUR_BALANCE"]<=0],
                fundjour_data_gb["OCCUR_BALANCE"][fundjour_data_gb["OCCUR_BALANCE"]<=0],
                color = "lightgreen")
        print(os.path.join(output_path,"出入金统计.png"))
        #保存图片
        plt.savefig(os.path.join(output_path,"出入金统计.png"),
                    bbox_inches = 'tight')
        plt.close()
    
    
        
        #下面开始化累计收益图
        rate_of_return = ((fuholddrop_data_gb["DROP_INCOME"] - \
            fuholddrop_data_gb["TOTAL_FARE"]) / \
            furisktotal_data["TOTAL_BALANCE"])
        acc_rate_of_return = pd.Series(index=rate_of_return.index)
    
        for my_iter,_ in enumerate(rate_of_return):
            print(my_iter)
            acc_rate_of_return.iloc[my_iter] = rate_of_return.iloc[:(my_iter+1)].sum()
            print(acc_rate_of_return)
        #x轴标签
        plt.ticklabel_format(style='plain',axis='x',useOffset=False)
        plt.xticks(acc_rate_of_return.index,rotation=90)
        #折线图
        plt.plot(acc_rate_of_return)
        plt.grid(True)
        plt.savefig(os.path.join(output_path,"累计收益图.png"),
                bbox_inches = 'tight')
        plt.close()
        
        
        #下面开始画累计盈亏和盯市盈亏
        
    
    
        #下面开始画当日权益
        #x轴标签
        #plt.ticklabel_format(style='plain',axis='x',useOffset=False)
        plt.xticks(pd.to_datetime(furisktotal_data.index[0],
                                  furisktotal_data.index[-1]),rotation=90)
        plt.plot(furisktotal_data["TOTAL_BALANCE"])
