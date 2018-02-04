# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 21:38:33 2017

@author: hnjyz
"""

from urllib.request import urlopen
text_page = urlopen(
        "http://www.pythonscraping.com/pages/warandpeace/chapter1.txt")
print(text_page.read())

from urllib.request import urlopen
from io import StringIO
import csv
data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").\
read().decode('utf-8','ignore')
data_file = StringIO(data)
csv_reader = csv.reader(data_file)
for row in csv_reader:
    print(row)

from urllib.request import urlopen
from io import StringIO
import csv
data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").\
read().decode('utf-8','ignore')   
data_file = StringIO(data)
dict_reader = csv.DictReader(data_file)
print(dict_reader.fieldnames)
for row in dict_reader:
    print(row)
    

from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager,process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open

def read_pdf(pdf_file):
    rsrcmgr = PDFResourceManager()
    retstr= StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr,retstr,laparams = laparams)
    
    process_pdf(rsrcmgr,device,pdf_file)
    device.close()
    
    content = retstr.getvalue()#获得文字
    retstr.close()
    return content

pdf_file = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1.pdf")
#在本机中可直接换成open
#pdf_file = open(,"rb")
outputString = read_pdf(pdf_file)
print(outputString)
pdf_file.close()


#docx

from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO

word_file = urlopen("http://pythonscraping.com/pages/AWordDocument.docx").read()
word_file = BytesIO(word_file)
document = ZipFile(word_file)
xml_content = document.read('word/document.xml')
print(xml_content.decode('utf-8'))



from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO
from bs4 import BeautifulSoup

word_file = urlopen("http://pythonscraping.com/pages/AWordDocument.docx").read()
word_file = BytesIO(word_file)
document = ZipFile(word_file)
xml_content = document.read('word/document.xml')

word_obj = BeautifulSoup(xml_content.decode('utf-8'),"lxml")
text_strings = word_obj.findAll("w:t")
for text_elem in text_strings:
    print(text_elem.text)



textStrings = word_obj.findAll("w:t")

for text_elem in text_strings:
    close_tag = ""
    try:
        style = text_elem.parent.previousSibiling.find("w:pstyle")
        if style is not None and style["w:val"] == "Title":
            print("<hl>")
            close_tag = "</hl>"
    except AttributeError:
    #不打印标签
        pass
    print(text_elem.text)
    print(close_tag)
                




