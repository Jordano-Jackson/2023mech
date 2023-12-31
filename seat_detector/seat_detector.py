import time

import cv2
import numpy as np

class SeatDetector() :

    def __init__(self) :
        
        yolo_weight_path = 'thirdparty/yolov3/yolov3.weights'
        yolo_config_path = 'thirdparty/yolov3/yolov3.cfg'

        print("Loading YOLOv3 model...")
        self.yolo = cv2.dnn.readNet(yolo_weight_path, yolo_config_path)
        print("Loading YOLOv3 model done.")

        self.timer = 0

    def is_sitting(self, mode = 0):
        self.timer = time.time()
        
        ## mode can be 'exist' or 'not exist'
        print('Seat detector activated. mode: ',mode)
        
        cap = cv2.VideoCapture(7)

        if not cap.isOpened() :
            print("Error: Could not open webcam.")
            exit()

        while True:
            ret, frame = cap.read()
            # if it is not able to read the frame
            if not ret:
                print("Error: Failed to grab frame.")
                break
            
            #frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            height, width = frame.shape[:2]
            blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416,416), swapRB=True, crop=False)

            # Set input image of the yolo model
            self.yolo.setInput(blob)

            # Executethe yolo model
            output = self.yolo.forward(self.yolo.getUnconnectedOutLayersNames())
            
            # Initialize list where detected objects will stored
            boxes = []
            confidences = []
            class_ids = []

            # Extract detected objects
            for out in output:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.3 and class_id == 0 and mode == 0:  # Class ID 0 corresponds to humans in most YOLO implementationss
                        print("human detected with confidence: ", confidence)
                        cap.release()
                        return True
                    
                    elif mode == 1:
                        if confidence > 0.1 and class_id == 0:
                            self.timer = time.time() 
                        elif confidence < 0.05 and class_id == 0 and time.time()-self.timer >5:
                            print("Human disappeared.", time.time()-self.timer)
                            cap.release()
                            return True

                        """
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        # Calculate coordinates for the top-left corner of the bounding box
                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
                        """
            """
            # Apply non-maximum suppression to remove overlapping bounding boxes
            indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            
            # Draw bounding boxes and labels on the frame
            for i in range(len(boxes)):
                if i in indices:
                    x, y, w, h = boxes[i]
                    label = "Human"
                    color = (0, 255, 0)  # Green color for bounding box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Display the frame with bounding boxes
            cv2.imshow("Human Detection", frame)

            # exit loop when 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        cap.release()
        cv2.destroyAllWindows()"""

if __name__ == '__main__':
    debug = SeatDetector()
    debug.is_sitting()
