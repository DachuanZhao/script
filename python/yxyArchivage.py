import urllib.request
import datetime
import time
import sys
import os.path

url="http://jadyn.strasbourg.eu/GPS/dynn.xml"
count = 0

while True:
    try:
        dt=datetime.datetime.now()
        dt = dt.replace(microsecond=0)
        urllib.request.urlretrieve(url, os.path."FILE_%(dt)s.xml" %{"dt":dt})
        time.sleep(180)
    except ConnectionResetError as e:
        print("error is ",e)
        time.sleep(180)
        count = count  + 1
        print("this is ",count" TH error")
