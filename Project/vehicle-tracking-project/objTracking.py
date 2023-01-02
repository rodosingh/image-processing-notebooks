'''
    File name         : objTracking.py
    Description       : Main file for object tracking
    Author            : Rahmad Sadli
    Date created      : 20/02/2020
    Python Version    : 3.7
'''

import cv2
from Detector import detect
from KalmanFilter import KalmanFilter

def main():

    # Create opencv video capture object
    VideoCap = cv2.VideoCapture('video/randomball.avi')#randomball.avi

    #Variable used to control the speed of reading the video
    ControlSpeedVar = 100  #Lowest: 1 - Highest:100

    HiSpeed = 100

    #Create KalmanFilter object KF
    #KalmanFilter(dt, u_x, u_y, std_acc, x_std_meas, y_std_meas)

    KF = KalmanFilter(0.1, 1, 1, 1, 0.1, 0.1)

    debugMode=1

    while(True):
        # Read frame
        ret, frame = VideoCap.read()
        if not ret:
            break

        # Detect object
        centers = detect(frame,debugMode)
        print(len(centers))
        # If centroids are detected then track them
        if (len(centers) > 0):

            # Draw the detected circle
            #cv2.circle(frame, (int(centers[0][0]), int(centers[0][1])), 15, (0, 191, 255), 2)
            x = int(centers[0][0])
            y = int(centers[0][1])
            w = int(centers[0][2])
            h = int(centers[0][3])
            cv2.rectangle(frame, (x, y), (x+w,y+h), (0, 255, 0), 2)
            
            # Predict
            (x, y) = KF.predict()
            # Draw a rectangle as the predicted object position
            cv2.rectangle(frame, (int(x) - 15, int(y) - 15), (int(x) + 15, int(y) + 15), (255, 0, 0), 2)

            # Update
            (x1, y1) = KF.update(centers[0])

            # Draw a rectangle as the estimated object position
            cv2.rectangle(frame, (int(x1) - 15, int(y1) - 15), (int(x1) + 15, int(y1) + 15), (0, 0, 255), 2)

            cv2.putText(frame, "Estimated Position", (int(x1) + 15, int(y1) + 10), 0, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, "Predicted Position", (int(x) + 15, int(y)), 0, 0.5, (255, 0, 0), 2)
            cv2.putText(frame, "Measured Position", (int(centers[0][0]) + 15, int(centers[0][1]) - 15), 0, 0.5, (0,191,255), 2)

        cv2.imshow('image', frame)

        if cv2.waitKey(2) & 0xFF == ord('q'):
            break
    VideoCap.release()
    cv2.destroyAllWindows()
    # cv2.waitKey(HiSpeed-ControlSpeedVar+1)


if __name__ == "__main__":
    # execute main
    main()
