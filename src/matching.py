import logging
import cv2
import model

class Matcher:
    def __init__(self, old, new):
        self.old = old
        self.new = new

    def match(self):
        g = Graph()
        for o in self.old:
            g.add_vertex_P1(o)
        for n in self.new:
            g.add_vertex_P2(n)

        for o in self.old:
            for n in self.new:
                if o.candMatch(n):
                    g.add_edge(o, n)

        g.match()
        #g.augment_matching()

        return [(o, g.M[o]) for o in g.M]


class Graph:
    def __init__(self):
        self.E = {}
        self.R = {}

        self.M = {}
        self.RM = {}

    def add_vertex_P1(self, a):
        self.E[a] = set()

    def add_vertex_P2(self, b):
        self.R[b] = set()

    def add_edge(self, a, b):
        self.E[a].add(b)
        self.R[b].add(a)

    def del_edge(self, a, b):
        self.E[a].remove(b)
        self.R[a].remove(a)

    def add_match(self, a, b):
        #if self.M.get(a):
        #    raise "Already had a match for #{a}"
        self.M[a] = b

        #if self.RM.get(b):
        #    raise "Already had a match for #{b}"
        self.RM[b] = a

    def del_match(self, a, b):
        del self.M[a]
        del self.RM[b]

    def match(self):
        for o in self.E:
            for d in reversed(sorted(self.E[o], key=lambda e: e.age)):
                if not d in self.RM:
                    self.add_match(o, d)
                    break

    def print_matches(self):
        print self.M

    def augment_path(self, o, visited=set([])):

        outs = set([(o, d) for d in self.E[o] \
                        if self.M.get(o) != d \
                        if not d in visited] )

        for (a, b) in outs:
            n_o = self.RM.get(b)
            if n_o and not n_o in visited:
                p =  self.augment_path(n_o, visited.union(set([n_o, a, b])))
                if p:
                    return [(a, b), (b, n_o)] + p
            else:
                return [(a, b)]
        return []

    def augment_matching(self):
        for o in self.E:
            if not self.M.get(o):
                p = self.augment_path(o)
                logging.info(p)
                #for (a, b) in p[1::2]:
                #    self.del_match(a, b)
                for (a, b) in p[0::2]:
                    self.add_match(a, b)
                break

    def get_edges(self):
        es = set()
        for o in self.E:
            for d in self.E[o]:
                es.add((o, d))

        for d in self.R:
            for o in self.R[d]:
                es.add((o, d))

        return es
