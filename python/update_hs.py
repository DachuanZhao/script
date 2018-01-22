# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:11:23 2017

@author: Deontrae Zhao

#!pip install patool
"""

import os
import logging
from patoolib import extract_archive
from stat import S_IWRITE
from shutil import rmtree as srm
from shutil import copyfile as scp

def cur_dir_file_list(file_dir,file_type = '.rar',subfolder = False):
    '''
    return absolute path of .rar in root directory,not contain subdirectories
    '''
    if subfolder:
        #file_dir = str("C:\\Users\\Administrator\\Desktop\\zip")
        path_list=[]   
        for root, dirs, files in os.walk(file_dir):  
            for file in files:  
                if os.path.splitext(file)[-1] == file_type:  
                    path_list.append(os.path.join(root, file))
        return path_list
    else:
        path_list=[]   
        for file in os.listdir(file_dir):  
            if os.path.splitext(file)[1] == file_type:  
                path_list.append(os.path.join(file_dir, file))
        return path_list    
    
def my_srm(file_dir):
        while(True):
            try: 
                if (os.path.exists(file_dir)):
                    srm(file_dir)
                    break;
                else:
                    break;
            except PermissionError as e:
                print(e)
                #cancel read only attribute
                os.chmod(str(e).split("\'")[-2].replace("\\\\","\\"), S_IWRITE)
                my_srm(file_dir)
    
def main():
    default_dir_of_sql = 'UFT2.0_UF2.0\\期货UF2.0系统\\Sql\\'
    
    while True:
        input_path = os.path.join(input('请输入存放rar文件目录: '))
        temp = '请输入输出目录(回车代表rar文件目录)(保证目录下无"output"的文件夹):'
        output_path = input(temp)
        if (output_path == ''):
            output_path = input_path
        if(os.path.isdir(input_path) and os.path.isdir(output_path)):
            break
    
    lfm = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    logging.basicConfig(level=logging.NOTSET,
                        format=lfm,
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=os.path.join(output_path,"error.log"),
                        filemode='w')
    
    '''   
    input_path = 'C:\\Users\\Administrator\\Desktop\\zip'
    output_path = 'C:\\Users\\Administrator\\Desktop\\zip'
    #begin_num = input("请输入开始编号: ")
    #end_num = input("请输入结束编号: ")
    begin_num = 26
    end_num = 42
    '''
    
    
    #if the directory isn't exist,create it
    if (os.path.exists(output_path)):
        if (os.path.exists(os.path.join(output_path, "output"))):
            my_srm(os.path.join(output_path, "output"))
        os.makedirs(os.path.join(output_path, "output"))   
    
    #Loop through all rar
    rar_path_list = cur_dir_file_list(input_path)
    
    for rar_path in rar_path_list:
        
        #rar_path = rar_path_list[5]
        unrar_path = rar_path + "_files"
        
        if os.path.isdir(unrar_path):
            my_srm(unrar_path) 
        else:
            os.makedirs(unrar_path)
        extract_archive(rar_path, outdir=(unrar_path),interactive=False)
        
        sql_path = os.path.join(unrar_path,default_dir_of_sql)
        
        if os.path.isdir(sql_path):
            sql_path_list = cur_dir_file_list(sql_path,file_type = '.sql')        
            sql_out_path = os.path.join(output_path,
                                        "output",
                                        os.path.basename(rar_path))
            
            if not os.path.exists(sql_out_path):
                os.makedirs(sql_out_path)
            
            for sql_path_i in sql_path_list:
                scp(sql_path_i,
                    os.path.join(sql_out_path,
                                 os.path.basename(sql_path_i)))
            
        my_srm(unrar_path)
        
main()