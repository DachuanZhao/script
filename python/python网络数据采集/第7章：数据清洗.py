# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 23:33:57 2017

@author: hnjyz
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

def ngrams(input,n):
    input = input.split(' ')
    output = []
    for i in range(len(input) - n + 1):
        output.append(input[i:i + n])
    return output

html = urlopen("https://en.wikipedia.org/wiki/Python")
bs_obj = BeautifulSoup(html,"lxml")
content = bs_obj.find("div",{"id":"mw-content-text"}).get_text()
ngrams = ngrams(content,2)
print(ngrams)
print("2-grams count is " + str(len(ngrams)))

def ngrams(input,n):
    input = re.sub('\n'," ",input)
    