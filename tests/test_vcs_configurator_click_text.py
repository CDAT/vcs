import basevcstest


class TestVSConfigurator(basevcstest.VCSBaseTest):
    def testConfiguratorClickTest(self):

        self.x.width = 800
        self.x.height = 606
        t = self.x.createtext()
        t.string = "test string"
        t.x = .1
        t.y = .1

        # enable the configurator
        self.x.configure()

        # plot in the background
        dp = self.x.plot(t, bg=True)

        # Grab the initialized configurator
        c = self.x.configurator

        # Make sure the displays are current
        c.update()

        w, h = self.x.width, self.x.height

        # Retrieve the actor at the specified point
        actor = c.actor_at_point(.1 * w + 10, .1 * h + 5)

        self.assertIsNotNone(actor, "Couldn't find text actor")

        display, key = c.display_and_key_for_actor(actor)

        self.assertEqual(display, dp, "Found wrong display")

        self.assertFalse(
            actor != display.backend[key] and actor not in display.backend[key],
            "Found wrong key for actor")
