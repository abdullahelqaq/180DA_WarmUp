import cv2
import numpy as np

HSV_MODE = False

cap = cv2.VideoCapture("tracking_phone_medium.mov")

#target_color = np.array([60, 40, 200], dtype=np.uint16)
#target_color = np.array([60, 40, 200], dtype=np.uint16)
target_color = np.array([186, 159, 69], dtype=np.uint16)

error_range = 50

lower_bound = target_color - error_range
upper_bound = target_color + error_range

while True:
    frame_available, frame = cap.read()
    if not frame_available:
        break

    original = frame
    if HSV_MODE:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        target_color = np.array([177, 204, 199], dtype=np.uint16)
        lower_bound = target_color - error_range
        upper_bound = target_color + error_range

    blur = cv2.bilateralFilter(frame, 9, 75, 75)
    mask = cv2.inRange(blur, lower_bound, upper_bound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    post_blur = cv2.GaussianBlur(res, (5, 5), 0)
    edges = cv2.Canny(post_blur, 100, 200)

    contours, hier = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        biggest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest_contour)

        cv2.rectangle(original, (x, y), (x+w, y+h), (255, 0, 0), 2)

    cv2.imshow('frame', original)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()