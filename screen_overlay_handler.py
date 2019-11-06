from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import time

'''
COPYRIGHT @ Grebtsew 2019

This file contains functions for showing overlay detections
'''

def create_box(x,y,width,height):
    '''
    Show an overlaybox without label
    @Param x box left
    @Param y box up
    @Param width box width
    @Param height box height
    @Return overlay instance
    '''

    splash_pix = QPixmap('images/square2.png')
    splash_pix = splash_pix.scaled(width,height);

    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowOpacity(0.2)

    splash.setAttribute(Qt.WA_NoSystemBackground)
    splash.move(x,y)

    splash.show()
    return splash


def create_box_with_score_classification(score, classification, x,y,width,height):
    '''
    Show an overlaybox with label
    @Param score float
    @Param classification string
    @Param x box left
    @Param y box up
    @Param width box width
    @Param height box height
    @Return overlay instance
    '''
    splash_pix = QPixmap('images/square2.png')
    splash_pix = splash_pix.scaled(width,height);

    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowOpacity(0.2)

    label = QLabel( splash );
    label.setWordWrap( True );
    label.setText( str(int(100*score))+"%" + " " + classification );

    splash.setAttribute(Qt.WA_NoSystemBackground)
    splash.move(x,y)

    splash.show()
    return splash

def create_box_with_image_score_classification(image_path, score, classification, x,y,width,height):
    '''
    Show an overlaybox with label
    @Param score float
    @Param classification string
    @Param x box left
    @Param y box up
    @Param width box width
    @Param height box height
    @Return overlay instance
    '''
    splash_pix = QPixmap(image_path)
    splash_pix = splash_pix.scaled(width,height);

    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowOpacity(0.2)

    label = QLabel( splash );
    label.setWordWrap( True );
    label.setText( str(int(100*score))+"%" + " " + classification );

    splash.setAttribute(Qt.WA_NoSystemBackground)
    splash.move(x,y)
    splash.show()
    return splash


'''
Testing
print("do the overlay")
screen_overlay_handler.create_box(10,10,100,100)
print("done")
time.sleep(10)
print("do the overlay")
screen_overlay_handler.create_box(100,10,100,100)
print("done")
'''
