import cv2
import time

class WebcamCamera :
    def __init__(self) :
        pass
    
    def take_photo(self) :

        self.cam = cv2.VideoCapture(7)
        new_width = 1920
        new_height = 1080
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)
        
        ret, frame = self.cam.read() 
        time.sleep(4)

        if ret : 
            return frame
        else :
            print("Unable to take picture.")
    
    def release(self) :
        self.cam.release()

