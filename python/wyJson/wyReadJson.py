import json
import sys
import os.path
file_path = os.path.dirname(sys.argv[0])
json_name = "minshi.json"

with open(os.path.join(file_path,json_name),'r',encoding='UTF-8') as load_f:
    load_dict = json.load(load_f)
    #print(load_dict)