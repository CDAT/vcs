import basevcstest

class TestVCSDrawMarkerLeg(basevcstest.VCSBaseTest):
    def __init__(self,*a,**k):
        k["bg"]=False
        super(TestVCSDrawMarkerLeg,self).__init__(*a,**k)

    def testDrawMarkerLegend(self):
        t = self.x.createtemplate()
        t.drawLinesAndMarkersLegend(self.x,
              ["red","blue","green"], ["solid","dash","dot"],[1,4,8],
              ["blue","green","red"], ["cross","square","dot"],[3,4,5],
              ["sample A","type B","thing C"],bg=self.bg,render=True)

        fnm = "test_drawLinesAndMarkersLegend.png"
        self.checkImage(fnm)
