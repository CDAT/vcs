#!/bin/env python
import basevcstest
import EzTemplate
import gc
import time
import resource
import vcs
import cdms2
import numpy
import vcs
import os


def initVCS(x, levs1, levs2, split):
    gtype = "isofill"
    if gtype == "isofill":
        crt = vcs.createisofill
    else:
        crt = vcs.createboxfill
    x.setcolormap("bl_to_darkred")
    gm1 = crt()
    #iso         = x.createboxfill()
    if gtype == "boxfill": gm1.boxfill_type="custom"
    gm1.levels = levs1
    gm1.ext_1 = True
    gm1.ext_2 = True
    cols = vcs.getcolors(gm1.levels, split=split)
    gm1.fillareacolors = cols

    gm2 = crt()
    if gtype == "boxfill": gm2.boxfill_type="custom"
    levs = levs2
    gm2.levels = levs
    gm2.ext_1 = True
    gm2.ext_2 = True
    cols = vcs.getcolors(gm2.levels, split=1)
    gm2.fillareacolors = cols

    leg = x.createtextorientation()
    leg.halign = "left"
    leg.height = 8

    tmpl = x.createtemplate()
    tmpl.blank()
    tmpl.scalefont(.9)

    tmpl.legend.textorientation = leg
    for a in ["data", "legend", "box1",
              "xlabel1", "xtic1", "ylabel1", "ytic1"]:
        setattr(getattr(tmpl, a), "priority", 1)

    Ez = EzTemplate.Multi(rows=3, columns=1, x=x, template=tmpl)
    Ez.legend.direction = 'vertical'
    Ez.margins.left = .05
    Ez.margins.right = .05
    Ez.margins.top = .05
    Ez.margins.bottom = .05

    title = x.createtext()
    title.height = 14
    title.halign = "center"
    title.x = [.5]
    title.y = [.975]

    t1 = Ez.get(legend="local")
    t2 = Ez.get(legend="local")
    t3 = Ez.get(legend="local")

    del(Ez)

    return gm1, gm2, title, t1, t2, t3, tmpl


class VCSTestMesaLeak(basevcstest.VCSBaseTest):
    def testMesaLeak(self):
        counter = 1
        levs1 = list(numpy.arange(-5, 115, 10))  # SIC
        levs2 = list(numpy.arange(-5, 5.5, .5))
        split = 0

        fout = cdms2.open(os.path.join(vcs.sample_data,"test_mesa_leak.nc"))
        NITER = 10
        mems = []
        for i in range(NITER):
                startTime = time.time()
                printStr = 'processing: %i' % (i)
                s1s = fout("sic")
                s2 = fout("variable_4")
                diff = s2 - s1s
                iso1, iso2, title, t1, t2, t3, tmpl = initVCS(self.x, levs1, levs2, split)
                title.string = '%i' % (i)
                self.x.plot(title)
                self.x.plot(s1s, t1, iso1)
                self.x.plot(diff, t2, iso2)
                self.x.plot(s2, t3, iso1)
                self.x.clear()
                vcs.removeobject(iso1)
                vcs.removeobject(iso2)
                vcs.removeobject(title)
                vcs.removeobject(t1)
                vcs.removeobject(t2)
                vcs.removeobject(t3)
                vcs.removeobject(tmpl)
                endTime = time.time()
                timeStr = 'Time: %06.3f secs;' % (endTime - startTime)
                mem = float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1.e6
                mems.append(mem)
                memStr = 'Max mem: %05.3f GB' % ( mem )
                counterStr = '%05d' % counter
                pyObj = 'PyObj#: %07d;' % (len(gc.get_objects()))
                print counterStr, printStr, timeStr, memStr, pyObj
                counter = counter + 1
                gc.collect()  # Attempt to force a memory flush
        a, b = numpy.polyfit(numpy.arange(NITER),numpy.array(mems),1)
        print a,b
        self.assertTrue(abs(a)<1.e-3)
