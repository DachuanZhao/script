# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 23:32:06 2018

@author: Administrator
"""
import sys
import os.path

class file():
    
    def __init__(self,work_path,file_name,encoding="UTF8"):
        self.work_path = self.__set_work_path(work_path)
        self.file_name = file_name
        self.encoding = encoding
        
    def __set_work_path(self,work_path):
        if os.path.dirname(sys.argv[0]) == "":
            work_path = work_path
        else:
            work_path = os.path.dirname(sys.argv[0])
        return work_path