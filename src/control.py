import matching
import model

class Rastreador:
    def __init__(self, hei):
        self.altura = hei
        self.objects = set()
        self.objects_cand = set()
        self.count = 0

    def novo(self, o):
        self.objects_cand.add(model.Ponto(o))

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

        self.limpa()

        print "Media", model.movimento.media()
        print "DP", model.movimento.dp()

    def limpa(self):
        af = model.movimento.media()

        if af:

            t = len(self.objects)
            self.commited = set([o for o in self.objects if (o.y + af) > self.altura and o.age > 3])
            self.objects = set([o for o in self.objects if (o.y + af) <= self.altura])

            print "limpando1: ", self.count, len(self.commited)
            print self.commited
            for o in self.commited:
                mq = o.mediaQuedas()
                if mq:
                    model.movimento.atualiza([mq])
            self.count += len(self.commited)

        self.objects = set([o for o in self.objects if o.fresh < 3])
        print "limpando2: ", self.count, len(self.objects)

