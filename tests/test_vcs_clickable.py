import unittest
import numpy
import vcs
import cdat_info
import cdms2
import os

class ClickTests(unittest.TestCase):
    def setUp(self):
        f=cdms2.open(os.path.join(cdat_info.get_sampledata_path(),"clt.nc"))
        s=f("clt",slice(0,1))
        self.x=vcs.init(bg=True,geometry=(800,600))
        b = vcs.createboxfill()
        t = vcs.createtemplate()
        to = vcs.createtextorientation()
        to.angle = 90
        t.xlabel1.textorientation = to
        b.xticlabels1= {45:"45N"}
        b.datawc_x1 = -180
        b.datawc_x2 = 180.
        self.b = b
        self.t = t
        self.x.plot(s,b,t)
        self.x.png("testClick")
        self.s = s
    def testClickLabels(self):
        click_labels_x = vcs.utils.axisToPngCoords([],self.b,self.t,'x1',[self.b.datawc_x1,self.b.datawc_x2,self.b.datawc_y1,self.b.datawc_y2],png="testClick.png")
        self.assertTrue(numpy.allclose(click_labels_x,[[[ 483.38333333,  483.38333333,  495.36666667,  495.36666667],
              [ 461.37500036,  475.62500036,  475.62500036,  461.37500036]]]))
    def testClickMap(self):
            click_areas = vcs.utils.meshToPngCoords(self.s,self.t,[self.b.datawc_x1,self.b.datawc_x2,self.b.datawc_y1,self.b.datawc_y2],png="testClick.png")
            self.assertEqual(click_areas.shape,(1,46,72))
            self.assertTrue(numpy.allclose(click_areas[0,33:43,25:45:],[[61, 61, 67, 66, 59, 72, 81, 75, 72, 67, 75, 70, 76, 71, 74, 83, 81, 83, 73, 68], [69, 77, 78, 81, 80, 81, 81, 79, 69, 73, 71, 81, 78, 87, 79, 85, 86, 90, 84, 80], [77, 80, 88, 88, 87, 88, 89, 88, 84, 85, 84, 83, 83, 90, 83, 91, 91, 91, 91, 93], [93, 91, 89, 89, 89, 88, 90, 91, 92, 89, 91, 93, 94, 97, 96, 95, 92, 93, 95, 97], [97, 98, 98, 97, 97, 97, 94, 93, 92, 94, 97, 97, 94, 96, 98, 98, 98, 98, 97, 98], [95, 97, 97, 87, 97, 98, 96, 97, 99, 98, 97, 98, 97, 97, 98, 98, 98, 97, 97, 97], [70, 77, 73, 76, 66, 79, 99, 98, 97, 94, 94, 93, 97, 98, 99, 99, 99, 74, 99, 71], [93, 94, 85, 83, 84, 79, 98, 98, 98, 89, 81, 72, 53, 69, 72, 68, 80, 87, 90, 69], [94, 87, 86, 83, 87, 91, 79, 77, 71, 69, 78, 86, 90, 85, 80, 68, 71, 71, 69, 72], [88, 93, 94, 95, 93, 86, 73, 78, 79, 83, 81, 82, 79, 74, 73, 72, 70, 79, 87, 85]]))
