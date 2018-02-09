# -*- coding: utf-8 -*-
import savReaderWriter
import os.path
import sys

def save_func_help(file_path,func_name):
    out = sys.stdout
    sys.stdout = open(file_path,'w')
    help(func_name)
    sys.stdout.close()
    sys.stdout = out
    
def set_encode_mbcs():
    sys.getfilesystemencoding()#查看修改前的
    sys._enablelegacywindowsfsencoding()#修改
    sys.getfilesystemencoding()#查看修改后的
    
    
if __name__ == "__main__":
    file_dir = r"D:\dropbox\Dropbox\git_hnjyzdc\git_python\李鑫老师人口统计学"
    file_name = "20171024易感人格与流动性数据.sav"
    save_func_help(os.path.join(file_dir,"SavReader.txt"),"savReaderWriter.SavReader")
    set_encode_mbcs()
    data = savReaderWriter.SavReader(os.path.join(file_dir,file_name))
    data