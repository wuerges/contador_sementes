from collections import defaultdict
import logging
import cv2


average_fall = 70

def filter_edge(a, b):
    global average_fall
    if abs(a[0] - b[0]) > 30:
        return False

    if b[1] < a[1]:
        return False

    d = b[1] - a[1]
    logging.info(average_fall)
    if d < average_fall * 2:

        average_fall = (d + average_fall) / 2

        return True

    return True
    return False

class Matcher:
    def __init__(self):
        self.old = []
        self.new = []

        self.count = 0

        self.objects = set()

        self.commited = []

        self.ages = {}
        self.lost = 0

    def add_contour(self, cnt):
        self.new.append(cnt)


    def next_frame(self):
        self.g = Graph()

        for o in self.old:
            self.g.add_vertex_P1(o)
        for n in self.new:
            self.g.add_vertex_P2(n)


        for o in self.old:
            for n in self.new:
                if filter_edge(o, n):
                    self.g.add_edge(o, n)

        self.g.match()
        self.g.augment_matching()

        self.old = self.new
        self.new = []

        for k in self.g.E:
            self.count += 1
            if not k in self.ages:
                self.ages[k] = 0

            if k in self.g.M:
                self.count -= 1
                n = self.g.M[k]
                self.ages[n] = self.ages[k] + 1
                if k in self.objects:
                    self.objects.remove(k)
                self.objects.add(n)
            else:
                self.old.append(k)



        total_0 = [k for k in self.objects if self.ages[k] > 0]
        total_1 = [k for k in self.objects if self.ages[k] > 1]
        total_2 = [k for k in self.objects if self.ages[k] > 2]
        total_3 = [k for k in self.objects if self.ages[k] > 3]
        total_4 = [k for k in self.objects if self.ages[k] > 4]
        logging.info("Total objects P = " + str(len(self.objects)))
        logging.info("Total objects 0 = " + str(len(total_0)))
        logging.info("Total objects 1 = " + str(len(total_1)))
        logging.info("Total objects 2 = " + str(len(total_2)))
        logging.info("Total objects 3 = " + str(len(total_3)))
        logging.info("Total objects 4 = " + str(len(total_4)))
        logging.info("count = " + str(self.count))


    def get_matches(self):
        return [(k, self.g.M[k]) for k in self.g.M]


class Graph:
    def __init__(self):
        #self.E = defaultdict(set)
        #self.R = defaultdict(set)

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
            for d in self.E[o]:
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

    def edges(self):
        es = set()
        for o in self.E:
            for d in self.E[o]:
                es.add((o, d))

        for d in self.R:
            for o in self.R[d]:
                es.add((o, d))


#g = Graph()
#
#g.add_edge(1, 2)
#g.add_edge(2, 2)
#g.add_edge(3, 2)
#g.add_edge(2, 1)
#g.add_edge(3, 3)
#g.add_edge(3, 4)
#g.add_edge(4, 3)
#
#
#g.match()
#g.augment_matching()
#g.print_matches()
