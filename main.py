'''
MAIN
COPYRIGHT @ Grebtsew 2019

This is main function, used to start instances of the full program
'''

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow

from utils.shared_variables import Shared_Variables
from utils import screen_overlay_handler
from utils.ThreadPool import *
from ml import detector

import time

from pyfiglet import Figlet

import logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging threshold to DEBUG (or another level)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='last-run.log',  # Log messages to a file (optional)
    filemode='w'  # Append mode for the log file (optional)
)
console_handler = logging.StreamHandler()  # Use the default stream (sys.stdout)

# Create a formatter for the console handler (optional)
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Add the console handler to the root logger
root_logger = logging.getLogger()
root_logger.addHandler(console_handler)

# Create a logger for your module
logger = logging.getLogger('realtime-screen-object-detection.rsod')

# Change these variables if you want!
MAX_BOX_AREA = 100000000 # pixels^2
PRECISION = 0.7 # 60 % detection treshhold
MAX_DETECTION = 5
MAX_TRACKING_MISSES = 30
WIDTH = 1920
HEIGHT = 1080
SHOW_ONLY = ["person","Person"] # Start Empty, receive items to show
OFFSET = (0,0)
DETECTION_SIZE = 480
DETECTION_DURATION = 2
RESET_SHOW_ONLY_ON_START=False
HTTP_SERVER = False

class MainGUI(QMainWindow):

    def initiate_shared_variables(self):
        self.shared_variables = Shared_Variables()
        self.shared_variables.MAX_BOX_AREA = MAX_BOX_AREA
        self.shared_variables.PRECISION = PRECISION
        self.shared_variables.MAX_DETECTION = MAX_DETECTION
        self.shared_variables.WIDTH = WIDTH
        self.shared_variables.HEIGHT = HEIGHT
        self.shared_variables.SHOW_ONLY = SHOW_ONLY
        self.shared_variables.list = []
        self.shared_variables.OFFSET = OFFSET
        self.shared_variables.DETECTION_SIZE = DETECTION_SIZE
        self.shared_variables.DETECTION_DURATION = DETECTION_DURATION
        self.shared_variables.MAX_TRACKING_MISSES = MAX_TRACKING_MISSES
        self.shared_variables.HTTP_SERVER = HTTP_SERVER

        if RESET_SHOW_ONLY_ON_START:
            self.shared_variables.SHOW_ONLY = []

        # Start webserver
        if HTTP_SERVER:
            from server.http_server import HTTPserver
            HTTPserver(shared_variables=self.shared_variables).start()

    def __init__(self):
        super(MainGUI, self).__init__()

        self.initiate_shared_variables()

        # Create detection and load model
        self.detection_model = self.shared_variables.model(shared_variables = self.shared_variables)
        self.detection_model.download_model()
        self.detection_model.load_model()
        
        self.threadpool = QThreadPool()

        logging.info("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.print_output)
        self.timer.start()
        

        # Start Detection thread
        self.start_worker()

    def execute_this_fn(self, progress_callback):
        while True:
            
            if len(self.shared_variables.SHOW_ONLY) == 0:
                 # how often we should detect stuff
                pass
            else:
                logging.debug("Trigger Detection...")
                if self.shared_variables.OutputFrame is not None: # wait for the first frame
                    progress_callback.emit(self.detection_model.predict()) # detect and emits boxes!

            time.sleep(self.shared_variables.DETECTION_DURATION)

    def create_tracking_boxes(self, boxes):
        if len(boxes)> 0:
            logging.debug(f"got detection now create trackerbox: {boxes}")

        for box in boxes:
            if len(self.shared_variables.list) < MAX_DETECTION:
                self.shared_variables.list.append(screen_overlay_handler.TrackingBox(len(self.shared_variables.list), self.shared_variables, box[0],box[1],box[2]))

    def print_output(self):
        remove = []
        index = 0
        for box in self.shared_variables.list:
            if box.done:
                box.finish(self)
                remove.insert(0,index)
            index += 1

        for i in remove:
            del self.shared_variables.list[i]
            #logging.debug(self.shared_variables.list)
        
        
    def thread_complete(self):
        #logging.debug("Thread closed")
        pass

    def start_worker(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.progress.connect(self.create_tracking_boxes)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        # Execute
        self.threadpool.start(worker)

# Main start here
if __name__ == "__main__":
    f = Figlet(font='slant')
    logging.info (f.renderText('Realtime Screen stream with Ai detection Overlay'))
    logging.info("This program starts several threads that stream pc screen and" +
     "run object detection on it and show detections with PyQt5 overlay.")

    logging.info("Starting Program...")
    logging.info("All threads started, will take a few seconds to load model, enjoy!")

    logging.info("")
    logging.info("----- Settings -----")
    logging.info("Max box size : "+ str(MAX_BOX_AREA))
    logging.info("Detection precision treshhold : " + str(100*PRECISION)+"%")
    logging.info("Max amount of detection : "+ str(MAX_DETECTION))
    logging.info("Max amount of tracking misses : "+ str(MAX_TRACKING_MISSES))
    logging.info("Do detections every : "+str(DETECTION_DURATION) + " second")
    logging.info("Rescale image detection size : " +str(DETECTION_SIZE))
    logging.info("Classifications : " + str(SHOW_ONLY) + " * if empty all detections are allowed.")
    logging.info("Screen size : " + str(WIDTH) +"x"+str(HEIGHT))
    logging.info("Screen offset : "+str(OFFSET))
    logging.info("Activate HTTPserver : " + str(HTTP_SERVER))
    logging.info("")

    logging.info("")
    logging.info("----- Usage -----")
    logging.info("Exit by typing : 'ctrl+c'")
    logging.info("")

    logging.info("")
    logging.info("Realtime-Screen-stream-with-Ai-detection-Overlay Copyright (C) 2019  Daniel Westberg")
    logging.info("This program comes with ABSOLUTELY NO WARRANTY;")
    logging.info("This is free software, and you are welcome to redistribute it under certain conditions;")
    logging.info("")
    
    app = QApplication([])

    MainGUI()

    app.exec_()
