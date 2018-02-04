# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 23:35:33 2017

@author: hnjyz
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bs_obj = BeautifulSoup(html,"lxml")
nameList = bs_obj.findAll("span",{"class":"green"})
for name in nameList:
    print(name.get_text())
    
#处理子标签和其他后代标签    
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bs_obj = BeautifulSoup(html,"lxml")
for child in bs_obj.find("table",{"id":"giftList"}).children:
    print(child)
    
#处理兄弟标签
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bs_obj = BeautifulSoup(html,"lxml")
for sibling in bs_obj.find("table",{"id":"giftList"}).tr.next_siblings:
    print(sibling)
    
#父标签处理,有问题
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bs_obj = BeautifulSoup(html,"lxml")
print(bs_obj.find("img",{"src":"../img/gifts/img1.jpg"
                        }).parent.previous_sibling.get_text())

#正则表达式之后
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
html  = urlopen("http://www.pythonscraping.com/pages/page3.html")
bs_obj = BeautifulSoup(html,"lxml")
images = bs_obj.findAll("img",{"src":re.compile("\.\.\/img\/gifts\/img.*\.jpg")})
for image in images:
    print(image["src"])\
    
