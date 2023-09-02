import numpy as np
import cv2

kalman = cv2.KalmanFilter(4, 2, 0)
kalman.measurementMatrix = np.array([[1,0,0,0],
                                     [0,1,0,0]],np.float32)

kalman.transitionMatrix = np.array([[1,0,1,0],
                                    [0,1,0,1],
                                    [0,0,1,0],
                                    [0,0,0,1]],np.float32)

kalman.processNoiseCov = np.array([[1,0,0,0],
                                   [0,1,0,0],
                                   [0,0,1,0],
                                   [0,0,0,1]],np.float32) * 0.03

measurement = np.array((2,1), np.float32)
prediction = np.zeros((2,1), np.float32)

i = 0
x = 0
while True:
    current_measurement = np.array([[np.float32(i)], [np.float32(x)]])
    kalman.correct(current_measurement)
    prediction = kalman.predict()
    print(current_measurement)
    print(prediction)

    if i% 6 == 0:
        i -= 5
    if i % 2 == 0:
        i+=1
    i+=1
