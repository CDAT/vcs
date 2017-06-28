import cdms2
import cdat_info
import time
import numpy
import basevcstest
import vcs

class VCSTestXtra(basevcstest.VCSBaseTest):
    def testNoXtra(self):
        s=self.clt("clt",time=(45,45,'cob'),longitude=(46.,46.,'cob'),squeeze=1)
        print s.shape
        self.x.portrait()

        N = 20

        elements = vcs.listelements()
        cpy = {}
        for e in elements:
            cpy[e] = vcs.elements[e].copy()

        mn = 10000
        times = []
        for i in range(N):
            start = time.time()
            self.x.plot(s)
            self.x.png("blah",width=1200,height=1600,units="pixels")
            self.x.clear()
            end = time.time()
            elapsed = end -start
            if mn>elapsed: mn = elapsed
            print i,elapsed,elapsed/mn
            times.append(elapsed)
            for e in elements:
                #print "\t",e,len(vcs.elements[e]),len(cpy[e])
                if len(vcs.elements[e])!=len(cpy[e]):
                    print "\tMore elements in:",e,len(vcs.elements[e]),len(cpy[e]),len(vcs.elements[e])-len(cpy[e])
                self.assertEqual(len(vcs.elements[e]),len(cpy[e]))

