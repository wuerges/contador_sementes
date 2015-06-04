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

        model.movimento.atualiza(matches)

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

    def limpa(self):
        af = model.movimento.media()

        if af:
            t = len(self.objects)
            self.commited = set([o for o in self.objects if (o.y + (1 * af)) > self.altura and o.age > 3])
            self.objects = set([o for o in self.objects if (o.y + (1 * af)) <= self.altura])

            print "limpando1: ", self.count, len(self.commited)
            print self.commited
            self.count += len(self.commited)

        self.objects = set([o for o in self.objects if o.fresh < 3])
        print "limpando2: ", self.count, len(self.objects)

