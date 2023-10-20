import time
import math

from communication.send_num import sendNum

from camera.webcam import WebcamCamera
from model.pose_estimator import PoseEstimator
from model.level_regressor import LevelRegressor
from seat_detector.seat_detector import SeatDetector

class SeatBelt():
        
    def __init__(self):
        print("initializing...")
        self.level = 0
        self.level_prev = 0
        self.regressor_pth = "../saved_params/regressor.pth"
        self.seat_detector = SeatDetector()
        self.pose_estimator = PoseEstimator()
        self.level_regressor = LevelRegressor()
        self.level_regressor.load_parameter(self.regressor_pth)
        self.webcam = WebcamCamera()

    def wait_to_sit(self):
        if self.seat_detection.is_sitting():
            time.sleep(3) # wait 3 sec to modify the level

    def convert_to_valid_level(level):
        level_min = 0
        level_max = 14
        level = math.floor(level)
        level = max(level_min, level)
        level = min(level_max, level)
        return level 

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
            
            self.level_prev = self.level
            self.level = self.level_regressor.forward(self.pose_vector)
            self.level = self.convert_to_valid_level(math.floor(self.level))
            self.level_adjust = self.level - self.level_prev

            # send the data the motors
            print(f"Estimated level is {self.level}.\nStart to send data...")
            sendNum(self.level_adjust)
            print("Sending data done.")

            # wait til the YOLO cannot detect any person 
            self.wait_to_sit(mode=1)

if __name__ == '__main__' :
    seat_belt_system = SeatBelt()
    seat_belt_system.system()
    