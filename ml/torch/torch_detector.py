"""
Class for specific usage of tensorflow 2.X
"""
from detector import Detector

import torch 

class TorchDetector(Detector):
    def __init__(self):
        self.model = None

    def download_model(self):
        # Initialize TensorFlow specific setup here
        pass

    def load_model(self, model_path):
        pass

    def predict(self, image):
        # Implement TensorFlow specific prediction logic here
        pass