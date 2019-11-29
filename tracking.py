from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np
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
    first = True
    # Initiate thread
    # parameters name , shared_variables reference
    #
    def __init__(self,   box,  shared_variables):
        self.box = box
        self.shared_variables = shared_variables

        self.kalman = cv2.KalmanFilter(4, 2, 0)
        self.kalman.measurementMatrix = np.array([[1,0,0,0],
                                             [0,1,0,0]],np.float32)

        self.kalman.transitionMatrix = np.array([[1,0,1,0],
                                            [0,1,0,1],
                                            [0,0,1,0],
                                            [0,0,0,1]],np.float32)

        self.kalman.processNoiseCov = np.array([[1,0,0,0],
                                           [0,1,0,0],
                                           [0,0,1,0],
                                           [0,0,0,1]],np.float32) * 0.03


    # Run
    # Thread run function
    #
    def run(self):
        self.frame = self.shared_variables.OutputFrame

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
        #print(self.tracker_test, box, len(self.shared_variables.list))

        if self.tracker_test:
            #cv2.waitKey(1)
            #cv2.imshow("test", self.frame)

            if self.first:
                A = self.kalman.statePost
                A[0:4] = np.array([[np.float32(box[0])], [np.float32(box[1])],[0],[0]])
                # A[4:8] = 0.0
                self.kalman.statePost = A
                self.kalman.statePre = A
                self.first = False

            current_measurement = np.array([[np.float32(box[0])], [np.float32(box[1])]])
            self.kalman.correct(current_measurement)
            prediction = self.kalman.predict()
            #print(int(prediction[0]), int(prediction[1]))
            self.box = [int(prediction[0]), int(prediction[1]), box[2], box[3]]
            self.fail_counter = 0

        else:
            self.fail_counter+=1
            if(self.fail_counter > self.shared_variables.MAX_TRACKING_MISSES): # missed fifteen frames
                self.running = False

class MultiTracking():
    tracker_test = None
    tracker = None
    frame = None
    running = True

    fail_counter = 0

    def __init__(self, shared_variables):
        self.box = box
        self.shared_variables = shared_variables

    def run(self):
        self.frame = self.shared_variables.OutputFrame

        if self.frame is not None:
            if self.first_time:
                self.update_custom_tracker()
                self.first_time = False
            self.object_custom_tracking()

    def create_custom_tracker(self):
        self.Tracker = cv2.MultiTracker_create()

    def update_custom_tracker(self):
        self.create_custom_tracker()

        #self.tracker_test = self.tracker.init( self.frame, self.box)

    def get_box(self):
        return self.box

    def add_tracker(self, frame, box):
        trackerType = "CSRT"

        # Initialize MultiTracker
        for bbox in bboxes:
            self.tracker.add(createTrackerByName(trackerType), frame, box)

    def object_custom_tracking(self):
    # Calculate
        self.tracker_test, box = self.tracker.update(self.frame)
    # Update tracker box
        #print(self.tracker_test, box)
        if self.tracker_test:
            cv2.waitKey(1)
            cv2.imshow("test", self.frame)
            self.box = box
            self.fail_counter = 0


        else:
            self.fail_counter+=1
            if(self.fail_counter > 2): # missed five frames
                self.running = False
