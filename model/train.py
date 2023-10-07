print('hello')
from pose_estimator import PoseEstimator
#import level_regressor

import tensorflow as tf
import torchvision 
import torch
from PIL import Image
import json
import numpy as np 

metadata_path = "/home/csjihwanh/Desktop/Projects/2023mech/datasets/metadata.json"
pose = PoseEstimator() 

with open(metadata_path, 'r', encoding='utf-8') as json_file : 
    dataset = json.load(json_file)
    print("loaded")

print(dataset)
for data in dataset :
    #image = Image.open(data['link'])
    #image.show()
    img = torchvision.io.read_image(data['link'])
    print(np.shape(img))
    pose.load_image(img)
    pose.inference()