# -*- coding: utf-8 -*-
"""
Created on Thu May 19 13:33:50 2016

@author: zdc
"""

class LNode:#定义每个节点
    def __init__(self,elem,next_=None):
        self.elem = elem
        self.next = next_

llist1 = LNode(1)
p = llist1
for i in range(2,11):
    p.next = LNode(i)#每一个next属性都连接着下一个对象
    p = p.next
p = llist1
while p is not None:
    print(p.elem)
    p = p.next

def length(head):
    p,n = head,0
    while p is not None:
        n += 1
        p = p.next
    return n

class LinkedListUnderflow(ValueError):
    pass

class LList:#定义单链表
    def __init__(self):
        self._head = None
        
    def is_empty(self):
        return self._head is None
        
    def prepend(self,elem):
        self._head = LNode(elem,self._head)
        
    def pop(self):#前端删除
        if self._head is None:#无节点引发异常
            raise LinkedListUnderflow('in pop')
        e = self._head.elem
        self._head = self._head.next
        return e
        
    def append(self,elem):#尾端插入
        if self._head is None:
            self._head = LNode(elem)
            return
        p = self._head
        while p.next is not None:
            p = p.next
        p.next = LNode(elem)
        
    def pop_last(self):#尾端删除
        if self._head is None:
            raise LinkedListUnderflow('in pop_last')
        p = self._head
        if p.next is None:
            e = p.elem
            self._head = None
            return e
        while p.next.next is not None:
            p = p.next
        e = p.next.elem
        p.next = None#对象是指向地址的
        return e
        
    def find(self,pred):
        p = self._head
        while p is not None:
            if pred(p.elem):
                return p.elem
            p = p.next
    
    def printall(self):
        p = self._head
        while p is not None:
            print(p.elem,end='')
            if p.next is not None:
                print(',',end='')
            p = p.next
        print('')#输出一个换行符
    
    def for_each(self,proc):
        p = self._head
        while p is not None:
            proc(p.elem)
            p = p.next
    
    def elements(self):
        p = self._head
        while p is not None:
            yield p.elem
            p = p.next
            
    def filter(self,pred):
        p = self._head
        while p is not None:
            if pred(p.elem):
                yield p.elem
            p = p.next
    
        
class StackUnderflow(ValueError):
    pass

#list实现栈
class SStack():
    def __init__(self):
        self._elems = []
        
    def is_empty(self):
        return self._elems == []
    
    def top(self):
        if self._elems == []:
            raise StackUnderflow('in SStack.top()')
        return self._elems[-1]
        
    def push(self,elem):
        self._elems.append(elem)
        
    def pop(self):
        if self._elems == []:
            raise StackUnderflow('in SStack.pop()')
        return self._elems.pop()
        

#基于链接表实现栈
class LStack():
    def __init__(self):
        self._top = None
        
    def is_enpty(self):
        return self._top is None
        
    def top(self):
        if self._top is None:
            raise StackUnderflow('in LStack.top()')
        return self._top.elem
        
    def push(self,elem):
        self._top = LNode(elem,self._top)
        
    def pop(self):
        if self._top is None:
            raise StackUnderflow('in LStack.pop()')
        p = self._top
        self._top = p.next
        return p.elem

#队列的实现
class QueueUnderflow(ValueError):
    pass

class SQueue():
    def __init__(self,init_len=8):
        self._len = init_len
        self._elems = [0]*init_len
        self._head = 0
        self._num = 0
        
    def is_empty(self):
        return self._num == 0
        
    def peek(self):
        if self._num == 0:
            raise QueueUnderflow
        return self._elems[self._head]
        
    def dequeue(self):
        if self._num == 0:
            raise QueueUnderflow
        e = self._elems[self._head]
        self._head = (self._head+1) % self._len
        self._num -= 1
        return e
        
    def enqueue(self,e):
        if self._num == self._len:
            self._extend()
        self._elems[(self._head+self._num)%self._len] = e
        self._num += 1
        
    def __extend(self):
        old_len = self._len
        self._len *= 2
        new_elems = [0]*self._len
        for i in range(old_len):
            new_elems[i] = self.elems[(self._head + i) % old_len]
        self .elems,self._head = new_elems,0