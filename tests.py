import cv2
import config
import sys
config.test_configs()

cap = cv2.VideoCapture(sys.argv[1])
ret, image0 = cap.read()

#testing generate background cascade
import cascade_extractor as bcg

bcg.g_background_cascades(image0, (100, 100))

#testing generating cascades

bcg.g_extract_cascades(cap)
