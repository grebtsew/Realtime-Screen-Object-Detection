import threading

import sys
sys.path.insert(0,'..')

import os

from utils import label_map_util
from screen_overlay_handler import *
import socket
import pickle
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
import sys
import screen_overlay_handler

"""
COPYRIGHT @ Grebtsew 2019


QtServer recieves detection boxes and visualize them.
"""

MAX_DETECTION = 5
MAX_BOX_AREA = 1000000 # pixels^2
PRECISION = 0.6 # 60 % detection treshhold
MAX_DETECTION = 5
WIDTH = 1920
HEIGTH = 1080
SHOW_ONLY = ["person"]
BOX_VIS_TIME = 0.2 # in seconds

# Dont change these
list = []
queue = []
class QtServer(threading.Thread):
    """
    This server recieves boxes and shows them in pyqt5
    """

    def __init__(self, address, port):
        super(QtServer,self).__init__()
        self.address = address
        self.port = port
        self.categorylist = self.load_tf_categories()

    def load_tf_categories(self):
        self.NUM_CLASSES = 90
        CWD_PATH = os.path.dirname(os.getcwd())
        self.PATH_TO_LABELS = os.path.join(CWD_PATH,'object_detection', 'data', 'mscoco_label_map.pbtxt')
        self.label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        self.categories = label_map_util.convert_label_map_to_categories(self.label_map, max_num_classes=self.NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(self.categories)
        return self.categories

    def handle_connection(self, conn):
        with conn:
            while True:
                data = conn.recv(50000) # approx larger than the incoming tf result
                if not data:
                    break
                else:
                    try:
                        dict = pickle.loads(data)
                    except Exception:
                        continue # If for some reason not entire package is recieved!

                    boxes = np.squeeze(dict[0])
                    scores = np.squeeze(dict[1])
                    classification = np.squeeze(dict[2])
                    amount = np.squeeze(dict[3])

                    # loop through all detections
                    for i in range(0,len(boxes)):
                        # Calculate rescale rectangle
                        x = int(WIDTH*boxes[i][1])
                        y = int(HEIGTH*boxes[i][0])
                        w = int(WIDTH*(boxes[i][3]-boxes[i][1]))
                        h = int(HEIGTH*(boxes[i][2]-boxes[i][0]))
                        c = ""

                        # Check category in bounds
                        if len(self.categorylist) >= classification[i]:
                            c = str(self.categorylist[int(classification[i]-1)]['name'])

                        if len(SHOW_ONLY) > 0: # dont show wrong items
                            if not SHOW_ONLY.__contains__(c):
                                continue
                        if scores[i] > PRECISION: # precision treshold
                            if w*h < MAX_BOX_AREA : # max box size check
                                queue.append((scores[i], c,x,y,w,h)) # save all vis data in queue


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, self.port))
            s.listen()
            print("Qt Server started at ", self.address, self.port )
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_connection, args=(conn,)).start()

def show_rect(scores, c,x,y,w,h):
    list.append((screen_overlay_handler.create_box_with_image_score_classification("../images/square2.png",scores,c,x,y,w,h), time.time()))

def remove_old_detections():
    for box in list:
        if time.time() - box[1] > BOX_VIS_TIME:
            list.remove(box);

def paint_rects():
    if len(queue) > 0:
        for box in queue:
            show_rect(box[0],box[1],box[2],box[3],box[4],box[5])
        queue.clear()
    else:
        time.sleep(0.1)
        remove_old_detections()

if __name__ == '__main__':
    app = QApplication(sys.argv) # create window handler
    QtServer_address= [["127.0.0.1",8081]]
    qtserver = QtServer(QtServer_address[0][0],QtServer_address[0][1])
    qtserver.start()

    while True: # Paint all incoming boxes on MAIN thread (required!)
        paint_rects()
