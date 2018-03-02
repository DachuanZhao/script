# -*- coding: utf-8 -*-
#from urllib.request import urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup
from selenium import webdriver
import time

if __name__ == '__main__':
    url = quote("http://sj.qq.com/myapp/search.htm?kw=微信",
                         safe='/:?=')
    browser = webdriver.Chrome("e://chromedriver.exe")
    browser.implicitly_wait(30)
    browser.get(url)
    time.sleep(10)
    bs_obj = BeautifulSoup(browser.page_source,"lxml")
    
    #我直接把网站下载了，从本地读取，下面的都没问题
    #bs_obj = BeautifulSoup(open(r"D:\input.html",encoding="utf8"),"lxml")
    
    #输出html文件
    fout = open("D://a.html", "w+", encoding="utf-8")
    print(bs_obj,file=fout)
    fout.close()
    
    href_input_list = bs_obj.find_all('a')
    href_output_list = []
    for i,href in enumerate(href_input_list):
        print(i,":",href.contents)
        if href.contents == ["微信"]:
            href_output_list.append(href["href"])