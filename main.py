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
PRECISION = 0.6 # 60 % detection treshhold
MAX_DETECTION = 5
WIDTH = 1920
HEIGHT = 1080
SHOW_ONLY = ["person"]

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


    def __init__(self):
        super(MainGUI, self).__init__()

        self.initiate_shared_variables()

        # Create detection and load model
        self.detection = Detection(shared_variables = self.shared_variables)

        self.threadpool = QThreadPool()

        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.print_output)
        self.timer.start()


        # Start Detection thread
        self.start_worker()

    def execute_this_fn(self, progress_callback):
        while True:
            time.sleep(2) # how often we should detect stuff
            progress_callback.emit(self.detection.run()) # detect and emits boxes!
        return "Done"

    def create_tracking_boxes(self, boxes):
        print("got detection now create trackerbox")
        print(boxes)
        for box in boxes:
            self.shared_variables.list.append(TrackingBox(self.shared_variables, box[0],box[1],box[2]))

    def print_output(self):
        #print("ddd")
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
    print("Screen size : " + str(WIDTH) +"x"+str(HEIGHT))
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
