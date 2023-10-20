## LevelRegressor 

import torch
import torch.nn as nn

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
    
    def load_parameter(self, file_path):
        state_dict = torch.load(file_path)
        self.load_state_dict(state_dict)