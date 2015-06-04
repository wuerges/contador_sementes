import cv2
import model

def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print "mouse", (x, y)

class Window:
    def __init__(self, nome, frame):
        self.nome = nome
        self.frame = frame
        #cv2.setMouseCallback(self.nome, click)

    def show(self):
        cv2.imshow(self.nome, self.frame)

    def mostraPonto(self, p, cor=(0,255,255), esp=2, n = 0):
        if n == 0:
            cv2.circle(self.frame,(int(p.x), int(p.y)),int(p.radius),(255,0,0),esp)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(self.frame,str(p.age),(int(p.x),int(p.y)), font, 2,(255,255,255),2,cv2.CV_AA)
        else:
            cv2.circle(self.frame,(int(p.x), int(p.y)),int(p.radius),(255,255,0),esp)

        if p.antecessor:
            cv2.line(self.frame, (int(p.x), int(p.y)), (int(p.antecessor.x), int(p.antecessor.y)), (255,255,255), esp)
            self.mostraPonto(p.antecessor, n=n+1)

