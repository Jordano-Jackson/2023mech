import torch
import cv2

from model.pose_estimator import PoseEstimator

if __name__ == '__main__' :
    #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print("Loading cv2...")
    cap = cv2.VideoCapture(0)
    print("Loading cv2 done.\nLoading Pose...")
    pose = PoseEstimator()#.to(device)

    if not cap.isOpened() :
        print("Error: Could not open webcam.")
        exit()

    while True:
        ret, frame = cap.read()

        # if it is not able to read the frame
        if not ret:
            print("Error: Failed to grab frame.")
            break

        height, width = frame.shape[:2]

        keypoints = pose.debug(frame)

        
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
        
        for i in range(len(keypoints)):
            # 점 그리기
            x, y = int(keypoints[i][0]), int(keypoints[i][1])
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)  # 빨간색으로 점 그리기

        for connection in connections:
            partA, partB = connection
            if keypoints[partA] and keypoints[partB]:
                xA, yA = keypoints[partA][0], keypoints[partA][1]
                xB, yB = keypoints[partB][0], keypoints[partB][1]

                if connection in [(5, 6), (6, 5)]:
                    cv2.line(frame, (xA, yA), (xB, yB), (0, 255, 0), 5)  # 어깨 라인은 두꺼운 초록색
                else:
                    cv2.line(frame, (xA, yA), (xB, yB), (0, 0, 255), 2)  # 나머지 라인은 빨간색


        # Display the frame with bounding boxes
        cv2.imshow("Human Detection", frame)

        # exit loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()