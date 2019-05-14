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
    def setupUi(self, FirstWindow):

        FirstWindow.setObjectName("FirstWindow")
        FirstWindow.resize(400, 300)
        self.centralWidget = QtWidgets.QWidget(FirstWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 130, 191, 23))
        self.pushButton.setObjectName("pushButton")
        FirstWindow.setCentralWidget(self.centralWidget)


        self.retranslateUi(FirstWindow)
        QtCore.QMetaObject.connectSlotsByName(FirstWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("FirstWindow", "FirstWindow"))
        self.pushButton.setText(_translate("FirstWindow", "LoadSecondWindow"))

    def LoadSecondWindow(self):
        SecondWindow = QtWidgets.QMainWindow()
        ui = Ui_SecondWindow()
        ui.setupUi(SecondWindow)
        SecondWindow.show()

class Ui_SecondWindow(object):

    def setupUi(self, SecondWindow):
        SecondWindow.setObjectName("SecondWindow")
        SecondWindow.resize(400, 300)
        self.centralWidget = QtWidgets.QWidget(SecondWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 130, 191, 23))
        self.pushButton.setObjectName("pushButton")
        SecondWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(SecondWindow)
        QtCore.QMetaObject.connectSlotsByName(SecondWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("SecondWindow", "SecondWindow"))
        self.pushButton.setText(_translate("SecondWindow", "Congratz !"))

class Controller:

    def __init__(self):
        pass

    def Show_FirstWindow(self):
        self.background_style_css = "background-color: rgba(22, 160, 133, 100); border-radius: 4px;"
        self.close_button_style_css = """
                                        QPushButton{
                                                    background-color: none;
                                                    color: white; border-radius: 6px;
                                                    font-size: 18px;
                                                    }
                                    """


        self.FirstWindow = QtWidgets.QMainWindow()
        self.ui = Ui_FirstWindow()
        self.ui.setupUi(self.FirstWindow)

        self.main_back = QLabel(self)
        self.main_back.resize(500, 200)
        self.main_back.setStyleSheet(self.background_style_css)
        # </ Main Style >

        # < Text Label >
        self.text_label = QLabel(self)
        self.text_label.move(10, 5)
        self.text_label.resize(300, 100)
        self.text_label.setText("Hi YUVI, How are You ? :)")
        # < Text Label >

        # < Header Style >
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # This Line Set Your Window Always on To
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowStaysOnTopHint)
        # </ Header Style >

        self.ui.pushButton.clicked.connect(self.Show_SecondWindow)

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
    Controller2.Show_FirstWindow()
    Controller2.Show_SecondWindow()

    Controller1 = Controller()
    Controller1.Show_SecondWindow()

    sys.exit(app.exec_())
