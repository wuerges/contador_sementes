import cv2
import sys

cap = cv2.VideoCapture(sys.argv[1])

ret,background = cap.read()
cv2.imshow('background', background)
cv2.waitKey()


while(ret):
    ret,frame = cap.read()
    #cv2.imshow('frame',frame)
    #if cv2.waitKey() & 0xFF == ord('q'):
    #    break
    cv2.destroyAllWindows()

