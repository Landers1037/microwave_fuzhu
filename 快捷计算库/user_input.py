'''由用户输入的变量由此类进行存储'''
import sys

class Get:
    data = []
    def __init__(self,n):
        dict = {'y':0,'l':0,'r':0}
        self.count = int(input('节点数'))
        for n in range(n):
            dict['y'] = int(input('电导值'))+int(input('电纳值'))*1j
            dict['l'] = int(input('左节点'))
            dict['r'] = int(input('右节点'))
            self.data.append(dict)