import PyQt5
from PyQt5 import*
import numpy as np
import time
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QTextEdit
from PyQt5.Qt import QFont
import numpy.core._dtype_ctypes

'''使用pyqt做一个简单的客户端'''


class window(QWidget):
    data = []

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.lb = QLabel(self)
        self.b2 = QPushButton(self)
        self.b3 = QPushButton(self)
        self.b4 = QPushButton(self)
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
        self.qlelist = [self.qle1, self.qle2, self.qle3, self.qle4]

        self.lb.setText('节点数')
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
        self.qle5.setGeometry(30, 250, 500, 350)
        self.lb.move(130, 50)
        self.b2.move(430, 100)
        self.b3.move(40, 200)
        self.b4.move(160, 200)
        self.lb1.move(60, 150)
        self.lb2.move(150, 150)
        self.lb3.move(230, 150)
        self.lb4.move(330, 150)

        self.b2.clicked.connect(self.get)
        self.b3.clicked.connect(self.out)
        self.b4.clicked.connect(self.clean)

        self.setGeometry(300, 100, 550, 650)
        self.setWindowTitle('矩阵计算')
        self.setFont(QFont('微软雅黑', 11, QFont.Normal))
        self.show()

    def get(self):
        if len(self.data) < int(self.qle.text()):
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
        # 矩阵的相加
        sum = self.zero()
        for dict in self.data:
            array = self.buding(dict['l'], dict['r'], dict['导纳'])
            sum += array
        # print('求和矩阵')
        # print(sum)
        return sum

    def result(self):
        # 得到不定导纳矩阵
        budingjuzhen = self.sum()
        tmp1 = np.delete(budingjuzhen, 0, axis=1)
        tmp2 = np.delete(tmp1, 0, axis=0)
        budingjuzhen = tmp2
        # print('不定导纳矩阵\n')
        return budingjuzhen

    def Zarray(self):
        # Z矩阵
        Z = np.linalg.pinv(self.result())  # 逆矩阵就是Z矩阵
        # print('逆矩阵\n', Z)
        return Z

    def out(self):
        n = int(self.qle.text())
        nof = n*(n-1)/2
        self.qle5.setText('所需的元件数目: ' + str(int(nof)) + '\n求和矩阵:\n' + str(self.sum()) +
                          '\n  '+'\n不定导纳矩阵:\n' + str(self.result()) + '\n  '+'\nZ矩阵:\n' + str(self.Zarray()))
        # print('\n----开始----')
        # print('节点数: ', self.qle.text())
        # print('所需的元件数目: ', int(nof))
        # print('元件的导纳矩阵和\n', self.sum())
        # print('不定导纳矩阵\n', self.result())
        # print('逆矩阵\n', self.Zarray())

        # time.sleep(2)
        # print('\n----结束----')


if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = window()
    sys.exit(app.exec_())
