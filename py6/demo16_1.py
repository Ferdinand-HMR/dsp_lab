# blur_video.py
# Demonstrates 2D spatial filtering

import numpy as np
import cv2
from scipy import signal

cap = cv2.VideoCapture(0)

print("Switch to video window. Then press 'p' to save image, 'q' to quit")

kernel = np.ones((9, 9)) / (-1)
kernel[4][4] = 80

kernel2 = np.ones((3,3)) / (-1)

kernel2[0][0] = 0
kernel2[0][2] = 0
kernel2[2][0] = 0
kernel2[2][2] = 0
kernel2[1][1] = 4

kernel3 = np.ones((3,3)) / (-1)
kernel3[1][1] = 8


# kernel1 = np.ones((9,9))

# kernel2 = signal.convolve2d(kernel,kernel1,'')

print kernel2

# kernel = np.ones((9,9), np.float32)/81    # alternately, explicitly specify the data type

while True:

    ok, frame = cap.read()  # Read one frame

    frame = cv2.flip(frame, 1)

    frame = cv2.filter2D(frame, -1, kernel3)

    # frame = cv2.filter2D(frame,-1, kernel1)
    # -1 means the output will have the same data type as input frame

    # Alternately: Gaussian blurring. Arguments: frame, kernal size, spread in X and Y directions.
    # frame = cv2.GaussianBlur(frame, (9,9), sigmaX = 10, sigmaY = 10)

    cv2.imshow('Live video (blurred)', frame)

    key = cv2.waitKey(1)
    # key = key & 0xFF      # (May not be necessary)

    if key == ord('p'):
        cv2.imwrite('blurred.jpg', frame)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
