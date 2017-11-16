import basevcstest


class FakeConfigurator(object):
    def __init__(self):
        self.detached = False

    def detach(self):
        self.detached = True


class TestVCSEndConfigure(basevcstest.VCSBaseTest):
    def testEndConfigure(self):

        fake = FakeConfigurator()

        self.x.configurator = fake
        self.x.close()

        self.assertIsNone(
            self.x.configurator,
            "x.close() did not end configuration")

        self.assertTrue(fake.detached, "x.close() did not detach configurator")

        fake = FakeConfigurator()
        self.x.configurator = fake
        self.x.onClosing(None)

        self.assertIsNone(
            self.x.configurator,
            "x.onClosing did not end configuration")

        self.assertTrue(
            fake.detached,
            "x.onClosing() did not detach configurator")
