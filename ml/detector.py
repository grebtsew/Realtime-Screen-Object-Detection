"""
Abstract Object Detector Class
"""
import math

from utils import screen_overlay_handler
from abc import ABC, abstractmethod

class Detector(ABC):

    def __init__(self, shared_variables) -> None:
        super().__init__(shared_variables)
        
        self.shared_variables = shared_variables
        self.id = id

    def distance_between_boxes(self, box1, box2):
        return int(abs(math.hypot(box2[0]-box1[0], box2[1]-box1[1])))

    def detection_exist(self, tracking_list, box):
        for tracking_box in tracking_list:
            if(self.distance_between_boxes(tracking_box.get_box(), box)) < 100:
                return True
        return False

    def create_new_tracking_box(self, scores,c, shared_variables, box):
        shared_variables.trackingboxes.append(screen_overlay_handler.TrackingBox(scores, c,shared_variables, box))

    @abstractmethod
    def download_model(self, url):
        pass

    @abstractmethod
    def load_model(self, model_path):
        pass

    @abstractmethod
    def predict(self, image):
        pass
