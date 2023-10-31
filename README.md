# 인공지능 기반 자동 안전벨트 조절 장치 개발(Development of an automatic seat belt adjustment device based on AI)
제13회 전국학생기계설계경진대회 대학부 대상(과학기술정보통신부 장관상) 수상작 


<a href = "http://www.mtnews.net/m/view.php?idx=17187">고려대학교 ‘어깨꽉잡아’ 팀(이재윤, 김영서, 홍지환, 김수인, 김재원, 지우성), ‘인공지능 기반 자동 안전벨트 조절 장치 개발’</a>

## Overview
![image](https://github.com/Jordano-Jackson/2023mech/assets/19871043/d461c4ac-83dc-43a8-bf87-17728cdc69a9)

# Introduction 
Proper seat belt usage is crucial for vehicle safety. However, seat belts are typically designed for the average adult male, causing issues for individuals with different body types. To address this, we propose an AI-based system that automatically adjusts seat belt height. Using in-vehicle cameras, the system collects passenger body data and calculates the ideal seat belt position. A stepper motor then adjusts the seat belt accordingly, ensuring a secure fit. Our device aims to reduce accident fatalities and prevent secondary injuries caused by improper seat belt positioning.

(Excerpted from the original paper)

# Modules 
## Seat Detector
Seat detector is made utilizing YOLOv3.

![yolo_demo_480](https://github.com/Jordano-Jackson/2023mech/assets/19871043/d1256607-8920-4567-bebe-f4a66a0d2f01)


## Pose Estimator & Level Regressor
<img width="437" alt="image" src="https://github.com/Jordano-Jackson/2023mech/assets/19871043/c5b5e414-c097-4833-9b2f-9f84b6483346">


# Pose Estimator
Pose Estimator is based on MoveNet thunder version 

<img src="https://github.com/Jordano-Jackson/2023mech/assets/19871043/642658de-aff5-41da-abb6-5a5b25ed4df8" width="380">

  

Final results is resized image like below:

<img width="188" alt="image" src="https://github.com/Jordano-Jackson/2023mech/assets/19871043/777f5382-5758-43d4-9eec-69cb5ca32292">


# Level Regressor
Level regressor is a 2-layer dense layer model. It was 3-layer dense layer at the first time, but during the training time, I realized that 2-layer model learns better.

The regressor receives the heights of the left shoulder and right shoulder and then returns the proper height level of the safety belt. The domain of the safety belt level is $l \in \mathbb Z, 1 \le l \le 14$.


## Communication
SendNum sends how much to rotate the stepper motor to esp32. It was implemented through the pybluez library. It transmits by distinguishing direction 0 or 1 and degree that absolute of difference between current and estimated level.

Communication between Arduino uno and Esp32 is simplex via softserial. 
Firmware upload is required for each.

## Acquirement

YOLOv3 weight file can be downloaded using `wget https://pjreddie.com/media/files/yolov3.weights`

## References
[1] Redmon, J., & Farhadi, A. (2018). Yolov3: An incremental improvement. arXiv preprint arXiv:1804.02767.

[2] Kathuria, A. (2018, July 4). What’s new in YOLO v3? - Towards Data Science. Medium. https://towardsdatascience.com/yolo-v3-object-detection-53fb7d3bfe6b

[3] Next-Generation Pose Detection with MoveNet and TensorFlow.js. (n.d.-b). https://blog.tensorflow.org/2021/05/next-generation-pose-detection-with-movenet-and-tensorflowjs.html

## Developers
<ul>
  <li><a href="https://github.com/xwsa568">Youngseo Kim</a></li>
  <li><a href="https://github.com/Jordano-Jackson">Jihwan Hong</a></li>
</ul>
