#用于微波网络的不定导纳矩阵科学计算
import numpy as np
import sys
import json

from user_input import Get

def go(n):
    datas = Get(n).data #data是外部传入的列表用于存储信息的
    return datas

def Buding(num,datas):
    #不定导纳矩阵运算
    z = np.zeros((num, num), dtype=complex)
    buding = z.copy()
    for data in datas:
        zero = np.zeros((num, num), dtype=complex)
        zero[data['l']-1,data['l']-1] = data['y']
        zero[data['r'] - 1, data['r'] - 1] = data['y']
        zero[data['l'] - 1, data['r'] - 1] = -data['y']
        zero[data['r'] - 1, data['l'] - 1] = -data['y']
        buding = buding + zero
    return buding

def Yarray(array):
    #节点导纳矩阵
    Y = array.copy()
    tmp1 = np.delete(Y, 0, axis=1)
    tmp2 = np.delete(tmp1, 0, axis=0)
    Y = tmp2
    return Y





