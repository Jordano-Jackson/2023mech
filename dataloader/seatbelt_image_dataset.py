import json
import numpy as np

import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image

class SeatImageDataset(Dataset) :
    def __init__(self) :
        self.image_data = json.load(open("/home/csjihwanh/Desktop/Projects/2023mech/datasets/metadata.json"))
        self.label_count = [0]*15

    def __len__(self) :
        return len(self.image_data)
    
    def label_count(self, label_idx) :
        return self.label_count[label_idx]

    def __getitem__(self, img_idx) :
        img_src = self.image_data[img_idx]["link"]
        img = Image.open(img_src)
        img = transforms.ToTensor()(img)
        label = self.image_data[img_idx]["level"]
        self.label_count[label]+=1
        return img, label
    