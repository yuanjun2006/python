#!/usr/bin/env python3

import camdbg
import time
import cv2

def main():
    vcap = cv2.VideoCapture(0)
    camdbg.init('192.168.10.152', 5000)

    while True:
        ret, frame = vcap.read()
        if not ret:
            continue

        camdbg.im_show('Frame', frame)
        cv2.imshow('Local', frame)
        key = cv2.waitKey(33)
        if key == ord('q') or key == ord('Q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
