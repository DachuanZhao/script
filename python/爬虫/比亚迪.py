# -*- coding: utf-8 -*-
"""
20171121
互相交流
赵大川
"""

from selenium import webdriver
from selenium.webdriver.support.select import Select
import pandas as pd
import itertools
import time

#https://sites.google.com/a/chromium.org/chromedriver/downloads
browser = webdriver.Chrome("e://chromedriver.exe")
browser.implicitly_wait(30)
browser.get('http://www.bydauto.com.cn/counter-sellpoint.html')

'''
TIME_INTERVAL = 1

#车型
car_id = browser.find_element_by_id('carid').text.split()[1:]

#处理一个异常值"e5 300",split()会把他分成list中的两项
for car_id_remove_i in ['e5','300']:
    car_id.remove(car_id_remove_i)
car_id.append("e5 300")
       
#最终结果保存在csv
result = pd.DataFrame(columns=["car_id","pro","city"])

for car_id_i in car_id:
    #car_id_i = car_id[0]
    #模拟鼠标选择下拉框
    Select(browser.find_element_by_id('carid')).\
        select_by_visible_text(car_id_i)
    pro =  browser.find_element_by_id('pro').text.split()[1:]
    while(True):
        time.sleep(TIME_INTERVAL)
        #判断间隔后是否有变化
        if(browser.find_element_by_id('pro').text.split()[1:] == pro):
            break
        else:
            pro =  browser.find_element_by_id('pro').text.split()[1:]
        
    for pro_i in pro:
        # pro_i = pro[2]
        Select(browser.find_element_by_id('pro')).\
            select_by_visible_text(pro_i)
        city = browser.find_element_by_id('city').text.split()[1:]
        while(True):
            time.sleep(TIME_INTERVAL)
            if(browser.find_element_by_id('city').text.split()[1:] == city):
                break
            else:
                city = browser.find_element_by_id('city').text.split()[1:]

        #browser.find_element_by_xpath(
        #   "//*[@id=\"map\"]/div[1]/div[2]/div[2]/span[1]").click()        

        # 临时结果生成csv
        temp_df= pd.DataFrame(list(itertools.product([car_id_i],[pro_i],city)),
                              columns = ["car_id","pro","city"])
        # 将临时结果保存在result里
        result = pd.concat([result,temp_df])

result.to_csv("e:\\result.csv")
browser.quit()
'''