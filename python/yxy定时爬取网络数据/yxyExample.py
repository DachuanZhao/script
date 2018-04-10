import pandas as pd
import sys
import os.path

class File(object):
    
    def __init__(self,work_path,file_name,encoding="UTF-8"):
        self.work_path = self.__set_work_path(work_path)
        self.file_name = file_name
        self.encoding = encoding
        
    def __set_work_path(self,work_path):
        if os.path.dirname(sys.argv[0]) == "":
            work_path = work_path
        else:
            work_path = os.path.dirname(sys.argv[0])
        return work_path



class YxyExample(File):
    
    def __init__(self,work_path,file_name,encoding="UTF-8"):
        super().__init__(work_path,file_name,encoding="UTF-8")
        self.df = pd.read_csv(os.path.join(work_path,file_name),
                               encoding = self.encoding,
                               engine='python',
                               header = None)
        
    def clean_df(self):
        temp_df = self.df[0].str.split("\t",expand=True)
        temp_df[0] = pd.to_datetime(temp_df[0])
        temp_df = temp_df.set_index(0)
        time_delta_list = [0]
        for my_iter,value in enumerate(temp_df.index[:-1]):
            time_delta_list.append(int(
                    ((temp_df.index[my_iter+1]-value).total_seconds())/180))
        temp_df["time_delta"] = time_delta_list
        self.df = temp_df
            
    
if __name__ == "__main__":
    work_path = r'E:\script\python\yxy定时爬取网络数据'
    file_name = "exemple.csv"
    encoding = "UTF-8"
    csv = YxyExample(work_path,file_name,encoding)
    csv.clean_df()
    print(csv.df)
