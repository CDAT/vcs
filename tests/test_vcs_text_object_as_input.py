import basevcstest


class TestVCSText(basevcstest.VCSBaseTest):
    def testTextObjectAsInput(self):
        tt = self.x.createtexttable()
        to = self.x.createtextorientation()

        t = self.x.createtemplate()

        t.title.texttable = tt
        t.title.textorientation = to

        assert(t.title.texttable == tt.name)
        assert(t.title.textorientation == to.name)
