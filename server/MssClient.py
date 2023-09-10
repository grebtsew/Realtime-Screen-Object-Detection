import threading
from QtServer import QtServer
import socket
from mss import mss
from PIL import Image
import cv2
import numpy as np
import pickle
import struct
import time
import logging

"""
COPYRIGHT @ Grebtsew 2019

This Client Creates connections to servers in server_list and send images
to each server then recieve result and display images
"""

server_list= [["127.0.0.1",8585]]
QtServer_address= [["127.0.0.1",8081]]
image_size_treshhold = 720
screensize = (1920, 1080)

class MssClient(threading.Thread):
    """
    This client sends images for detection server
    """

    def __init__(self, address,port):
        super(MssClient,self).__init__()
        self.address = address
        self.port = port
        self.s = socket.socket()
        #self.demo_start_tfserver()
        logging.info("MSS Client trying to connect to Tensorflow Server ", self.address, self.port)
        self.s.connect((self.address,self.port))
        logging.info("SUCCESS : Mss Client successfully connected to Tensorflow Server!")
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def demo_start_tfserver(self):
        from TfServer import TfServer
        TfServer().start()

    def send(self):
        result, frame = cv2.imencode('.jpg', self.image, self.encode_param)

        data = pickle.dumps(frame, 0)
        size = len(data)
        logging.debug("Sending Image of size ", size)
        self.s.sendall(struct.pack(">L", size) + data)

    def run(self):
        self.send()

def downscale(image):
    height, width, channel = image.shape

    if height > image_size_treshhold:
        scale = height/image_size_treshhold

        image = cv2.resize(image, (int(width/scale), int(height/scale)))

    return image, scale



if __name__ == '__main__':

    image = None

    # Start Create connections
    clientlist = []
    for server in server_list:
        clientlist.append(MssClient(server[0],server[1]))

    # create mss
    sct = mss()
    monitor = {'top': 0, 'left': 0, 'width': screensize[0], 'height': screensize[1]}

    # start loop
    while True:
        # Recieve Image
        image = Image.frombytes('RGB', (screensize[0], screensize[1]), sct.grab(monitor).rgb)
        image = np.array(image)
        # Rescale Image
        image, scale = downscale(image)

        # async send image to all servers
        for server in clientlist:
            server.image = image
            server.send()
