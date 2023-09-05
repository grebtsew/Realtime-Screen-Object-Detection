"""
Class for specific usage of tensorflow 2.X
"""
from ml import detector as d

import tensorflow as tf
import keras

class TFDetector(d.Detector):
    def __init__(self):
        self.model = None

    def download_model(self):
        # Initialize TensorFlow specific setup here
        tf.compat.v1.enable_eager_execution()

    def load_model(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, image):
        # Implement TensorFlow specific prediction logic here
        prediction = self.model.predict(image)
        return prediction
