# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from urllib.request import urlopen
from urllib.parse import urlencode
from bs4 import BeautifulSoup

def my_urlencode(in_put):
    """
    转换中文为url的函数
    """
    #in_put = "俄国"
    data = {"data":in_put}
    data = urlencode(data)
    data = data[data.find('data') + 5 :]
    return data


html = urlopen("http://www.juzimi.com/country/" + my_urlencode("俄国"))
bs_obj = BeautifulSoup(html,"lxml")

picture = bs_obj.findAll("div",{"class":"views-field-tid"})
for link_picture in picture:
    if ""


for name in nameList:
    print(name)
    



