import cv2
import sys

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

cam = cv2.VideoCapture(sys.argv[1])

winName = "Movement Indicator"
colorWin = "ColoredImage"
dstWin = "DistanceWin"
closeWin = "CloseWin"
otsuWin = "Otsu"

for wn in [winName, colorWin, closeWin, dstWin, otsuWin]:
    cv2.namedWindow(wn, cv2.CV_WINDOW_AUTOSIZE)
    cv2.resizeWindow(wn, 360, 240)

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

while True:
    d = diffImg(t_minus, t, t_plus)
    cv2.imshow( winName, d )
    cv2.imshow( colorWin, t )

    blur = cv2.GaussianBlur(d,(7,7),0)
    ret1,th1 = cv2.threshold(blur,10,255,cv2.THRESH_BINARY)
    #ret2,otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))

    #otsu =  cv2.morphologyEx(otsu,cv2.MORPH_OPEN,kernel)
    cv2.imshow( otsuWin, th1)
    #cv2.imshow( otsuWin, th1)


    #_, img_bin = cv2.threshold(d, 0, 255, cv2.THRESH_OTSU)
    #dt = cv2.distanceTransform(th1, 3, 5)
    #cv2.imshow( dstWin, dt )

    #n = cv2.normalize(dt, dt, 0, 1.0, cv2.NORM_MINMAX)
    #n =  cv2.morphologyEx(d,cv2.MORPH_OPEN,kernel)
    n =  cv2.morphologyEx(th1,cv2.MORPH_CLOSE,kernel)
    cv2.imshow( dstWin, n )
    n =  cv2.morphologyEx(n,cv2.MORPH_OPEN,kernel)
    #n =  cv2.morphologyEx(n,cv2.MORPH_OPEN,kernel)
    #n =  cv2.morphologyEx(n,cv2.MORPH_OPEN,kernel)

    cv2.imshow( closeWin, n )


# Read next image
    #t_minus = t
    t = t_plus
    t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

    if cv2.waitKey() & 0xFF == ord('q'):
        cv2.destroyWindow(winName)
        break

print "Goodbye"

