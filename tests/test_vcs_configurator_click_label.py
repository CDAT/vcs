import basevcstest


class TestVSConfigurator(basevcstest.VCSBaseTest):
    def __init__(self, *a, **k):
        k["bg"] = False
        k["geometry"] = {"width": 800, "height": 606}
        super(TestVSConfigurator, self).__init__(*a, **k)

    def testConfiguratorClickTest(self):
        clt = self.clt("clt")

        # Create a template to use
        t = self.x.createtemplate()

        # Hide everything that isn't the dataname
        for attr in dir(t):
            try:
                a = getattr(t, attr)
                if "priority" in dir(a):
                    a.priority = 0
            except AttributeError as TypeError:
                pass

        t.dataname.priority = 1
        t.dataname.x = .1
        t.dataname.y = .9

        orient = self.x.createtextorientation("level", "default")
        orient.angle = 0
        orient.halign = 'left'
        orient.valign = 'half'

        t.dataname.textorientation = orient.name

        # enable the configurator
        self.x.configure()

        # plot in the background
        dp = self.x.boxfill(clt, t)

        # Grab the initialized configurator
        c = self.x.configurator

        # Make sure the displays are current
        c.update()

        w, h = 800, 606

        # Retrieve the actor at the specified point
        actor = c.actor_at_point(.1 * w + 5, .9 * h + 5)

        self.assertIsNotNone(
            actor, "Couldn't find text actor at (%f, %f)" %
            (.1 * w + 5, .9 * h + 5))

        display, key = c.display_and_key_for_actor(actor)
        self.assertEqual(display, dp, "Found wrong display")

        self.assertFalse(
            actor != display.backend[key] and actor not in display.backend[key],
            "Found wrong key for actor")
