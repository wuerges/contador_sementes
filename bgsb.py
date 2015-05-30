import numpy as np
import cv2
import sys

cap = cv2.VideoCapture(sys.argv[1])

fgbg = cv2.BackgroundSubtractorMOG2()

while(1):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    cv2.imshow('frame',fgmask)
    cv2.imshow('image',frame)
    k = cv2.waitKey() & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
