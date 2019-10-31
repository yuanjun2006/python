import cv2
import numpy as np

vcap = cv2.VideoCapture(0)

while True:
    ret, img = vcap.read()
    if not ret:
        continue

    cv2.imshow('Frame', img)
    key = cv2.waitKey(33)
    if key == 113 or key == 81:
        break

cv2.destroyAllWindows()

print('demo complete')
