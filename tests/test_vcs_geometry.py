import vcs
import unittest

class TestVCSGeometry(unittest.TestCase):
    def testGeometry(self):

        # This will check if we can set the geometry
        # at the initialization of canvas
        canvas = vcs.init(geometry=(600, 400))
        canvas.open()

        self.assertEqual(dict(width=600, height=400), canvas.geometry())

        canvas.close()

        canvas2 = vcs.init()

        # This will check if we can safely set the geometry even
        # though the canvas window has not been created yet
        canvas2.geometry(400, 400)
        canvas2.open()
        self.assertEqual(dict(width=400, height=400), canvas2.geometry())

        # This will check if we can dynamically change the geometry
        canvas2.geometry(500, 400)
        canvas2.geometry(500, 500)
        self.assertEqual(dict(width=500, height=500), canvas2.geometry())

        canvas2.close()
