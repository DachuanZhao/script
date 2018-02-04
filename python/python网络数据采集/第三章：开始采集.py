# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 01:23:25 2017

@author: hnjyz
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
bs_obj = BeautifulSoup(html,"lxml")
for link in bs_obj.findAll("a"):
    if 'href' in link.attrs:
        print(link.attrs['href'])
        
#修改后
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
bs_obj = BeautifulSoup(html,"lxml")
for link in bs_obj.find("div",{"id":"bodyContent"}).findAll("a",
                       href = re.compile("^(/wiki/)((?!:).)*$")):
    if 'href' in link.attrs:
        print(link.attrs['href'])
        
#完整代码
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re
random.seed(datetime.datetime.now())
def getLinks(article_url):
    html = urlopen("https://en.wikipedia.org" + article_url)
    bs_obj = BeautifulSoup(html,"lxml")
    return bs_obj.find("div",{"id":"bodyContent"}).findAll("a",
                      href = re.compile("^(/wiki/)((?!:).)*$"))
links = getLinks("/wiki/Kevin_Bacon")
while len(links) > 0:
    newArticle = links[random.randint(0,len(links)-1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)
    
from urllib.request import urlopen
from bs4 import BeaytifulSoup
import re
pages = set()
def getLinks(page_url):
    global pages
    html = urlopen("https://en.wikipedia.org" + page_url)
    bs_obj = BeautifulSoup(html,"lxml")
    for link in bs_obj.findAll("a",href = re.compile("^(/wiki/)")):
        if link.attrs['href'] not in pages:
            #遇到新页面
            new_page = link.attrs['href']
            print(new_page)
            pages.add(new_page)
            getLinks(new_page)
            
getLinks("")

#搜集整个网站数据
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()
def getlinks(page_url):
    global pages
    html = urlopen("https://en.wikipedia.org" + page_url)
    bs_obj = BeautifulSoup(html)
    try:
        print(bs_obj.h1.get_text())
        print(bs_obj.find(id="mw-content-text").findAll("p")[0])
        print(bs_obj.find(id="ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print("页面缺少一些属性！不过不用担心！")
    for link in bs_obj.findAll("a",href = re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                #我们遇到了新页面
                new_page = link.attrs['href']
                print("----------------\n"+new_page)
                pages.add(new_page)
                getLinks(new_page)
getLinks("")

#通过互联网采集
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

#获取页面所有内链的列表
def get_internal_links(bs_obj,include_url):
    include_url = urlparse(include_url).scheme + "://" + \
    urlparse(include_url).netloc
    internal_links = []
    #找出所有以“/”开头的链接
    for link in bs_obj.findAll("a",
                               href = re.compile("^(/|.*" + \
                                                    include_url + ")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internal_links:
                internal_links.append(link.attrs['href'])
            else:
                internal_links.append(link.attrs['href'])
    return internal_links

#获取页面所有外链的列表
def get_external_links(bs_obj,exclude_url):
    external_links = []
    #找出所有以"http"或"www"开头且不包含当前URL的链接
    for link in bs_obj.findAll("a",
                               href = re.compile("^(http|www)(?!" + \
                                                 exclude_url + ").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in external_links:
                external_links.append(link.attrs['href'])
    return external_links

def get_random_external_link(starting_page):
    html = urlopen(starting_page)
    bs_obj = BeautifulSoup(html)       
    external_links = get_external_links(bs_obj,splitAddress(starting_page)[0])
    if len(external_links) == 0:
        print("没有额外的链接,正在查找")
        domain = urlparse(starting_page).scheme + \
        "://" + urlparse(starting_page).netloc
        internal_links = get_internal_links(bs_obj,domain)
        internal_links = get_internal_links(starting_page)
        return get_next_external_link(
                internal_links[random.randint(0,len(internal_links)-1)])
    else:
        return external_links[random.randint(0,len(external_links)-1)]

def follow_external_only(starting_site):
    external_link = get_random_external_link(starting_site)
    print("Random extern link is: " + external_link)
    follow_external_only(external_link)
    
follow_external_only("http://oreilly.com")
        
    
     
        
        
        
        