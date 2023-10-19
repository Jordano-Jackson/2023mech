# Import TF and TF Hub libraries.
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np

import torch
import torch.nn as nn

model_path = '/home/csjihwanh/Desktop/Projects/2023mech/model/movenet_singlepose_thunder_4/'

class PoseEstimator(nn.Module) :
    def __init__(self) :
        super(PoseEstimator,self).__init__()
        # Download the model from TF Hub.
        print("Loading the model...")
        self.model = hub.load("https://tfhub.dev/google/movenet/singlepose/thunder/4")
        self.model = self.model.signatures['serving_default']
        print("Loading model is done.")

    def load_image(self, image) :
        # Load the input image.
        self.image = image # image shape is [1, 3, 1080, 1920]
        self.image = self.image.permute(0,3,2,1) # image shape is [1 ,1920, 1080, 3]
        self.image = tf.image.flip_up_down(self.image)
        #self.input = tf.convert_to_tensor(self.image, dtype=tf.int32)
        self.input = self.image
        self.input = tf.image.resize(self.input, [256,256])
        self.input*=256
        self.input = tf.cast(self.input, dtype= tf.int32)
        self.input = tf.reshape(self.input, [1,256,256,3])
        """
        plt.imshow(self.image[0])
        plt.show()
        plt.imshow(self.input[0])
        plt.show()
        """

    def inference(self) : 
        # returns the (height of spine, width of shoulder) tuple

        # Run model inference.
        outputs = self.model(self.input)


        keypoints = outputs['output_0']
        print(keypoints)
        # Define body part connections.
        connections = [
            (5, 6),  # left shoulder to right shoulder
            (5, 7),  # left shoulder to left elbow
            (7, 9),  # left elbow to left wrist
            (6, 8),  # right shoulder to right elbow
            (8, 10),  # right elbow to right wrist
            (5, 11), # left shoulder to left hip
            (6, 12), # right shoulder to right hip 
            (11, 12),  # left hip to right hip
            (11, 13),  # left hip to left knee
            (13, 15),  # left knee to left ankle
            (12, 14),  # right hip to right knee
            (14, 16)  # right knee to right ankle
        ]

        # Create a figure and axis to plot the image. 
        ####### for debugging purpose ############
        fig, ax = plt.subplots()
        ax.imshow(self.input[0])

        # Plot the keypoints on the image.
        keypoints = keypoints[0, 0]  # Extract keypoints from the tensor
        threshold = 0

        for keypoint in keypoints:
            x, y, confidence = keypoint  # Extract x, y coordinates, and confidence
            if confidence > threshold:  # Adjust the threshold as needed
                x *= self.input[0].shape[0]  # Scale the x coordinate to image frame
                y *= self.input[0].shape[1]  # Scale the y coordinate to image frame
                plt.plot(y, x, 'r.', markersize=5)
            if np.array_equal(keypoint, keypoints[5]):  # Check for left shoulder
                left_shoulder = (y, x)
            elif np.array_equal(keypoint, keypoints[6]):  # Check for right shoulder
                right_shoulder = (y, x)

        for connection in connections:
            part_a, part_b = connection
            x_a, y_a, _ = keypoints[part_a]
            x_b, y_b, _ = keypoints[part_b]
            if keypoints[part_a, 2] > threshold and keypoints[part_b, 2] > threshold:  # Adjust the threshold as needed
                x_a *= self.input[0].shape[0]
                y_a *= self.input[0].shape[1]
                x_b *= self.input[0].shape[0]
                y_b *= self.input[0].shape[1]
                plt.plot( [y_a, y_b], [x_a, x_b],'r-', linewidth=1)  # Plot connection as a red line


        # Connect the left shoulder and right shoulder with a line.
        
        ######### for debugging purpose ##############
        if left_shoulder is not None and right_shoulder is not None:
            plt.plot([left_shoulder[0], right_shoulder[0]], [left_shoulder[1], right_shoulder[1]], 'g-', linewidth=2)

        # Remove the axis labels and ticks.
        ax.axis('off')

        # Show the plotted image.
        plt.show()
        
            # Output is a [1, 1, 17, 3] tensor.
        keypoints = tf.squeeze(outputs['output_0'])
        keypoints = keypoints.numpy()
        keypoints = torch.tensor(keypoints) # convert into torch tensor
        keypoints = keypoints[:, :-1] # confidence score removal

        return torch.cat([keypoints[5], keypoints[6], keypoints[11], keypoints[12]])
    
    def debug(self) : 
        # returns the (height of spine, width of shoulder) tuple
        outputs = self.model(self.input)

        keypoints = outputs['output_0']

        return keypoints 
        # Define body part connections.
        connections = [
            (5, 6),  # left shoulder to right shoulder
            (5, 7),  # left shoulder to left elbow
            (7, 9),  # left elbow to left wrist
            (6, 8),  # right shoulder to right elbow
            (8, 10),  # right elbow to right wrist
            (5, 11), # left shoulder to left hip
            (6, 12), # right shoulder to right hip 
            (11, 12),  # left hip to right hip
            (11, 13),  # left hip to left knee
            (13, 15),  # left knee to left ankle
            (12, 14),  # right hip to right knee
            (14, 16)  # right knee to right ankle
        ]

        # Create a figure and axis to plot the image. 
        ####### for debugging purpose ############
        fig, ax = plt.subplots()
        ax.imshow(self.input[0])

        # Plot the keypoints on the image.
        keypoints = keypoints[0, 0]  # Extract keypoints from the tensor
        threshold = 0

        for keypoint in keypoints:
            x, y, confidence = keypoint  # Extract x, y coordinates, and confidence
            if confidence > threshold:  # Adjust the threshold as needed
                x *= self.input[0].shape[0]  # Scale the x coordinate to image frame
                y *= self.input[0].shape[1]  # Scale the y coordinate to image frame
                plt.plot(y, x, 'r.', markersize=5)
            if np.array_equal(keypoint, keypoints[5]):  # Check for left shoulder
                left_shoulder = (y, x)
            elif np.array_equal(keypoint, keypoints[6]):  # Check for right shoulder
                right_shoulder = (y, x)

        for connection in connections:
            part_a, part_b = connection
            x_a, y_a, _ = keypoints[part_a]
            x_b, y_b, _ = keypoints[part_b]
            if keypoints[part_a, 2] > threshold and keypoints[part_b, 2] > threshold:  # Adjust the threshold as needed
                x_a *= self.input[0].shape[0]
                y_a *= self.input[0].shape[1]
                x_b *= self.input[0].shape[0]
                y_b *= self.input[0].shape[1]
                plt.plot( [y_a, y_b], [x_a, x_b],'r-', linewidth=1)  # Plot connection as a red line


        # Connect the left shoulder and right shoulder with a line.
        
        ######### for debugging purpose ##############
        if left_shoulder is not None and right_shoulder is not None:
            plt.plot([left_shoulder[0], right_shoulder[0]], [left_shoulder[1], right_shoulder[1]], 'g-', linewidth=2)

        # Remove the axis labels and ticks.
        ax.axis('off')

        # Show the plotted image.
        plt.show()
        
            # Output is a [1, 1, 17, 3] tensor.
        keypoints = tf.squeeze(outputs['output_0'])
        keypoints = keypoints.numpy()
        keypoints = torch.tensor(keypoints) # convert into torch tensor
        keypoints = keypoints[:, :-1] # confidence score removal

        return torch.cat([keypoints[5], keypoints[6], keypoints[11], keypoints[12]])
    
