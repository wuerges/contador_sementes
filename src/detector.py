import cv2
import control
import view
import logging
import numpy
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-q", "--quiet",
        action="store_false", dest="verbose", default=True,
        help="don't print status messages to stdout")

parser.add_option("-c", "--crop", default="0,0,0,0")
parser.add_option("-r", "--rotate", default=False, action="store_true")

(options, args) = parser.parse_args()
if options.verbose:
    logging.basicConfig(level=logging.INFO)


def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

cam = cv2.VideoCapture(args[0])

def next_frame():
    [x1, y1, x2, y2] = map(int, options.crop.split(","))


    global cam
    img = cam.read()[1]


    #print x1, y1, x2, y2



    if img is None:
        return None
    elif x1 == x2 == y1 == y2 == 0:
        return img
    else:
        return img[y1:y2, x1:x2]

def rotate(img):
    if options.rotate:
        img = numpy.rot90( img, 1 )
        img = numpy.rot90( img, 1 )
        img = numpy.rot90( img, 1 )
    return img



# Read three images first:
t_minus = cv2.cvtColor(next_frame(), cv2.COLOR_RGB2GRAY)
t_minus = rotate(t_minus)
color = next_frame()
t = cv2.cvtColor(color, cv2.COLOR_RGB2GRAY)
t = rotate(t)
t_plus = cv2.cvtColor(next_frame(), cv2.COLOR_RGB2GRAY)
t_plus = rotate(t_plus)

height , width , layers =  color.shape
video = cv2.VideoWriter('video.avi',-1,1,(width,height))

def enclosing_circle(cnt, img):
    (x,y),radius = cv2.minEnclosingCircle(cnt)
    center = (int(x),int(y))
    radius = int(radius)
    #img = cv2.circle(img,center,radius,(0,255,0),2)
    cv2.circle(img,center,radius,(0,255,0),2)
    return img


average_area = 90

rastr = control.Rastreador(height)

while True:

    d = diffImg(t_minus, t, t_plus)
    #imshow( winName, d )

    blur = cv2.GaussianBlur(d,(7,7),0)
    ret1,th1 = cv2.threshold(blur,10,255,cv2.THRESH_BINARY)
    #ret2,otsu = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))

    #otsu =  cv2.morphologyEx(otsu,cv2.MORPH_OPEN,kernel)
    #imshow( otsuWin, th1)
    #imshow( otsuWin, th1)

    #_, img_bin = cv2.threshold(d, 0, 255, cv2.THRESH_OTSU)
    #dt = cv2.distanceTransform(th1, 3, 5)
    #imshow( dstWin, dt )

    #n = cv2.normalize(dt, dt, 0, 1.0, cv2.NORM_MINMAX)
    #n =  cv2.morphologyEx(d,cv2.MORPH_OPEN,kernel)
    n =  cv2.morphologyEx(th1,cv2.MORPH_CLOSE,kernel)
    #imshow( dstWin, n )
    n =  cv2.morphologyEx(n,cv2.MORPH_OPEN,kernel)

    contours,hierarchy = cv2.findContours(n, 1, 2)

    for cnt in contours:
        rastr.novo(cnt)

    rastr.rastreia()

    colorWin = view.Window("ColoredImage", color)
    for o in rastr.objects:
        colorWin.mostraPonto(o)

    #for (a, b) in matcher.g.get_edges():
    #    x = (int(a[0]), int(a[1]))
    #    y = (int(b[0]), int(b[1]))
    #    cv2.line(color, x, y ,(255,255,255),2)


    #for (a, b) in ms:
    #    x = (int(a[0]), int(a[1]))
    #    y = (int(b[0]), int(b[1]))
    #    cv2.line(color, x, y ,(255,0,0),5)
    #    print "y dist: ", (a[1] - b[1])
    #    print "x dist: ", (a[0] - b[0])


    #for obj in matcher.g.E:
    #    cv2.circle(color,(int(obj[0]), int(obj[1])),10,(255,255,0),1)
    #for obj in matcher.g.R:
    #    cv2.circle(color,(int(obj[0]), int(obj[1])),10,(0,255,255),1)


    #cv2.line(color, (0,350), (width, 350), (255,255,255), 1)
    colorWin.show()
    #video.write(color)

    #n =  cv2.morphologyEx(n,cv2.MORPH_OPEN,kernel)
    #n =  cv2.morphologyEx(n,cv2.MORPH_OPEN,kernel)

    #try:
    #    imshow( closeWin, n )
    #except:
    #    pass


# Read next image
    #t_minus = t
    t = t_plus
    color = next_frame()
    if color is None:
        break

    t_plus = cv2.cvtColor(color, cv2.COLOR_RGB2GRAY)
    t_plus = rotate(t_plus)

    if options.verbose and contours and (cv2.waitKey(10) & 0xFF == ord('q')):
        break

cv2.destroyAllWindows()
video.release()
print "Results"
print "Total", rastr.count

