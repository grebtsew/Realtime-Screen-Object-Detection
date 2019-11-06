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
    boxes = None
    categorylist = []
    category_max = None
    stream_running = True
    detection_running = True

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
            if self.shared_variables.detection_ready:
                img = Image.frombytes('RGB', (self.shared_variables.width, self.shared_variables.height), sct.grab(monitor).rgb)
                #cv2.imshow('test', np.array(img))
                self.shared_variables.OutputFrame, scale = self.downscale(np.array(img))
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break
            else:
                time.sleep(0.1)
