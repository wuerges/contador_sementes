import cv2
import copy
import math

class Filtro:
    def __init__(self, n):
        self.n = n
        self.amostras = []

    def atualiza(self, ms):
        nfs = [self.valor(e) for e in ms]
        self.amostras = (nfs + self.amostras)[0:self.n]

    def dp(self):
        print self.amostras
        if len(self.amostras) > 10:
            m = self.media()
            d = sum([(a - m)**2 for a in self.amostras]) / len(self.amostras)
            return math.sqrt(d)
        return None

    def media(self):
        if len(self.amostras) > 10:
            return sum(self.amostras) / len(self.amostras)
        return None

class Area(Filtro):
    def valor(self, p):
        return p.area

class Contorno(Filtro):
    def valor(self, p):
        return p.radius

class Movimento(Filtro):
    #def valor(self, (a, b)):
    #    return b.y - a.y
    def valor(self, v):
        return v

area = Area(30)
movimento = Movimento(30)
contorno = Contorno(30)

class Ponto:
    serialSeed = 0

    def __init__(self, contour):
        self.cnt = contour
        self.mean = cv2.mean(contour)
        self.x = self.mean[0]
        self.y = self.mean[1]
        (x,y),radius = cv2.minEnclosingCircle(contour)
        self.area = cv2.contourArea(contour)
        self.radius = radius
        self.antecessor = None
        self.age = 0
        self.fresh = 0
        self.serial = Ponto.serialSeed + 1

        Ponto.serialSeed += 1

    def __hash__(self):
        return hash(self.serial)

#checa se o @o e' um bom candidato para casar
    def candMatch(self, o):
        af = 80
        dp = 15
# checa deslocamento X
        if abs(self.x - o.x) > 30:
            return False

        return (o.y - dp) > self.y

# checa se esta abaixo do @o
        #if self.y > o.y:
        #    return False

        #af = movimento.media()
        #dp = movimento.dp()
        #if af and (af - dp) < (o.y - self.y) < (af + dp):
        #    return False

        #return True

    def mediaQuedas(self):
        qs = self.quedas()
        if qs:
            return sum(qs) / len(qs)
        return None

    def quedas(self):
        if self.antecessor:
            return [self.y - self.antecessor.y] + self.antecessor.quedas()
        else:
            return []


    def atualiza(self, o):

        self.antecessor = copy.copy(self)

        self.area = o.area
        self.radius = o.radius
        self.cnt = o.cnt
        self.mean = o.mean
        self.x = o.x
        self.y = o.y
        self.age += 1
        self.fresh = 0

