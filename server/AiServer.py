import time
from threading import Thread, Event
import socket
import cv2
import pickle
import struct
import logging
from ml.torch import yolo

"""
COPYRIGHT @ Grebtsew 2019

AiServer receives a couple of connections, reads images from incoming streams
and send detections to the QtServer
"""

QtServer_address= [["127.0.0.1",8081]]

class AiServer(Thread):
    HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
    PORT = 8585        # Port to listen on (non-privileged ports are > 1023)

    def __init__(self):
        super(AiServer, self).__init__()
        logging.info("Tensorflow Server started at ", self.HOST, self.PORT)
        # Start detections
        self.ai_thread = yolo.YOLO()
        # Setup output socket
        logging.debug("Ai Server try connecting to Qt Server ", QtServer_address[0][0],QtServer_address[0][1])
        self.outSocket = socket.socket()
        self.outSocket.connect((QtServer_address[0][0],QtServer_address[0][1]))
        logging.debug("SUCCESS : Ai Server successfully connected to Qt Server!", )

    def handle_connection(self, conn):
        with conn:
            data = b""
            payload_size = struct.calcsize(">L")

            while True:
                # Recieve image package size
                while len(data) < payload_size:
                    logging.debug("Recv: {}".format(len(data)))
                    data += conn.recv(4096)

                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack(">L", packed_msg_size)[0]

                logging.debug("msg_size: {}".format(msg_size))

                # Recieve image
                while len(data) < msg_size:
                    data += conn.recv(4096)
                frame_data = data[:msg_size]
                data = data[msg_size:]

                # Decode image
                frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

                # do detetions
                # TODO:
                #self.ai_thread.frame = frame
                #self.ai_thread.run_async()
                #detect_res = self.ai_thread.get_result()

                # send detection result to QtServer
                if detect_res is not None:
                    self.send(detect_res)


    def send(self, data):
        self.outSocket.sendall(pickle.dumps(data))

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as inSocket:
            inSocket.bind((self.HOST, self.PORT))
            inSocket.listen()
            while True:
                conn, addr = inSocket.accept()
                Thread(target=self.handle_connection, args=(conn,)).start()


if __name__ == '__main__':
    aiserver = AiServer().start()
