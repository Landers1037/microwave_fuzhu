import PyQt5
from PyQt5 import*
import numpy as np
import time
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QTextEdit
from PyQt5.Qt import QFont
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
import numpy.core._dtype_ctypes

'''使用pyqt做一个简单的客户端'''


class window(QWidget):
    data = []
    A = B = C = D = 0.1+ 1j

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.lb = QLabel(self)
        self.rin = QLabel(self)
        self.rout = QLabel(self)
        self.inadd = QLabel('+',self)
        self.outadd = QLabel('+',self)
        self.b2 = QPushButton(self)
        self.b3 = QPushButton(self)
        self.b4 = QPushButton(self)
        self.ex = QPushButton('退出', self)
        self.lb1 = QLabel(self)
        self.lb2 = QLabel(self)
        self.lb3 = QLabel(self)
        self.lb4 = QLabel(self)
        self.qle = QLineEdit(self)
        self.qle1 = QLineEdit(self)
        self.qle2 = QLineEdit(self)
        self.qle3 = QLineEdit(self)
        self.qle4 = QLineEdit(self)
        self.qle5 = QTextEdit(self)  # 用于显示的文本框
        self.inrline = QLineEdit(self)
        self.inuline = QLineEdit(self)# 输入阻抗
        self.orline = QLineEdit(self)
        self.ouline = QLineEdit(self)# 输出阻抗
        self.qlelist = [self.qle1, self.qle2, self.qle3, self.qle4,self.inrline,self.inuline,self.orline,self.ouline]
        self.buttonlist = [self.b2, self.b3, self.b4, self.ex]

        self.lb.setText('节点数')
        self.rin.setText('j  源阻抗')
        self.rout.setText('j  负载阻抗')
        self.b2.setText('添加参数')
        self.b3.setText('计算')
        self.b4.setText('清空')
        self.lb1.setText('电导')
        self.lb2.setText('电纳')
        self.lb3.setText('前节点')
        self.lb4.setText('后节点')

        self.qle.setGeometry(40, 50, 80, 40)
        self.qle1.setGeometry(40, 100, 80, 40)
        self.qle2.setGeometry(130, 100, 80, 40)
        self.qle3.setGeometry(220, 100, 80, 40)
        self.qle4.setGeometry(310, 100, 80, 40)
        self.qle5.setGeometry(25, 350, 500, 500)
        self.inrline.setGeometry(40,170,80,40)
        self.inuline.setGeometry(150,170,80,40)
        self.orline.setGeometry(40,220,80,40)
        self.ouline.setGeometry(150,220,80,40)

        self.lb.move(130, 60)
        self.b2.move(430, 95)
        self.b3.move(40, 290)
        self.b4.move(160, 290)
        self.ex.move(280, 290)
        self.lb1.move(60, 150)
        self.lb2.move(150, 150)
        self.lb3.move(230, 150)
        self.lb4.move(330, 150)
        self.rin.move(250,180)
        self.rout.move(250,230)
        self.inadd.move(130,180)
        self.outadd.move(130,230)

        # 样式表
        for n in range(len(self.buttonlist)):
            self.buttonlist[n].setStyleSheet('''
            QPushButton{
                        color:white;
                        background:black;
                        font-size:17px;
                        height:50px;
                        width:70px;
                        font-family:"微软雅黑";
                        border-radius:5px;
                        }
            QPushButton:pressed{
                        color:white;
                        background:dark green;
                        font-size:17px;
                        height:50px;
                        width:70px;
                        font-family:"微软雅黑";
                        border-radius:5px;
                        }''')
        self.qle.setStyleSheet('''
                                border:2px black;
                                width:300px;
                                border-radius:10px;
                                padding:2px 4px;
                                font-size:17px;
                                ''')
        self.qle5.setStyleSheet('''
                                border:2px solid black;
                                border-radius:15px;
                                padding:1px 8px;
                                font-size:17px;
                                ''')
        for n in range(len(self.qlelist)):
            self.qlelist[n].setStyleSheet('''
                                border:2px black;
                                width:300px;
                                font-size:17px;
                                border-radius:10px;
                                padding:2px 4px;
                                ''')

        self.b2.clicked.connect(self.get)
        self.b3.clicked.connect(self.out)
        self.b4.clicked.connect(self.clean)
        self.ex.clicked.connect(QCoreApplication.quit)

        self.setGeometry(300, 100, 550, 850)
        self.setWindowTitle('矩阵计算')
        self.setFont(QFont('宋体', 11, QFont.Normal))
        self.show()

    def get(self):
        n = int(self.qle.text())
        nof = n*(n-1)/2
        if len(self.data) < int(nof):
            dict = {'导纳': '', 'l': '', 'r': ''}
            image = 1j
            dict['导纳'] = int(self.qle1.text()) + int(self.qle2.text())*image
            dict['l'] = int(self.qle3.text())
            dict['r'] = int(self.qle4.text())
            self.data.append(dict)
        else:
            # print('输入的元件数目超出')
            self.qle5.setText('输入的元件数目超出')
            pass

    def clean(self):
        for n in range(4):
            self.qlelist[n].setText(None)
        self.qle.setText(None)  # 清空文本框
        self.data.clear()  # 清空参数列表
        self.qle5.clear()

    def zero(self):
        # 创建全0矩阵
        num = int(self.qle.text())
        zarray = np.zeros((num, num), dtype=complex)
        return zarray

    def buding(self, l, r, Y):
        zarray = self.zero()
        # 单个元件的不定导纳矩阵
        zarray[l-1, l-1] = Y
        zarray[r-1, r-1] = Y
        zarray[l-1, r-1] = -Y
        zarray[r-1, l-1] = -Y
        # print(zarray,'\n')
        return zarray

    def sum(self):
        # 矩阵的相加得到不定导纳矩阵
        sum = self.zero()
        for dict in self.data:
            array = self.buding(dict['l'], dict['r'], dict['导纳'])
            sum += array
        # print('求和矩阵')
        # print(sum)
        return sum

    def result(self):
        # 得到节点导纳矩阵
        dingjuzhen = self.sum()
        tmp1 = np.delete(dingjuzhen, 0, axis=1)
        tmp2 = np.delete(tmp1, 0, axis=0)
        dingjuzhen = tmp2
        # print('定导纳矩阵\n')
        return dingjuzhen

    def Zarray(self):
        # Z矩阵
        Z = np.linalg.pinv(self.result())  # 逆矩阵就是Z矩阵
        # print('逆矩阵\n', Z)
        return Z

    def Z(self):
        j = int(self.qle.text())-3
        k = int(self.qle.text())-2
        zarray = self.Zarray()
        self.A = zarray[j,j]/zarray[k,j]
        self.B = -(zarray[j,j]*zarray[k,k]-zarray[j,k]*zarray[j,k])/zarray[j,k]
        self.C = -1/zarray[k,j]
        self.D = zarray[k,k]/zarray[k,j]

    def Zin(self):
        #计算输入阻抗参数
        ZL = int(self.orline.text()) + int(self.ouline.text())*1j
        zin = (self.A*ZL + self.B)/(self.C*ZL + self.D)
        return zin

    def Zout(self):
        #输出阻抗
        ZG = int(self.inrline.text()) + int(self.inuline.text())*1j
        zout = (self.D*ZG + self.B)/(self.C*ZG+self.A)
        return zout


    def Sin(self):
        # s参数
        ZG = int(self.inrline.text()) + int(self.inuline.text()) * 1j
        sin = (self.Zin() - ZG)/(self.Zin() + ZG)
        return sin

    def Sout(self):
        ZL = int(self.orline.text()) + int(self.ouline.text()) * 1j
        sout = (self.Zout() - ZL)/(self.Zout() + ZL)
        return sout

    def out(self):
        n = int(self.qle.text()) # 节点数
        nof = n*(n-1)/2 # 计算总元件数
        try:
            self.Z()
            self.qle5.setText('所需的元件数目: ' + str(int(nof)) + '\n' + '取1节点为公共端点' \
                          '\n不定导纳矩阵:\n' + str(self.sum()) +
                          '\n  '+'\n节点导纳矩阵:\n' + str(self.result()) + '\n  '+'\nZ矩阵:\n' + str(self.Zarray()) +
                          '\n' + '\n输入阻抗\n' + str(self.Zin()) + '\n' \
                              + '\n输出阻抗\n' + str(self.Zout()) + '\n' \
                              + '\n输入反射系数\n' + str(self.Sin()) + '\n' \
                              + '\n输出反射系数\n' + str(self.Sout()))
        except Exception as e:
            self.qle5.setText('计算出现错误，检查输入的变量')


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = window()
    sys.exit(app.exec_())
