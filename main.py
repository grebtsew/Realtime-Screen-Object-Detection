'''
MAIN
COPYRIGHT @ Grebtsew 2019


This is main function, used to start instances of the full program
'''

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

from shared_variables import Shared_Variables
from obj_detection import Obj_Detection
import screen_overlay_handler

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
SHOW_ONLY = ["airplane"]

def create_new_tracking_box( scores,c, shared_variables, box):
    shared_variables.trackingboxes.append(screen_overlay_handler.TrackingBox(scores, c,shared_variables, box))


# Main start here
if __name__ == "__main__":
    f = Figlet(font='slant')
    print (f.renderText('Realtime Screen stream with Ai detetion Overlay'))
    print("This program starts several threads that stream pc screen and" +
     "run object detection on it and show detections with PyQt5 overlay.")

    print("Starting Program...")

    shared_variables = Shared_Variables()
    shared_variables.height = HEIGHT
    shared_variables.width = WIDTH
    detection_thread = Obj_Detection( id = 0, shared_variables=shared_variables).start()
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

    app = QApplication(sys.argv) # create window handler

    '''
    Show detection overlay work here!
    '''
    k = 0
    shared_variables.splash_list = []
    shared_variables.MAX_BOX_AREA = MAX_BOX_AREA
    shared_variables.PRECISION = PRECISION
    shared_variables.MAX_DETECTION = MAX_DETECTION
    shared_variables.WIDTH = WIDTH
    shared_variables.HEIGHT = HEIGHT
    shared_variables.SHOW_ONLY = SHOW_ONLY

    list = []
    while True:
        if len(shared_variables.create_queue) > 0:
            for box in shared_variables.create_queue:
                list.append(screen_overlay_handler.create_fancy_box(box[0],box[1],box[2][0],box[2][1],box[2][2],box[2][3]))
                print("created box")
            shared_variables.create_queue = []
        time.sleep(1)

    app.exec_()


    # Stop everything here
    sys.exit(app.exec_())
    shared_variables.stream_running = False
    shared_variables.detection_running = False
