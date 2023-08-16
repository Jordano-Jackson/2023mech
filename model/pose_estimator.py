# Import TF and TF Hub libraries.
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np

class PoseEstimator :
    def __init__(self, image_path) :
        # Load the input image.
        self.image = tf.io.read_file(image_path)
        self.image = tf.compat.v1.image.decode_jpeg(self.image)
        self.image = tf.expand_dims(self.image, axis=0)
        # Resize and pad the image to keep the aspect ratio and fit the expected size.
        self.image = tf.cast(tf.image.resize_with_pad(self.image, 256, 256), dtype=tf.int32)

        # Download the model from TF Hub.
        self.model = hub.load("https://tfhub.dev/google/movenet/singlepose/thunder/4")
        self.model = self.model.signatures['serving_default']


    def inference(self) : 
        # returns the (height of spine, width of shoulder) tuple

        # Run model inference.
        outputs = self.model(self.image)
        
        # Output is a [1, 1, 17, 3] tensor.
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
        ax.imshow(self.image)

        # Plot the keypoints on the image.
        keypoints = keypoints[0, 0]  # Extract keypoints from the tensor
        threshold = 0

        for keypoint in keypoints:
            x, y, confidence = keypoint  # Extract x, y coordinates, and confidence
            if confidence > threshold:  # Adjust the threshold as needed
                x *= self.image.shape[0]  # Scale the x coordinate to image frame
                y *= self.image.shape[1]  # Scale the y coordinate to image frame
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
                x_a *= self.image.shape[0]
                y_a *= self.image.shape[1]
                x_b *= self.image.shape[0]
                y_b *= self.image.shape[1]
                plt.plot( [y_a, y_b], [x_a, x_b],'r-', linewidth=1)  # Plot connection as a red line


        # Connect the left shoulder and right shoulder with a line.
        ######### for debugging purpose ##############
        if left_shoulder is not None and right_shoulder is not None:
            plt.plot([left_shoulder[0], right_shoulder[0]], [left_shoulder[1], right_shoulder[1]], 'g-', linewidth=2)

        # Remove the axis labels and ticks.
        ax.axis('off')

        # Show the plotted image.
        plt.show()
