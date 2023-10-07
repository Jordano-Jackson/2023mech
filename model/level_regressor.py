## LevelRegressor 

import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

class LevelRegressor(nn.Module) :
    def __init__(self) :
        super(LevelRegressor, self).__init__()
        self.layer = nn.Sequential(
            nn.Linear(8,16),
            nn.ReLU(),
            nn.Linear(16,8),
            nn.ReLU(),
            nn.Linear(8,4),
            nn.ReLU(),
            nn.Linear(4,1)
        )

    def forward(self, x) :
        x = self.layer(x)
        return x
