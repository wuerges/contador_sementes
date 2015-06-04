import cv2
import copy

class Filtro:
    def __init__(self, n):
        self.n = n
        self.amostras = []

    def atualiza(self, ms):
        nfs = [self.valor(e) for e in ms]
        self.amostras = (self.amostras + nfs)[0:self.n]

    def media(self):
        if self.amostras:
            return sum(self.amostras) / len(self.amostras)
        return None

class Contorno(Filtro):
    def valor(self, p):
        return cv2.contourArea(p.cnt)

class Movimento(Filtro):
    def valor(self, (a, b)):
        return b.y - a.y

movimento = Movimento(20)
contorno = Contorno(20)

class Ponto:
    serialSeed = 0

    def __init__(self, contour):
        self.cnt = contour
        self.mean = cv2.mean(contour)
        self.x = self.mean[0]
        self.y = self.mean[1]
        (x,y),radius = cv2.minEnclosingCircle(contour)
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
# checa deslocamento X
        if abs(self.x - o.x) > 30:
            return False

# checa se esta abaixo do @o
        if self.y > o.y:
            return False

        af = movimento.media()
        if af and af * 0.7 < (self.y - o.y) < af * 1.3:
            return False

        return True

    def atualiza(self, o):

        self.antecessor = copy.copy(self)

        self.radius = o.radius
        self.cnt = o.cnt
        self.mean = o.mean
        self.x = o.x
        self.y = o.y
        self.age += 1
        self.fresh = 0

