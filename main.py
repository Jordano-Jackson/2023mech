import cv2

from communication import sendNum
import numpy as np

from camera import webcam
from model import pose_estimator
#from model import level_regressor
#from model import level_inference

camera = webcam.WebcamCamera(1)
pose = pose_estimator.PoseEstimator()
img = camera.take_photo()

curData = 1 #initial position

"""
while True:
    key = cv2.waitKey(1) & 0xFF  # 1ms 대기 후 키 이벤트 처리
    if key == ord('q'):
        break  # 'q' 키를 누르면 루프 종료
    cv2.imshow("img", img)


cv2.destroyAllWindows()
"""

print("on main.py, type(img) and np.shape(img) : ", type(img), np.shape(img))

pose.load_image(img)
newData = pose.inference()

sendNum(curData - newData)
newData = curData