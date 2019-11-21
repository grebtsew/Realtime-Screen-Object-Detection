from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time
import traceback, sys
# Tracking thread

# imports
from math import hypot
import math
import cv2
import sys
import threading
import datetime

# Tracking
# Class that handles tracking thread
#
class Tracking():
    tracker_test = None
    tracker = None
    frame = None
    running = True

    fail_counter = 0

    start_time = None
    end_time = None
    first_time = True

    # Initiate thread
    # parameters name , shared_variables reference
    #
    def __init__(self,   box,  shared_variables):
        threading.Thread.__init__(self)
        self.box = box
        self.shared_variables = shared_variables


    # Run
    # Thread run function
    #
    def run(self):

        self.frame = self.shared_variables.frame


        if self.frame is not None:
            if self.first_time:
                self.update_custom_tracker()
                self.first_time = False
            self.object_custom_tracking()



    # Create_custom_tracker
    #
    # Create custom tracker, can chage tracking method here
    # will need cv2 and cv2-contrib to work!
    #
    def create_custom_tracker(self):
        #higher object tracking accuracy and can tolerate slower FPS throughput
        #self.tracker = cv2.TrackerCSRT_create()
        #faster FPS throughput but can handle slightly lower object tracking accuracy
        #self.tracker = cv2.TrackerKCF_create()
        #MOSSE when you need pure speed
        self.tracker = cv2.TrackerMOSSE_create()

    # Update_custom_tracker
    #
    # Set and reset custom tracker
    #
    def update_custom_tracker(self):
        self.create_custom_tracker()

        self.tracker_test = self.tracker.init( self.frame, self.box)

    def distance_between_boxes(self, box1, box2):
        return int(abs(math.hypot(box2[0]-box1[0], box2[1]-box1[1])))

    def get_box(self):
        return self.box

    # Object_Custom_tracking
    #
    # This function uses the OpenCV tracking form uncommented in update_custom_tracking
    #
    def object_custom_tracking(self):

    # Calculate
        self.tracker_test, box = self.tracker.update(self.frame)
    # Update tracker box
        if self.tracker_test:
            self.box = box
            self.fail_counter = 0

        else:
            self.fail_counter+=1
            if(self.fail_counter > 5): # missed five frames
                self.running = False

'''
COPYRIGHT @ Grebtsew 2019

This file contains a shared variables class and a mss screen stream capture class
'''


# Shared variables between threads
from mss import mss
from PIL import Image
from threading import Thread

import numpy as np
import cv2
import time

# Global shared variables
# an instace of this class share variables between system threads
class Shared_Variables():

    _initialized = 0
    width, height = 1920, 1080
    detection_ready = False
    category_index = None
    OutputFrame = None
    frame = None
    boxes = None
    categorylist = []
    category_max = None
    stream_running = True
    detection_running = True
    splash_list = []
    move_queue = []
    resize_queue = []
    create_queue = []
    remove_queue = []
    tracking_list = []

    def __init__(self):
        Thread.__init__(self)
        self._initialized = 1

        Screen_Streamer(shared_variables=self).start()

class Screen_Streamer(Thread):
    def __init__(self, shared_variables = None ):
        Thread.__init__(self)
        self.shared_variables = shared_variables


    def downscale(self, image):
        image_size_treshhold = 720
        height, width, channel = image.shape

        if height > image_size_treshhold:
            scale = height/image_size_treshhold

            image = cv2.resize(image, (int(width/scale), int(height/scale)))

        return image, scale


    def run(self):
        sct = mss()
        monitor = {'top': 0, 'left': 0, 'width': self.shared_variables.width, 'height': self.shared_variables.height}

        while self.shared_variables.stream_running:

            #if self.shared_variables.detection_ready:
            img = Image.frombytes('RGB', (self.shared_variables.width, self.shared_variables.height), sct.grab(monitor).rgb)
            #cv2.imshow('test', np.array(img))
            self.shared_variables.frame = np.array(img)
            self.shared_variables.OutputFrame, scale = self.downscale(np.array(img))
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done



class TrackingBox(QSplashScreen):
    splash_pix = None


    def __init__(self, shared_variables, box, *args, **kwargs):
        super(TrackingBox, self).__init__(*args, **kwargs)
        self.shared_variables = shared_variables
        self.counter = 0
        self.x = box[0]
        self.y = box[1]
        self.width = box[2]
        self.height = box[3]


        self.splash_pix = QPixmap(self.width, self.height)

        self.setWindowFlag(Qt.WindowStaysOnTopHint)

        painter = QPainter(self.splash_pix)
        painter.setPen(QPen(Qt.blue,  10, Qt.SolidLine))
        path = QPainterPath()

        path.addRoundedRect(QRectF(0+10,0+10,self.width-20,self.height-20), 30, 30);
        painter.drawPath(path);
        painter.end()

        self.setPixmap(self.splash_pix)
        self.setWindowOpacity(1)
        self.setAttribute(Qt.WA_TranslucentBackground)

        label = QLabel( self )
        label.setWordWrap( True )
        label.move(30,30)
        label.setStyleSheet(" color: rgba(0, 100, 200); font-size: 15pt; ")

        #label.setText( str(int(100*score))+"%" + " " + classification );
        label.setText("hdjasda")
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.move(self.x,self.y)
        self.show()

        self.tracking = Tracking( (self.x,self.y,self.width,self.height),self.shared_variables)


        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.tracking_update)
        self.timer.start()

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            time.sleep(0.1)
            progress_callback.emit(n*100/4)

        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

    def repaint_size(self, width, height):
        self.splash_pix = QPixmap(width, height)

        painter = QPainter(self.splash_pix)
        painter.setPen(QPen(Qt.blue,  10, Qt.SolidLine))
        path = QPainterPath()

        path.addRoundedRect(QRectF(0+10,0+10,width-20,height-20), 30, 30);
        painter.drawPath(path);
        painter.end()

        self.setPixmap(self.splash_pix)

        label = QLabel( self )
        label.setWordWrap( True )
        label.move(30,30)
        label.setStyleSheet(" color: rgba(0, 100, 200); font-size: 15pt; ")

    def get_box():
        return self.tracking.box

    def tracking_update(self):
        self.tracking.run()
        self.repaint_size(self.tracking.box[2], self.tracking.box[3])
        self.move(self.tracking.box[0], self.tracking.box[1])
        print(self.tracking.box)

        if(not self.tracking.running ):
            self.hide()
            self.timer.stop()


    def recurring_timer(self):
        self.counter +=1
        #self.repaint_size(self.counter, self.counter)

        self.move(self.counter, self.counter)


HEIGHT = 1080
WIDTH = 1920
shared_variables = Shared_Variables()
shared_variables.height = HEIGHT
shared_variables.width = WIDTH
app = QApplication([])
time.sleep(3)
list = []
list.append( TrackingBox(shared_variables, [800,800,200,200]))
list.append(TrackingBox(shared_variables, [500,800,200,200]))
#list.append(TrackingBox(shared_variables, [500,500,200,200]))
#list.append(TrackingBox(shared_variables, [800,500,200,200]))

app.exec_()
