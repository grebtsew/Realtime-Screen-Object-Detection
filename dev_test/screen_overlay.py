import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *


class MyNotification(QMainWindow):

    def __init__(self):

        QMainWindow.__init__(self)

        # < Styles >
        self.background_style_css = "background-color: rgba(22, 160, 133, 100); border-radius: 4px;"
        self.close_button_style_css = """
                                        QPushButton{
                                                    background-color: none;
                                                    color: white; border-radius: 6px;
                                                    font-size: 18px;
                                                    }
                                    """
        # </ Styles >

        # < Global Settings >
        self.setFixedSize(510, 210)
        self.move(400, 30)
        # </ Global Settings >

        # < Main Style >
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

    def terminal_ask(self):

        while True:

            print("If you want to close this window, type stop: ")

            get_input = input()

            if get_input.lstrip().rstrip().lower() == "stop":
                self.close_window()

            else:
                print("Invalid Syntax, Try it again.")

#            QApplication.processEvents()

    def close_window(self):

        self.close()
    #    sys.exit()


if __name__ == '__main__':

    My_Application = QApplication(sys.argv)
    MainWindow = MyNotification()

    MainWindow.show()
    MainWindow.terminal_ask()

    sys.exit(My_Application.exec_())
