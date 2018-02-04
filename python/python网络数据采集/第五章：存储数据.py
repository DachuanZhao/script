# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 18:46:18 2017

@author: hnjyz
"""

from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
file_path = r"D:\python3.x\python网络数据采集"


html = urlopen("http://pythonscraping.com/")
bs_obj = BeautifulSoup(html,"lxml")
image_location = bs_obj.find("a",{"id":"logo"}).find("img")["src"]
urlretrieve (image_location,file_path + "\\logo.jpg")

import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

download_directory = "downloaded"
base_url = "http://pyrhonscraping.com"

def get_absolute_url(base_url,source):
    if source.startswith("http://www."):
        url = "http://" + source[11:]
    elif source.startswith("http://"):
        url = source
    elif source.startswith("www."):
        url = "http://" + source[4:]
    else:
        url = base_url + "/" + source
    if base_url not in url:
        return None
    return url

def get_download_path(base_url,absolute_url,download_directory):
    path = absolute_url.replace("www.","")
    path = path.replace(base_url,"")
    path = download_directory + path
    directory = os.path.dirname(path)
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    return path


html = urlopen("http://www.pythonscraping.com")
bs_obj = BeautifulSoup(html,"lxml")
download_list = bs_obj.findAll(src = True)

for download in download_list:
    #download = download_list[4]
    file_url = get_absolute_url(base_url,download["src"])
    if file_url is not None:
        print(file_url)
        urlretrieve(file_url,
                    get_download_path(base_url,
                                      file_url,
                                      download_directory))

import csv
csv_file = open(file_path + "\\test.csv","w+")#以读写方式打开
try:
    writer = csv.writer(csv_file)
    writer.writerow(('number','bumber plus 2','number times 2'))
    for i in range(10):
        writer.writerow((i,i+2,i*2))
finally:
   csv_file.close()     
   

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://en.wikipedia.org/wiki/Comparison_of_text_editors")
bs_obj = BeautifulSoup(html,"lxml")
# 主对比表格是当前页面上的第一个表格
table = bs_obj.findAll("table",{"class":"wikitable"})[0]
rows = table.findAll("tr")

csv_file = open(file_path + "\\editots.csv","wt",newline="",encoding="utf-8")
writer = csv.writer(csv_file)
try:
    #row = rows[0]
    for row in rows:
        csv_row = []
        for cell in row.findAll(["td","th"]):
            #cell = row.findAll(["td","th"])[0]
            csv_row.append(cell.get_text())
        writer.writerow(csv_row)
finally:
    csv_file.close()
    