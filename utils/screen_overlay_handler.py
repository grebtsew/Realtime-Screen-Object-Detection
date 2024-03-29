from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from utils.ThreadPool import *

from utils.tracking import Tracking

import logging
import threading
import sys
import time

'''
COPYRIGHT @ Grebtsew 2019

This file contains functions for showing overlay detections
'''


class TrackingBox(QSplashScreen):
    splash_pix = None
    done = False

    def __init__(self, id, shared_variables, score, classification, box, *args, **kwargs):
        super(TrackingBox, self).__init__(*args, **kwargs)
        self.classification = classification
        self.shared_variables = shared_variables
        self.counter = 0
        # TODO: this might be a little haxy
        self.x = int(box[0]*(self.shared_variables.WIDTH/self.shared_variables.DETECTION_SCALE)-(box[2]*(self.shared_variables.WIDTH/self.shared_variables.DETECTION_SCALE))/2)
        self.y = int(box[1]*(self.shared_variables.HEIGHT/self.shared_variables.DETECTION_SCALE)-(box[3]*(self.shared_variables.HEIGHT/self.shared_variables.DETECTION_SCALE))/2)
        self.width = int(box[2]*(self.shared_variables.WIDTH/self.shared_variables.DETECTION_SCALE))
        self.height = int(box[3]*(self.shared_variables.HEIGHT/self.shared_variables.DETECTION_SCALE))
        self.id = id
        self.splash_pix = QPixmap('./docs/box2.png')
        self.splash_pix = self.splash_pix.scaled(round(self.width*self.shared_variables.DETECTION_SCALE),round(self.height*self.shared_variables.DETECTION_SCALE));
        self.setPixmap(self.splash_pix)

        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)

        label = QLabel( self )
        label.setWordWrap( True )
        label.move(30,30)
        label.setStyleSheet(" color: rgb(0, 100, 200); font-size: 15pt; ")

        label.setText( str(int(100*score))+"%" + " " + classification );
        self.move(self.x,self.y)
        self.show()

        self.tracking = Tracking( (self.x,self.y,self.width,self.height),self.shared_variables)

        self.threadpool = QThreadPool()

        logging.debug(f"New Box Created at {str(self.x)} {str(self.y)}  Size {str(self.width)} {str(self.height)}")

        self.start_worker()

    def progress_fn(self, n):
        logging.debug("%d%% done" % n)
        pass
    
    def remove(self):
        self.shared_variables.list.remove(self)
        self.done = True
        self.threadpool.cancel

    def execute_this_fn(self, progress_callback):

        if(not self.tracking.running):
            if not self.done: # Remove ourself from gui list
                self.shared_variables.list.remove(self)
                self.done = True
                self.threadpool.cancel
        else:
            self.tracking.run()

        return "Done."


    def print_output(self, s):
        #logging.debug(str(self.id))
        self.hide()
        self.repaint_size(round(self.tracking.box[2]*self.shared_variables.DETECTION_SCALE), round(self.tracking.box[3]*self.shared_variables.DETECTION_SCALE))
        self.move(round(self.tracking.box[0]*self.shared_variables.DETECTION_SCALE), round(self.tracking.box[1]*self.shared_variables.DETECTION_SCALE))
        self.show()

    def thread_complete(self):
        #logging.debug("THREAD COMPLETE!")
        self.start_worker()

    def start_worker(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

    def repaint_size(self, width, height):
        #splash_pix = QPixmap('../images/box2.png')
        self.splash_pix = self.splash_pix.scaled(width,height);
        self.setPixmap(self.splash_pix)


    def get_box(self):
        return self.tracking.box


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

#TODO
def create_fancy_box(score, classification,  x,y,width,height):
    # Create fancier box without image
    splash_pix = QPixmap(width, height)


    painter = QPainter(splash_pix)
    painter.setPen(QPen(Qt.blue,  10, Qt.SolidLine))
    path = QPainterPath()

    path.addRoundedRect(QRectF(0+10,0+10,width-20,height-20), 30, 30);
    painter.drawPath(path);
    painter.end()


    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowOpacity(1)
    splash.setAttribute(Qt.WA_TranslucentBackground)


    label = QLabel( splash );
    label.setWordWrap( True );
    label.move(30,30)
    label.setStyleSheet(" color: rgb(0, 100, 200); font-size: 30pt; ")
    label.setText( str(int(100*score))+"%" + " " + classification );

    splash.setAttribute(Qt.WA_NoSystemBackground)
    splash.move(x,y)
    splash.show()
    return splash
