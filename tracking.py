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
        self.tracker = cv2.TrackerKCF_create()
        #MOSSE when you need pure speed
        #self.tracker = cv2.TrackerMOSSE_create()

    # Update_custom_tracker
    #
    # Set and reset custom tracker
    #
    def update_custom_tracker(self):
        self.create_custom_tracker()

        self.tracker_test = self.tracker.init( self.frame, self.box)

#    def distance_between_boxes(self, box1, box2):
#        return int(abs(math.hypot(box2[0]-box1[0], box2[1]-box1[1])))

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
#                print("done")
