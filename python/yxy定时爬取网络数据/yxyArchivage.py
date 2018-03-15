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
import logging

# create logger
logger = logging.getLogger(os.path.basename(sys.argv[0]))
logger.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# create file handler and set level to debug
time_log=str(datetime.datetime.now().replace(microsecond=0)).replace(" ","_").replace(":","_")
file_handler = logging.FileHandler("".join((str(time_log),'.log')))
file_handler.setFormatter(formatter) 

# create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# add formatter to ch
console_handler.setFormatter(formatter)

# add file and ch to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


if __name__ == "__main__":
    url="http://jadyn.strasbourg.eu/GPS/dynn.xml"
    #count error times
    count_e = 0
    #count sueeess times
    count_s = 0
    #get the current file's path of the python script
    file_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    #time between download
    time_wait = 5

    while True:
        try:
            time_now=str(datetime.datetime.now().replace(microsecond=0)).replace(" ","_").replace(":","_")
            output_path = os.path.join(file_path,("".join(("FILE_",str(time_now),".xml"))))
            logger.info("".join(("this is ",str(count_s)," TH success")))
            logger.info("".join(("output_path is :",str(output_path))))
            count_s = count_s + 1
            urllib_start_time = datetime.datetime.now()
            urllib.request.urlretrieve(url,output_path)
            urllib_spend_sec = (datetime.datetime.now() - urllib_start_time).seconds
            logger.info("".join(("downloading the web spends ",str(urllib_spend_sec),"s")))
            time.sleep(time_wait)
        except Exception as e:
            logger.exception(e)
            time.sleep(time_wait)
            count_e = count_e  + 1
            logger.info("".join(("this is ",str(count_e)," TH error")))
        