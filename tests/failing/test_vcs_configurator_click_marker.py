import basevcstest


class TestVSConfigurator(basevcstest.VCSBaseTest):
    def testClickMarker(self):
        self.x.width = 800
        self.x.height = 606
        m = self.x.createmarker()
        m.x = .1,
        m.y = .1,

        # enable the configurator
        self.x.configure()

        # plot in the background
        dp = self.x.plot(m, bg=1)

        # Grab the initialized configurator
        c = self.x.configurator

        # Make sure the displays are current
        c.update()

        w, h = self.x.width, self.x.height

        # Retrieve the actor at the specified point
        actor = c.actor_at_point(.1 * w, .1 * h)

        self.assertIsNotNone(actor, "Couldn't find marker actor")

        display, key = c.display_and_key_for_actor(actor)

        self.assertEqual(display, dp, "Found wrong display")

        try:
            if actor not in display.backend[key][0]:
                print("Found wrong key for actor")
                sys.exit(1)
        except AttributeError:
            print("Found wrong key for actor")
            sys.exit(1)
