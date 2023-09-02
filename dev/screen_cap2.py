import numpy as np
import cv2
from mss import mss
from PIL import Image

bbox = {'top': 0, 'left': 0, 'width': 1920, 'height': 1080}

sct = mss()

while 1:

    sct_img = sct.grab(bbox)
    cv2.imshow('screen', np.array(sct_img))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
