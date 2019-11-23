from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from tracking import Tracking

import sys
import time

'''
COPYRIGHT @ Grebtsew 2019

This file contains functions for showing overlay detections
'''


class TrackingBox(QSplashScreen):
    splash_pix = None


    def __init__(self, shared_variables, score, classification, box, *args, **kwargs):
        super(TrackingBox, self).__init__(*args, **kwargs)
        self.shared_variables = shared_variables
        self.counter = 0
        self.x = box[0]
        self.y = box[1]
        self.width = box[2]
        self.height = box[3]


        self.splash_pix = QPixmap('./images/box2.png')
        self.splash_pix = self.splash_pix.scaled(self.width,self.height);
        self.setPixmap(self.splash_pix)

        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_NoSystemBackground)

        label = QLabel( self )
        label.setWordWrap( True )
        label.move(30,30)
        label.setStyleSheet(" color: rgba(0, 100, 200); font-size: 15pt; ")

        label.setText( str(int(100*score))+"%" + " " + classification );
        self.move(self.x,self.y)
        self.show()

        self.tracking = Tracking( (self.x,self.y,self.width,self.height),self.shared_variables)

        self.threadpool = QThreadPool()

        print("New Box Created at ",self.x,self.y, " Size ", self.width, self.height)

        self.start_worker()

    def progress_fn(self, n):
        #print("%d%% done" % n)
        pass

    def execute_this_fn(self, progress_callback):
        self.tracking.run()
        return "Done."

    def print_output(self, s):
        self.repaint_size(self.tracking.box[2], self.tracking.box[3])
        self.move(self.tracking.box[0], self.tracking.box[1])
        #next tracking


    def thread_complete(self):
        #print("THREAD COMPLETE!")
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
        #self.setPixmap(self.splash_pix)

    def get_box():
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
    label.setStyleSheet(" color: rgba(0, 100, 200); font-size: 30pt; ")
    label.setText( str(int(100*score))+"%" + " " + classification );


    splash.setAttribute(Qt.WA_NoSystemBackground)
    splash.move(x,y)
    splash.show()
    return splash






"""
For Testing
"""
#app = QApplication(sys.argv) # create window handler
#print("do the overlay")
#screen_overlay_handler.create_box(10,10,100,100)
#print("done")
#time.sleep(10)
#print("do the overlay")
#screen_overlay_handler.create_box(100,10,100,100)

#list = []
#list.append(create_fancy_box(100,10,100,100))
#time.sleep(2)
#list[0].hide()
#print("hiede")
#time.sleep(2)
#print("done")
