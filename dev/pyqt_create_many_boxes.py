import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
import time
import logging


def create(score, classification, x,y,width,height):
    logging.info("create")
    splash_pix = QPixmap('../images/box2.png')
    splash_pix = splash_pix.scaled(width,height);

    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    #splash.setWindowOpacity(0.2)
    splash.setWindowFlag(Qt.WindowStaysOnTopHint)
    splash.setAttribute(Qt.WA_NoSystemBackground)
    splash.setAttribute(Qt.WA_TranslucentBackground)

    label = QLabel( splash );
    label.setWordWrap( True );
    label.setText( score + " " + classification );


    splash.setAttribute(Qt.WA_NoSystemBackground)
    splash.move(x,y)

    splash.show()
    
    logging.info("done")
    return splash


if __name__ == '__main__':

    app = QApplication(sys.argv)
    x = 10
    y = 10
    width = 100
    height = 100

    i = 0
    list = []
    while(1):
        list.append( create("10%", "person", 10+i,10+i,100,100))
        i = i+1
        time.sleep(0.1)
    time.sleep(2)

    sys.exit(app.exec_())
