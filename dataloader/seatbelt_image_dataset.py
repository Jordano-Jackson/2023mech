import json

import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import numpy as np

class SeatImageDataset(Dataset) :
    def __init__(self) :
        self.image_data = json.load(open("/home/csjihwanh/Desktop/Projects/2023mech/datasets/metadata.json"))

    def __len__(self) :
        return len(self.image_data)
    
    def __getitem__(self, img_idx) :
        img = self.image_data[img_idx]["link"]
        img = transforms.ToTensor()(img)
        label = self.image_data[img_idx]["level"]
        return img, label
    