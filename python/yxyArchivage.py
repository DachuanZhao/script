# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 17:06:19 2018

@author: Administrator
"""

import urllib.request
import datetime
import time
import sys
import os.path

url="http://jadyn.strasbourg.eu/GPS/dynn.xml"
count_e = 0
count_s = 0
file_path = os.path.dirname(os.path.abspath(sys.argv[0]))
time_wait = 5

while True:
    try:
        dt=str(datetime.datetime.now().replace(microsecond=0)).replace(" ","_").replace(":","_")
        output_path = os.path.join(file_path,("".join(("FILE_",str(dt),".xml"))))
        print("this is ",count_s," TH success")
        print("output_path is :",output_path)
        count_s = count_s + 1
        urllib.request.urlretrieve(url,output_path)
        time.sleep(time_wait)
    except ConnectionResetError as e:
        print("error is ",e)
        time.sleep(time_wait)
        count_e = count_e  + 1
        print("this is ",count_e," TH error")
        