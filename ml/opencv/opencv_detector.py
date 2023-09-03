"""
Class for specific usage of tensorflow 2.X
"""
from detector import Detector

import cv2

class OPENCVDetector(Detector):
    def __init__(self):
        self.model = None

    def download_model(self):
        # Initialize TensorFlow specific setup here
        #tf.compat.v1.enable_eager_execution()
        pass
    
    def load_model(self, model_path):
        #self.model = tf.keras.models.load_model(model_path)
        pass
        
    def predict(self, image):
        # Implement TensorFlow specific prediction logic here
        prediction = self.model.predict(image)
        return prediction
