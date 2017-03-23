import basevcstest
import numpy
import vcs

class TestVCSNoXtraElts(basevcstest.VCSBaseTest):
    def testNoXtraElements(self):
        data = numpy.sin(numpy.arange(100))
        data.shape = (10, 10)
        orig =  {}
        new = {}
        for k in vcs.elements.keys():
            new[k] = []
            orig[k]=vcs.elements[k].keys()

        self.x.plot(data,"default","boxfill",bg=self.bg)
        self.x.plot(data,"default","isofill",bg=self.bg)
        self.x.plot(data,"default","isoline",bg=self.bg)
        self.x.plot(data,data,"default","vector",bg=self.bg)
        self.x.plot(data,"default","1d",bg=self.bg)
        self.x.clear()

        diff = False
        for e in vcs.elements.keys():
            for k in vcs.elements[e].keys():
                if k not in orig[e]:
                    new[e].append(k)
                    diff = True

        if diff:
            for k in new.keys():
              if new[k]!=[]:
                print k,new[k]
            raise Exception("New elements added when it shouldn't")
