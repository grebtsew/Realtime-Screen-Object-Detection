'''
COPYRIGHT @ Grebtsew 2019

A simple object detection implementation
'''
import sys
sys.path.insert(0,'..')

import tensorflow as tf
from utils import label_map_util
import numpy as np
from threading import Thread
import os
import screen_overlay_handler


class Obj_Detection(Thread):
    result = None
    MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    PATH_TO_CKPT = '../models/' + MODEL_NAME + '/frozen_inference_graph.pb'
    # List of the strings that is used to add correct label for each box.
    CWD_PATH = os.path.dirname(os.getcwd())
    PATH_TO_LABELS = os.path.join(CWD_PATH,'object_detection', 'data', 'mscoco_label_map.pbtxt')
    NUM_CLASSES = 90

    def __init__(self ):
        Thread.__init__(self)
        self.detection_graph = self.load_model()

        #self.shared_variables.categorylist = categories
        #self.shared_variables.category_max = self.NUM_CLASSES
        #self.shared_variables.category_index = category_index

        self.sess = tf.Session(graph=self.detection_graph)
        print("Model successfully loaded! Detection Active!")


    def load_model(self):
        # Load model
        print("Loading model")
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        return detection_graph

    def run_async(self):
        thread = Thread(target=self.run).start()

    def get_result(self):
        # Deadlock warnings here but we will always only use one detection per frame so should be fine
        while self.result is None:
            pass
        return self.result

    def run(self):
        if self.frame is not None:
            image_np = self.frame
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

            num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

            self.result = self.sess.run(
              [boxes, scores, classes, num_detections],
              feed_dict={image_tensor: image_np_expanded})

            # Actual detection.
            return self.result
        else:
            return None
