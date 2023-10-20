import time

import cv2

from communication.send_num import sendNum
import numpy as np

from camera.webcam import WebcamCamera
from model.pose_estimator import PoseEstimator
from model.level_regressor import LevelRegressor
from seat_detector.seat_detector import SeatDetector

#from model import level_regressor
#from model import level_inference

#camera = webcam.WebcamCamera(1)
#pose = pose_estimator.PoseEstimator()
#img = camera.take_photo()

class SeatBelt():
        
    def __init__(self):
        print("initializing...")
        self.level = 0
        self.seat_detector = SeatDetector()
        self.pose_estimator = PoseEstimator()
        self.level_regressor = LevelRegressor()
        self.webcam = WebcamCamera()

    def wait_to_sit(self):
        if self.seat_detection.is_sitting():
            time.sleep(3) # wait 3 sec to modify the level

    def system(self): # main working method

        while(True):
            # wait til the YOLO detect a person
            self.wait_to_sit()

            # take a picture to inference
            self.image = self.webcam.take_photo()

            # estimate pose vector
            self.pose_estimator.load_image(self.image)
            self.pose_vector = self.pose_estimator.inference()

            # regress the level
            self.level = self.level_regressor.forward(self.pose_vector)

            # send the data the motors
            print(f"Estimated level is {self.level}.\nStart to send data...")
            sendNum(5)
            print("Sending data done.")

            # wait til the YOLO cannot detect any person 
            self.wait_to_sit(mode=1)

if __name__ == '__main__' :
    seat_belt_system = SeatBelt()
    seat_belt_system.system()
    