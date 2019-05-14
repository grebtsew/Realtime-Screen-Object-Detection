import numpy as np
import cv2
from mss import mss
from PIL import Image

sct = mss()

while 1:
    w, h = 800, 640
    monitor = {'top': 0, 'left': 0, 'width': w, 'height': h}
    img = Image.frombytes('RGB', (w,h), sct.grab(monitor).rgb)
    cv2.imshow('test', np.array(img))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
