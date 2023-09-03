import torch
import requests
from pathlib import Path

from torch_detector import TorchDetector

class YOLOv5(TorchDetector):
    def __init__(self, model_path, config_file):
        super().__init__()
        self.model_path = model_path
        self.config_file = config_file

    def setup(self):
        super().setup()
        # Add YOLOv5 specific setup here

    def load(self):
        model_path = "./models/yolov5s.pt"
        # Download if not exist:
        if not Path(model_path).is_file():
            model_url = "https://github.com/ultralytics/yolov5/releases/download/v5.0/yolov5s.pt"
            print(f"Downloading YOLOv5 model from {model_url}...")
            response = requests.get(model_url, stream=True)
            response.raise_for_status()
            with open(model_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Model downloaded to {model_path}")


        # Load model
        self.model = torch.hub.load("ultralytics/yolov5:master", "yolov5s", path=model_path)


        #super().load(self.model_path)
        # YOLOv5-specific loading logic

    def predict(self, image):
        results = self.model(image)

        # Display the results
        results.show()

        # Access detected objects and their attributes
        detected_objects = results.pred[0]
        for obj in detected_objects:
            print(f"Class: {obj[5]}, Confidence: {obj[4]}")
        
        # YOLOv5 specific prediction logic
        #prediction = super().predict(image)
        # Post-process YOLOv5 predictions
        # Implement your YOLOv5 post-processing here
        return results
