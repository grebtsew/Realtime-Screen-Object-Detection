import sys
from PyQt5 import QtCore, QtWidgets
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
import time

class Ui_FirstWindow(object):
    width = 0
    height = 0
    x = 0
    y = 0

    def __init__(self, width, height, x,y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def setupUi(self, FirstWindow):

        FirstWindow.setObjectName("FirstWindow")
        self.centralWidget = QtWidgets.QWidget(FirstWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
#        self.pushButton.setGeometry(QtCore.QRect(110, 130, 191, 23))
        self.pushButton.setObjectName("pushButton")
        FirstWindow.resize(self.width,self.height)

        FirstWindow.move(self.x,self.y)
        FirstWindow.setCentralWidget(self.centralWidget)


        self.retranslateUi(FirstWindow)
        QtCore.QMetaObject.connectSlotsByName(FirstWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("FirstWindow", "FirstWindow"))
#        self.pushButton.setText(_translate("FirstWindow", "LoadSecondWindow"))

    def LoadSecondWindow(self):
        SecondWindow = QtWidgets.QMainWindow()
        ui = Ui_SecondWindow()
        ui.setupUi(SecondWindow)
        SecondWindow.show()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("SecondWindow", "SecondWindow"))
        #self.pushButton.setText(_translate("SecondWindow", "Congratz !"))

class Controller:

    def __init__(self):
        pass

    def Show_FirstWindow(self, width, height, x ,y):

        self.FirstWindow = QtWidgets.QMainWindow()
        self.ui = Ui_FirstWindow(width,height,x,y)
        self.ui.setupUi(self.FirstWindow)
        # < Header Style >
        self.FirstWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.FirstWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.FirstWindow.setFixedSize(width,height)
        self.FirstWindow.show()

    def Show_SecondWindow(self):
        self.FirstWindow = QtWidgets.QMainWindow()
        self.ui = Ui_FirstWindow()
        self.ui.setupUi(self.FirstWindow)
        self.ui.pushButton.clicked.connect(self.Show_SecondWindow)

        self.FirstWindow.show()
        '''
        self.SecondWindow = QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow()
        self.ui.setupUi(self.SecondWindow)
        self.ui.pushButton.clicked.connect(self.Print)

        self.SecondWindow.show()
        '''

    def Print(self):
        print('After 99 hours of trying out everything')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    Controller2 = Controller()
    Controller2.Show_FirstWindow(500,500,10,10)

    sys.exit(app.exec_())
