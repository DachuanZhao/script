# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 22:56:17 2017

@author: hnjyz
"""

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
def getTitle(url):
    try:#网页在服务器上或服务器不存在
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    try:#排除标签不存在的情况
        bs_obj = BeautifulSoup(html.read(),"lxml")
        title = bs_obj.body.h1
    except AttributeError as e:
        print(e)
        return None
    return title

title = getTitle("http://www.pythonscraping.com/pages/page1.html")
if title == None:
    print("Title could not be found")
else:
    print(title)