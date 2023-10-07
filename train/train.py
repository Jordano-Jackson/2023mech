import numpy as np
import time

import torch
import torch.nn as nn
import torch.optim as optim 
from torch.utils.data import DataLoader
import torchvision

from model.pose_estimator import PoseEstimator
from dataloader.seatbelt_image_dataset import SeatImageDataset
from model.level_regressor import LevelRegressor

def train(model, train_loader, num_epochs, learning_rate, train_dataset) :
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = model.to(device)
    pose = PoseEstimator().to(device)

    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr = learning_rate)
    
    start_time = time.time()

    print("Training start.")
    for epoch in range(num_epochs) :
        total_loss = 0.0
        model.train()

        for img, label in train_loader :

            img = img.to(device)
            pose.load_image(img)
            x = pose.inference()

            # do inference and get output
            print(x)
            output = model(x)

            loss = criterion(output, label.float())
            loss = loss**0.5
            loss /= train_dataset.label_count[label] # correction of imbalance in number of labels
            loss.backward()
            optimizer.step()

            #if(label == 1) :
            print('answer : ',label, ' output: ', output , loss.item())
            total_loss += loss.item()
        
        print(f"Epoch: [{epoch + 1}/{num_epochs}] Loss: {(total_loss / len(train_loader)):.8f} Elapsed time: {time.time()-start_time:.2f}")
        if epoch % 100 == 0 :
            torch.save(model.state_dict(), 'regressor{epoch}.pth')
    print("Training finished.")
    torch.save(model.state_dict(), 'regressor.pth')
    print("Model saved.")

if __name__ == "__main__" :
    dataset = SeatImageDataset()
    
    batch_size = 1
    epochs = 1000
    lr = 2e-4
    dataloader = DataLoader(dataset, batch_size = batch_size, shuffle=False)

    regressor = LevelRegressor()
    regressor.load_state_dict(torch.load('/home/csjihwanh/Desktop/Projects/2023mech/saved_params/regressor_loss10.pth'))

    train(regressor, dataloader, epochs, lr, dataset)

