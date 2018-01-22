# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from math import isnan

def get_data(file_path,file_name):
    """
    读取文件
    """        
    data = pd.read_csv(file_path + '\\' + "金仕达权限导出.csv",
                       encoding = 'gb18030',
                       header=None)
    return data
    
def write_txt(file_path,file_name_output,data,data_id,dight):
    value = 1
    my_id = 1
    #dight = 3
    f = open(file_path + '\\' + file_name_output,'w')
    for col in data_id.columns:
        for row in data_id.index:
            print(row,col)
            if data_id.loc[row,col] != 0:
                #col = 0
                #row = 0
                #{ id:01, pId:00, name:"父节点1 -展开","value":1,"my_id":1}
                p1 ='                    { id:' + data_id.loc[row,col] + ','
                if col > 0:
                    p2 =' pId:' + data_id.loc[row,col][:-dight] + ',name:\"'
                else:
                    p2_temp = ''
                    for p2_i in range(dight):
                        p2_temp += str(0)
                    p2 =' pId:' + p2_temp + ',name:\"'
                p3 = data.loc[row,col] + '\",\"value\":' + str(value)
                p4 = ',\"my_id\":' + str(my_id) + '},'
                p1 + p2 + p3 + p4
                f.write(p1 + p2 + p3 + p4 + '\n')
    f.close()

    
def run_file():
    file_path = r"C:\Users\hnjyz\Desktop\Desktop"
    file_name_iuput = "金仕达权限导出.csv"
    file_name_output = 'code.txt'      
    data = get_data(file_path,file_name_iuput)
    data_id = pd.DataFrame(np.zeros([len(data.index),len(data.columns)])) 
    dight = len(str(len(data.index)))
    for col in data.columns:
        for row in data.index:       
            if type(data.loc[row,col]) != float:
                #row = 1
                print([row,col])
                my_id = str(row + 1)
                while(len(my_id)<dight):
                    my_id = "0" + str(my_id)
                if (col > 0):
                    if (type(data.loc[row,col-1]) != float):
                        my_id = data_id.loc[row,col-1] + my_id
                    else:
                        for father_row in range(row-1,-1,-1):
                            if type(data.loc[father_row,col-1]) != float:
                                my_id = data_id.loc[father_row,col-1] + my_id
                                break;
                data_id.loc[row,col] = my_id
                
write_txt(file_path,file_name_output,data,data_id,dight)



            
            
        
        
        
        
        
        