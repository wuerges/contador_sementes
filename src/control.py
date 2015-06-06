import matching
import cv2
import model

class Rastreador:
    def __init__(self, hei):
        self.altura = hei
        self.objects = set()
        self.objects_cand = set()
        self.count = 0

    def novo(self, o):
        p = model.Ponto(o)
        if p.radius < 15:
            return
        self.objects_cand.add(p)
        ma = 2000
        if ma:
            nels = p.area / 1850
            if nels >= 2:
            #if False:
            #if p.radius > (100 - 30):
                p.radius /= 2
                p.y -= p.radius / 2

                p2 = model.Ponto(o)
                p2.radius /= 2
                p2.y += (p.radius / 2)

                self.objects_cand.add(p2)

                #print "NUMBER OF AREAS", nels
                #cv2.waitKey()

    def rastreia(self):
        matches = matching.Matcher(self.objects, self.objects_cand).match()

        af = model.movimento.media()
        if not af:
            model.movimento.atualiza([b.y - a.y for (a, b) in matches])

        for o in self.objects:
            o.fresh += 1

        for (o, n) in matches:
            o.atualiza(n)
            self.objects_cand.remove(n)

            self.objects.add(o)

        for n in self.objects_cand:
            af = model.movimento.media()
            if not af or n.y < model.movimento.media() * 1.5:
                self.objects.add(n)

        self.objects_cand = set()
        self.limpa()

        #print "Media", model.movimento.media()
        #print "DP", model.movimento.dp()
        #print "Media Cont", model.contorno.media()
        #print "Media Cont DP", model.contorno.dp()
        #print "Media Area", model.area.media()
        #print "Media Area DP", model.area.dp()

    def limpa(self):
        #af = model.movimento.media()
        af = 90

        if af:

            t = len(self.objects)
            self.commited = set([o for o in self.objects if (o.y + af) > self.altura])
            self.objects = set([o for o in self.objects if (o.y + af) <= self.altura])

            #print "limpando1: ", self.count, len(self.commited)
            #print self.commited
            #for o in self.commited:
            #    model.area.atualiza([o])
            #    model.contorno.atualiza([o])
            #    mq = o.mediaQuedas()
            #    if mq:
            #        model.movimento.atualiza([mq])
            self.count += len(self.commited)

        self.objects = set([o for o in self.objects if o.fresh < 3])
        #print "limpando2: ", self.count, len(self.objects)

