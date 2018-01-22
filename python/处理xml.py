# -*- coding: utf-8 -*-
"""
@author: DachuanZhao
@environment: python3.6.2
"""
import pandas as pd
import os.path
import xml.dom.minidom
import networkx as nx

#文件路径
file_path = r"C:\Users\Administrator\Desktop\projet\projet"
#输出路径
output_path = file_path


#处理xml文件
#文件的一些属性
xml_name = "dynn.xml"
xml_columns = ["Ident","Etat","EtatExp","DMajEtatExp","Debit","Taux",
                "DebitLisse","TauxLisse","VitesseBRP"]
#读取文件
DOMTree = xml.dom.minidom.parse(os.path.join(file_path,xml_name))
#获得根节点
root = DOMTree.documentElement
#新建csv文件
xml_df = pd.DataFrame(columns=xml_columns)
#生成csv
for c_i in xml_columns:
    c_i_list = []
    for _ in root.getElementsByTagName("ARC"):
        c_i_list.append(_.getAttribute(c_i))
    xml_df[c_i] = c_i_list
#生成csv
xml_df.to_csv(os.path.join(output_path,"xml_ARC.csv"))

#处理gml
gml_name = "sig.gml"
gml = nx.read_gml(os.path.join(file_path,gml_name),"gml")
