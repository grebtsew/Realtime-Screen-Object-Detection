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
        
        # TODO: inherit this
        self.shared_variables.detection_ready=True



    def predict(self):
        image = self.shared_variables.OutputFrame
        
        results = self.model.predict(image)
        
        # Access detected objects and their attributes
        detected_objects = []
        
        

        for obj in results:
            classes = obj.names
            for i in range(len(obj.boxes.cls.tolist())):
                _box = obj.boxes.xywhn.tolist()[i]
                
                box = (_box[0],_box[1],_box[2],_box[3])
                
                score = obj.boxes.conf.tolist()[i]
                classification =  obj.boxes.cls.tolist()[i]   
                
                __box = obj.boxes.xywh.tolist()[i]

                # Apply filters
                
                
                if len(self.shared_variables.SHOW_ONLY )> 0:
                    if score >= self.shared_variables.PRECISION:
                        if classes[classification] in self.shared_variables.SHOW_ONLY:
                            if __box[2]*__box[3] <= self.shared_variables.MAX_BOX_AREA:
                                detected_objects.append((score,classes[classification], box))
                
                else:
                    if score > self.shared_variables.PRECISION :
                        if __box[2]*__box[3] <= self.shared_variables.MAX_BOX_AREA:
                            detected_objects.append((score,classes[classification], box))
                
        return detected_objects
    