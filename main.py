import time
import math
from PIL import Image

import torch

from communication.send_num import sendNum
from camera.webcam import WebcamCamera
from model.pose_estimator import PoseEstimator
from model.level_regressor import LevelRegressor
from seat_detector.seat_detector import SeatDetector

class SeatBelt():
        
    def __init__(self):
        print("initializing...")
        self.level = 1
        self.level_prev = 1
        self.regressor_pth = "saved_params/regressor.pth"
        self.seat_detector = SeatDetector()
        self.pose_estimator = PoseEstimator()
        self.level_regressor = LevelRegressor()
        self.level_regressor.load_parameter(self.regressor_pth)
        self.webcam = WebcamCamera()
        self.test = True

    def wait_to_sit(self):
        if self.seat_detection.is_sitting():
            time.sleep(3) # wait 3 sec to modify the level

    def convert_to_valid_level(self, level):
        level_min = 1
        level_max = 14
        level = math.floor(level)
        level = max(level_min, level)
        level = min(level_max, level)
        return level 

    def system(self): # main working method
        while(True):
            # wait til the YOLO detect a person
            self.seat_detector.is_sitting()

            # take a picture to inference
            self.image = self.webcam.take_photo()

            self.webcam.release()
            self.image = torch.from_numpy(self.image)
            self.image = self.image.unsqueeze(0)
            self.image = self.image.permute(0,3,1,2)

            # estimate pose vector
            self.pose_estimator.load_image(self.image)
            self.pose_vector = self.pose_estimator.inference()
            self.pose_vector = torch.tensor([self.pose_vector[0], self.pose_vector[2]])

            # regress the level
            self.level_prev = self.level
            self.level = self.level_regressor.forward(self.pose_vector)
            self.level = self.convert_to_valid_level(math.floor(self.level))
            #self.level_adjust = self.level - self.level_prev

            # send the data the motors
            print(f"Estimated level is {self.level}.\nStart to send data...")
            #sendNum(self.level)
            print("Sending data done.")

            # wait til the YOLO cannot detect any person 
            self.seat_detector.is_sitting(mode=1)
            #sendNum(-self.level-2) # -2 is subtracted to makeup the weakness of backward-side motor

if __name__ == '__main__' :
    seat_belt_system = SeatBelt()
    seat_belt_system.system()
    
