import cv2
import numpy as np

vcap = cv2.VideoCapture(0)

while True:
    ret, img = vcap.read()
    if not ret:
        continue

    edges = cv2.Canny(img, 50, 200)
    # cv2.imshow('Frame', img)
    cv2.imshow('Canny', edges)

    key = cv2.waitKey(33)
    if key == ord('q') or key == ord('Q'):
        break

cv2.destroyAllWindows()

print('demo complete')
