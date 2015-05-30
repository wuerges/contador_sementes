import cv2
import util

def g_background_cascades(img, dimension):
    (x_delta, y_delta) = dimension
    height, width = img.shape[:2]

    s = util.FileSequence("background")

    for x_skew in range(0, x_delta, 10):
        for y_skew in range(0, x_delta, 10):
            for x in range(x_skew, width - x_delta, x_delta):
                for y in range(y_skew, height - y_delta, y_delta):
                    #print (x, y), (x+x_delta, y+y_delta)
                    w = img[y:y+y_delta, x:x+x_delta]
                    cv2.imwrite(s.next(), w)

    s.gen_background_txt()

def g_extract_cascades(cap):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey() & 0xFF == ord('q'):
            break

