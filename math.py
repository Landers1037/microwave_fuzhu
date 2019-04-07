import numpy as np
import time

#使用字典来存储数据
data = []
num = int(input('输入节点数'))
jiedian = int((num*(num-1)/2))
for n in range(1,jiedian+1):
    dict = {'导纳':'','l':'','r':''}
    G = int(input('导纳值电导'))
    B = int(input('导纳值电纳'))
    image = 1j
    dict['导纳'] = G + B*image
    dict['l'] = int(input('左节点'))
    dict['r'] = int(input('右节点'))
    data.append(dict)


def zero():
    #创建全0矩阵
    zarray = np.zeros((num,num),dtype=complex)
    return zarray

def buding(l,r,Y):
    zarray = zero()
    #单个元件的不定导纳矩阵
    zarray[l-1,l-1] = Y
    zarray[r-1,r-1] = Y
    zarray[l-1,r-1] = -Y
    zarray[r-1,l-1] = -Y
    # print(zarray,'\n')
    return zarray

def sum():
    #矩阵的相加

    sum = zero()
    for dict in data:
        array = buding(dict['l'],dict['r'],dict['导纳'])
        sum += array
    # print('求和矩阵')
    # print(sum)
    return sum

def result():
    #得到不定导纳矩阵
    budingjuzhen = sum()
    tmp1 = np.delete(budingjuzhen,0,axis=1)
    tmp2 = np.delete(tmp1,0,axis=0)
    budingjuzhen = tmp2
    # print('不定导纳矩阵\n')
    return budingjuzhen

def Zarray():
    #Z矩阵
    Z = np.linalg.pinv(result())  # 逆矩阵就是Z矩阵
    # print('逆矩阵\n', Z)
    return Z

time.sleep(2)
print('\n----开始----')

print('单个元件的导纳矩阵和\n',sum())
print('不定导纳矩阵\n',result())
print('逆矩阵\n', Zarray())

time.sleep(2)  
print('\n----结束----')