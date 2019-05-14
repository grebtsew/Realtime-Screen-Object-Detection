import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
import time


def create(x,y,width,height):
    window = QMainWindow()

    label = QLabel(window)
    label.resize(width, height)

    background_style_css = "background-color: rgba(22, 160, 133, 100); border-radius: 4px;"

    label.setStyleSheet(background_style_css)

    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    window.setWindowFlags( Qt.WindowStaysOnTopHint)
    window.move(x,y)
    window.show()

def close(window):
    print("close window")
    window.close()

if __name__=="__main__":
    app = QApplication(sys.argv)
    close_button_style_css = """
                                    QPushButton{
                                                background-color: none;
                                                color: white; border-radius: 6px;
                                                font-size: 18px;
                                                }
                                """

    app.setStyleSheet(close_button_style_css)


    window = create(10,10,100,100)
    print("wait 10")
    time.sleep(10)
    print("close")
    close(window)
