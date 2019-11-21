'''
A simple object detection implementation
'''

import math

from math import hypot
import tensorflow as tf
from utils import label_map_util
import time
import numpy as np
from threading import Thread
import os
import screen_overlay_handler

class Obj_Detection(Thread):

    MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    PATH_TO_CKPT = 'models/' + MODEL_NAME + '/frozen_inference_graph.pb'
    # List of the strings that is used to add correct label for each box.
    CWD_PATH = os.getcwd()
    PATH_TO_LABELS = os.path.join(CWD_PATH,'object_detection', 'data', 'mscoco_label_map.pbtxt')
    NUM_CLASSES = 90
    boxes = None

    def __init__(self, id, model = 'ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb', name=None, shared_variables = None ):
        Thread.__init__(self)
        self.name = name
        self.shared_variables = shared_variables
        self.id = id

    def load_modell(self):
        # Load modell
        print("Loading modell")
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        return detection_graph

    def distance_between_boxes(self, box1, box2):
        return int(abs(math.hypot(box2[0]-box1[0], box2[1]-box1[1])))

    def detection_exist(self, tracking_list, box):

        for tracking_box in tracking_list:
            if(self.distance_between_boxes(tracking_box.get_box(), box)) < 1000:
                return True
        return False


    def create_new_tracking_box(self, scores,c, shared_variables, box):
        shared_variables.trackingboxes.append(screen_overlay_handler.TrackingBox(scores, c,shared_variables, box))


    def run(self):
        detection_graph = self.load_modell()
        label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.NUM_CLASSES, use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
        self.shared_variables.categorylist = categories
        self.shared_variables.category_max = self.NUM_CLASSES
        self.shared_variables.category_index = category_index

        sess = tf.Session(graph=detection_graph)

        self.shared_variables.detection_ready = True # activate rest of the program

        print("Starting detection")
        while self.shared_variables.detection_running:
            if self.shared_variables.OutputFrame is not None:
                frame = self.shared_variables.OutputFrame

                if( frame is not None):
                    image_np = frame
                    # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                    image_np_expanded = np.expand_dims(image_np, axis=0)
                    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                    # Each box represents a part of the image where a particular object was detected.
                    boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

                    # Each score represent how level of confidence for each of the objects.
                    # Score is shown on the result image, together with the class label.
                    scores = detection_graph.get_tensor_by_name('detection_scores:0')
                    classes = detection_graph.get_tensor_by_name('detection_classes:0')

                    num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                    # Actual detection.
                    self.shared_variables.boxes = sess.run(
                      [boxes, scores, classes, num_detections],
                      feed_dict={image_tensor: image_np_expanded})

                     # paint result here!
                    boxes = np.squeeze(self.shared_variables.boxes[0])
                    scores = np.squeeze(self.shared_variables.boxes[1])
                    classification = np.squeeze(self.shared_variables.boxes[2])

                    # loop through all detections
                    for i in range(0,len(np.squeeze(self.shared_variables.boxes[0]))):
                        x = int(self.shared_variables.width*boxes[i][1])
                        y = int(self.shared_variables.height*boxes[i][0])
                        w = int(self.shared_variables.width*(boxes[i][3]-boxes[i][1]))
                        h = int(self.shared_variables.height*(boxes[i][2]-boxes[i][0]))
                        c = ""

                        # Check category in bounds
                        if len(self.shared_variables.categorylist) >= classification[i]:
                            c = str(self.shared_variables.categorylist[int(classification[i]-1)]['name'])

                        if len(self.shared_variables.SHOW_ONLY) > 0: # dont show wrong items
                            if not self.shared_variables.SHOW_ONLY.__contains__(c):
                                continue

                        if scores[i] > self.shared_variables.PRECISION: # precision treshhold
                            if w*h < self.shared_variables.MAX_BOX_AREA : # max box size check

                                if(not self.detection_exist(self.shared_variables.trackingboxes, (x,y,w,h))): # see if tracking box already exist for this detection
                                #index = len(self.shared_variables.splash_list)
                                #self.create_new_tracking_box(scores[i],c,self.shared_variables,(x,y,w,h))
                                    self.shared_variables.create_queue.append((scores[i],c,(x,y,w,h)))
                    
                    time.sleep(1)
