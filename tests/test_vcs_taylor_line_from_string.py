import vcs
import unittest

class VCSTestTD(unittest.TestCase):
    def testStr(self):
        td = vcs.createtaylordiagram()
        td.skillColor = "red"
        self.assertEqual(td.skillColor,(100.0, 0.0, 0.0, 100.0))
        td.Marker.line_color = ["red",]
        self.assertEqual(td.Marker.line_color,[(100.0, 0.0, 0.0, 100.0)])
        td.Marker.color = ["red",]
        self.assertEqual(td.Marker.color,[(100.0, 0.0, 0.0, 100.0)])
        td.Marker.id_color = ["red",]
        self.assertEqual(td.Marker.id_color,[(100.0, 0.0, 0.0, 100.0)])
        print(dir(td))
        td.addMarker(id_color = "green", color="blue", line_color="pink")
        self.assertEqual(td.Marker.id_color,  [[100.0, 0.0, 0.0, 100.0], (0.0, 100.0, 0.0, 100.0)])
        self.assertEqual(td.Marker.color,  [[100.0, 0.0, 0.0, 100.0], (0.0, 0.0, 100.0, 100.0)])
        self.assertEqual(td.Marker.line_color,  [[100.0, 0.0, 0.0, 100.0], (100.0, 75.29411764705883, 79.6078431372549, 100.0)])

