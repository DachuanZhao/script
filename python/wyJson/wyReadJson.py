import json
import sys
import os.path
import zdc

class WyJson(zdc.file):
    
    def __init__(self,file_abs_path,encoding="UTF-8"):
        self.list = self.__json_to_list(file_abs_path,encoding = encoding)
    #读取Json文件    
    def __json_to_list(self,file_abs_path,encoding):        
        with open(file_abs_path,'r',encoding = encoding) as load_f:
            load_dict_and_list = json.load(load_f)
            return load_dict_and_list
    
    #本来我是想把查找子节点写在这的，结果发现根本没法写
    def find_lowest_leaf(self):
        pass

def set_work_path(work_path):
    if os.path.dirname(sys.argv[0]) == "":
        work_path = work_path
    else:
        work_path = os.path.dirname(sys.argv[0])
    return work_path

def getAllLeafs(dl=None,my_str="DM"):
    if type(dl) == dict:
        count_str = len(dl)
        for (key, value) in dl.items():
            if type(value) == "list":
                count_str = count_str - 1
                getAllLeafs(value)
        if count_str == len(dl):
            #leafs.append(dl)
            leafs.append(dl[my_str])
    elif type(dl) == list:
        for i in dl:
            getAllLeafs(i)
    return leafs


if __name__ == "__main__":    
    work_path = set_work_path(r"E:\script\python\wyJson")
    json_name = "minshi.json"
    json_abs_path = os.path.join(work_path,json_name)
    
    wy = WyJson(json_abs_path,encoding="UTF-8")
    # 准备保存叶子的list
    leafs=[]
    leafs = getAllLeafs(wy.dl)
    # 递归获取所有叶子节点

    print(leafs)
