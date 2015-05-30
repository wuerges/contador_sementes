import config
import os


class FileSequence:
    def __init__(self, name):
        self.c = 0
        self.name = name

        self.fns = []
        newpath = "%s/%s" % (config.outfolder, self.name)
        if not os.path.exists(newpath):
            os.makedirs(newpath)

    def next(self):
        fn =  "%s/%s_%010d.png" % (self.name, self.name, self.c)
        self.fns.append(fn)
        r = "%s/%s" % (config.outfolder, fn)
        self.c += 1
        return r

    def gen_background_txt(self):
        with open("%s/%s.txt" % (config.outfolder, self.name), "w") as f:
            f.write("\n".join(self.fns) + "\n")

