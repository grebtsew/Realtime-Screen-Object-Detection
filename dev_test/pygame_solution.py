import pygame
import win32api
import win32con
import win32gui
import threading

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


class TrackingBox(threading.Thread):
    def __init__(self, shared_variables, box):
        threading.Thread.__init__(self)
        self.x = box[0]
        self.box = box
        self.y = box[1]
        self.width = box[2]
        self.height = box[3]
        self.shared_variables = shared_variables

        pygame.init()

        self.screen = pygame.display.set_mode((self.width, self.height),pygame.NOFRAME) # For borderless, use pygame.NOFRAME
        #done = False
        fuchsia = (255, 0, 128)  # Transparency color
        dark_red = (139, 0, 0)

        # Set window transparency color
        #hwnd = pygame.display.get_wm_info()["window"]
        #win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
        #                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        #win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

        #while not done:
        #    for event in pygame.event.get():
        #        print(event)
        #        if event.type == pygame.QUIT:
        #            done = True

        screen.fill(fuchsia)  # Transparent background
        pygame.draw.rect(screen, dark_red, pygame.Rect(0, 0, self.width, self.height), 10)
        pygame.display.update()


    def run(self):
        tracking = Tracking(self.box,self.shared_variables)

        while True:
            tracking.run()
            print(tracking.box)
            self.screen.resize(tracking.box[2],tracking.box[3])
            self.screen.move




if __name__ == '__main__':
    """
    """
    HEIGHT = 1080
    WIDTH = 1920
    shared_variables = Shared_Variables()
    shared_variables.height = HEIGHT
    shared_variables.width = WIDTH

    TrackingBox(shared_variables, (10,10,1000,1000)).start()
