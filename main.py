'''
MAIN
COPYRIGHT @ Grebtsew 2019

This is main function, used to start instances of the full program
'''

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow

from shared_variables import Shared_Variables
from detection import Detection
import screen_overlay_handler
from ThreadPool import *

import time
import sys
import numpy as np

from pyfiglet import Figlet

# Change these variables if you want!
MAX_BOX_AREA = 100000000 # pixels^2
PRECISION = 0.7 # 60 % detection treshhold
MAX_DETECTION = 5
MAX_TRACKING_MISSES = 30
WIDTH = 1920
HEIGHT = 1080
SHOW_ONLY = ["person"] # Start Empty, receive items to show
OFFSET = (0,0)
DETECTION_SIZE = 480
DETECTION_DURATION = 2
RESET_SHOW_ONLY_ON_START=False
HTTP_SERVER = False

class MainGUI(QMainWindow):

    def initiate_shared_variables(self):
        self.shared_variables = Shared_Variables()
        self.shared_variables.MAX_BOX_AREA = MAX_BOX_AREA
        self.shared_variables.PRECISION = PRECISION
        self.shared_variables.MAX_DETECTION = MAX_DETECTION
        self.shared_variables.WIDTH = WIDTH
        self.shared_variables.HEIGHT = HEIGHT
        self.shared_variables.SHOW_ONLY = SHOW_ONLY
        self.shared_variables.list = []
        self.shared_variables.OFFSET = OFFSET
        self.shared_variables.DETECTION_SIZE = DETECTION_SIZE
        self.shared_variables.DETECTION_DURATION = DETECTION_DURATION
        self.shared_variables.MAX_TRACKING_MISSES = MAX_TRACKING_MISSES
        self.shared_variables.HTTP_SERVER = HTTP_SERVER

        if RESET_SHOW_ONLY_ON_START:
            self.shared_variables.SHOW_ONLY = []

        # Start webserver
        if HTTP_SERVER:
            from http_server import HTTPserver
            HTTPserver(shared_variables=self.shared_variables).start()

    def __init__(self):
        super(MainGUI, self).__init__()

        self.initiate_shared_variables()

        # Create detection and load model
        self.detection = Detection(shared_variables = self.shared_variables)

        self.threadpool = QThreadPool()

        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        """
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.print_output)
        self.timer.start()
        """

        # Start Detection thread
        self.start_worker()

    def execute_this_fn(self, progress_callback):
        while True:
            if len(self.shared_variables.SHOW_ONLY) == 0:
                time.sleep(self.shared_variables.DETECTION_DURATION) # how often we should detect stuff
                
            else:
                #print("Detection...")
                time.sleep(self.shared_variables.DETECTION_DURATION) # how often we should detect stuff
                progress_callback.emit(self.detection.run()) # detect and emits boxes!
        return "Done"

    def create_tracking_boxes(self, boxes):
        #print("got detection now create trackerbox")
        #print(boxes)

        for box in boxes:
            if len(self.shared_variables.list) < MAX_DETECTION:
                self.shared_variables.list.append(screen_overlay_handler.TrackingBox(len(self.shared_variables.list), self.shared_variables, box[0],box[1],box[2]))

    def print_output(self):
        """
        remove = []
        index = 0
        for box in self.shared_variables.list:
            if box.done:
                box.finish(self)
                remove.insert(0,index)
            index += 1

        for i in remove:
            del self.shared_variables.list[i]
            print(self.shared_variables.list)
        """
        pass

    def thread_complete(self):
        #print("sss")
        pass

    def start_worker(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.progress.connect(self.create_tracking_boxes)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        # Execute

        self.threadpool.start(worker)

# Main start here
if __name__ == "__main__":
    f = Figlet(font='slant')
    print (f.renderText('Realtime Screen stream with Ai detetion Overlay'))
    print("This program starts several threads that stream pc screen and" +
     "run object detection on it and show detections with PyQt5 overlay.")

    print("Starting Program...")
    print("All threads started, will take a few seconds to load model, enjoy!")

    print()
    print("----- Settings -----")
    print("Max box size : "+ str(MAX_BOX_AREA))
    print("Detection precision treshhold : " + str(100*PRECISION)+"%")
    print("Max amount of detection : "+ str(MAX_DETECTION))
    print("Max amount of tracking misses : "+ str(MAX_TRACKING_MISSES))
    print("Do detections every : "+str(DETECTION_DURATION) + " second")
    print("Rescale image detection size : " +str(DETECTION_SIZE))
    print("Classifications : " + str(SHOW_ONLY) + " * if empty all detections are allowed.")
    print("Screen size : " + str(WIDTH) +"x"+str(HEIGHT))
    print("Screen offset : "+str(OFFSET))
    print("Activate HTTPserver : " + str(HTTP_SERVER))
    print()

    print()
    print("----- Usage -----")
    print("Exit by typeing : 'ctrl+c'")
    print()

    print("")
    print("Realtime-Screen-stream-with-Ai-detetion-Overlay Copyright (C) 2019  Daniel Westberg")
    print("This program comes with ABSOLUTELY NO WARRANTY;")
    print("This is free software, and you are welcome to redistribute it under certain conditions;")
    print("")

    app = QApplication([])

    MainGUI()

    app.exec_()
