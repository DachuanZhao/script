# -*- coding: utf-8 -*-
"""
Created on Sat May 21 21:24:52 2016

@author: zdc
"""
class BinTNode:
    def __init__(self,dat,left = None,right = None):
        self.data = dat
        self.left = left
        self.right = right
        
    def count_BinTNodes(t):#统计节点个数
        if t is None:
            return 0
        else:
            return 1 + count_BinTNodes(t.left) + count_BinTNodes(t.right)
            
    def sum_BinTNodes(t):#假设节点中保存值，求所有数值和
        if t is None:
            return 0
        else:
            return t.dat + sum_BinTNodes(t.left) + sum_BinTNodes(t.right)
            
    def preorder(t,proc):#proc是具体的结点数据操作#递归定义的遍历函数
        if t is None:
            return
        proc(t.data)
        preorder(t.left)
        preorder(t.right)
        
    def print_BinTNodes(t):
        if t is None:
            print('^',end='')#空树输出 ^
            return
        print('(' + str(t.data),end='')
        print_BinTNodes(t.left)
        print_BinTNodes(t.right)
        print(')',end='')
        
    from SQueue import *
    