# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 23:37:43 2018

@author: Administrator
"""

import zdc

if __name__ == "__main__":
    file = zdc.file(r"D:\script\python","1234.txt")
    print(file.file_name)
    print(file.work_path)