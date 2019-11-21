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

def create_fancy_tracking_box(index,score, classification, shared_variables, x,y,width,height):
    # Fancy box with tracking capeabilities
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

    label = QLabel( splash )
    label.setWordWrap( True )
    label.move(30,30)
    label.setStyleSheet(" color: rgba(0, 100, 200); font-size: 15pt; ")
    label.setText( str(int(100*score))+"%" + " " + classification );

    splash.setAttribute(Qt.WA_NoSystemBackground)
    splash.move(x,y)
    splash.show()

    tracking_thread = Tracking( index ,splash,(x,y,width,height),shared_variables)
    tracking_thread.start()

    shared_variables.tracking_list.append(tracking_thread)
    return splash



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


    def __init__(self, score, classification, shared_variables, box, *args, **kwargs):
        super(TrackingBox, self).__init__(*args, **kwargs)
        self.shared_variables = shared_variables
        self.counter = 0
        self.x = box[0]
        self.y = box[1]
        self.width = box[2]
        self.height = box[3]
        self.splash_pix = QPixmap(self.width, self.height)
        self.score = score
        self.classification = classification

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

        label.setText( str(int(100*score))+"%" + " " + classification );
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.move(self.x,self.y)
        self.show()

        self.tracking = Tracking( (self.x,self.y,self.width,self.height),self.shared_variables)


        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.timer = QTimer()
        self.timer.setInterval(10)
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
        label.setText( str(int(100*self.score))+"%" + " " + self.classification );

    def get_box(self):
        return self.tracking.box

    def tracking_update(self):

        self.tracking.run()
        self.move(self.tracking.box[0], self.tracking.box[1])
        self.repaint_size(self.tracking.box[2], self.tracking.box[3])
    #    self.counter += 1
    #    print(self.tracking.box, self.counter)

        if(not self.tracking.running ):
            self.hide()
            self.timer.stop()
            sys.exit(app.exec_())



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
