'''
A simple object detection implementation
'''

import tensorflow as tf
from utils import label_map_util
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
