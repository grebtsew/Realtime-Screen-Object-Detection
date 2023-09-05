#import torch
#from pathlib import Path
#import os
from ml.torch import torch_detector as td
from ultralytics import YOLO as y
import logging

class YOLO(td.TorchDetector):
    def __init__(self, shared_variables):
        
        super().__init__(shared_variables)
        self.shared_variables = shared_variables

    def download_model(self):
        #...
        pass

    def load_model(self):
        # Load model
        self.model = y('yolov8n.pt')  
        # YOLOv5-specific loading logic

    def predict(self):
        if self.shared_variables.OutputFrame is not None:
            frame = self.shared_variables.OutputFrame
            logging.debug("HERE")
            if( frame is not None):
                image = frame
                results = self.model(image)
                logging.debug(results)
                # Display the results
                results.show()

                # Access detected objects and their attributes
                detected_objects = results.pred[0]
                for obj in detected_objects:
                    logging.debug(f"Class: {obj[5]}, Confidence: {obj[4]}")
                
                # YOLOv5 specific prediction logic
                #prediction = super().predict(image)
                # Post-process YOLOv5 predictions
                # Implement your YOLOv5 post-processing here

                logging.debug(f"YOLOv5 prediction results: {results}")
                return results
        else:
            logging.debug("is nune")
