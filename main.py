import time

import cv2

from communication import sendNum
import numpy as np

from camera import webcam
from model import pose_estimator
from seat_detector import SeatDetector
from communication import sendNum
#from model import level_regressor
#from model import level_inference

#camera = webcam.WebcamCamera(1)
#pose = pose_estimator.PoseEstimator()
#img = camera.take_photo()

if __name__ == '__main__' :
    mySeatDetector = SeatDetector()
    if mySeatDetector.seat_check(mode = 'exist') :
        time.sleep(3)
        sendNum(10)
