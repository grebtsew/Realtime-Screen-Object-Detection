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
MAX_BOX_AREA = 1000000 # pixels^2
PRECISION = 0.6 # 60 % detection treshhold
MAX_DETECTION = 5
WIDTH = 1920
HEIGTH = 1080

# Main start here
if __name__ == "__main__":
    f = Figlet(font='slant')
    print (f.renderText('Realtime Screen stream with Ai detetion Overlay'))
    print("This program starts several threads that stream pc screen and" +
     "run object detection on it and show detections with PyQt5 overlay.")

    print("Starting Program...")

    shared_variables = Shared_Variables()
    shared_variables.height = HEIGTH
    shared_variables.width = WIDTH
    detection_thread = Obj_Detection( id = 0, shared_variables=shared_variables).start()
    print("All threads started, will take a few seconds to load model, enjoy!")

    print()
    print("----- Settings -----")
    print("Max box size : "+ str(MAX_BOX_AREA))
    print("Detection precision treshhold : " + str(100*PRECISION)+"%")
    print("Max amount of detection : "+ str(MAX_DETECTION))
    print("Screen size : " + str(WIDTH) +"x"+str(HEIGTH))
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
    try:
        k = 0
        list = []
        while True:
            if shared_variables.boxes is not None:
                 # paint result here!
                boxes = np.squeeze(shared_variables.boxes[0])
                scores = np.squeeze(shared_variables.boxes[1])
                classification = np.squeeze(shared_variables.boxes[2])

                k = k+1
                if k == MAX_DETECTION: # clear detections more often
                    k = 0
                    list = []

                # loop through all detections
                for i in range(0,len(np.squeeze(shared_variables.boxes[0]))):
                    x = int(shared_variables.width*boxes[i][1])
                    y = int(shared_variables.height*boxes[i][0])
                    w = int(shared_variables.width*(boxes[i][3]-boxes[i][1]))
                    h = int(shared_variables.height*(boxes[i][2]-boxes[i][0]))
                    c = ""

                    # Check category in bounds
                    if len(shared_variables.categorylist) >= classification[i]:
                        c = str(shared_variables.categorylist[int(classification[i]-1)]['name'])

                    if scores[i] > PRECISION: # precision treshhold
                        if w*h < MAX_BOX_AREA : # max box size check
                            list.append(screen_overlay_handler.create_box_with_score_classification(scores[i],c,x,y,w,h))

                #    time.sleep(0.1) might want to sleep if crash!

            else:
                time.sleep(0.1)
    except KeyboardInterrupt:
        pass


    # Stop everything here
    sys.exit(app.exec_())
    shared_variables.stream_running = False
    shared_variables.detection_running = False
