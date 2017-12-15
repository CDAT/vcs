import basevcstest


class TestVCSBadPngPath(basevcstest.VCSBaseTest):
    def testBadPngPath(self):
        self.x.plot([1, 2, 3, 4, 5], bg=self.bg)
        try:
            x.png(os.path.join("b", "c", "c", "test.png"))
            failed = False
        except BaseException:
            failed = True
        assert(failed)
