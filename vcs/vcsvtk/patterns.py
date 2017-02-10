import vtk
import math


class Pattern(object):
    def __init__(self, patternPolyData, scale, style):
        self.patternPolyData = patternPolyData
        self.scale = scale
        self.style = style
        self.glyph = None
        self.rotation = 0.0

    def render(self):
        """
        Glyphs the input polydata points with the requested shape and
        replaces the input polydata with glyphed output polydata with
        colored cells
        """

        self.glyph = vtk.vtkPolyData()
        pts = vtk.vtkPoints()
        pts.Allocate(6, 6)
        self.glyph.SetPoints(pts)
        verts = vtk.vtkCellArray()
        verts.Allocate(verts.EstimateSize(1, 1), 1)
        self.glyph.SetVerts(verts)
        lines = vtk.vtkCellArray()
        lines.Allocate(lines.EstimateSize(4, 2), 2)
        self.glyph.SetLines(lines)
        polys = vtk.vtkCellArray()
        polys.Allocate(polys.EstimateSize(1, 4), 4)
        self.glyph.SetPolys(polys)

        self.paint()
        self.transform_glyph()

        self.glyph2D = vtk.vtkGlyph2D()
        self.glyph2D.OrientOff()
        self.glyph2D.ScalingOff()
        self.glyph2D.SetScaleModeToDataScalingOff()
        self.glyph2D.SetInputData(self.patternPolyData)
        self.glyph2D.SetSourceData(self.glyph)
        self.glyph2D.Update()
        self.patternPolyData.DeepCopy(self.glyph2D.GetOutput())

    def paint(self):
        raise NotImplementedError(
            "paint() not implemented for %s" % str(
                type(self)))

    def transform_glyph(self):
        pts = self.glyph.GetPoints()
        npts = pts.GetNumberOfPoints()
        if self.rotation == 0.0:
            pass
            for i in range(npts):
                x = pts.GetPoint(i)
                y = [c * d for c, d in zip(x, self.scale)]
                y.append(0.0)
                pts.SetPoint(i, y)
        else:
            a = math.radians(self.rotation)
            for i in range(npts):
                x = pts.GetPoint(i)
                xt = x[0] * math.cos(a) - x[1] * math.sin(a)
                yt = x[0] * math.sin(a) + x[1] * math.cos(a)
                y = [xt, yt, 0]
                y = [c * d for c, d in zip(y, self.scale)]
                y.append(0.0)
                pts.SetPoint(i, y)


class BottomLeftTri(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.5, -0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.5, 0.25, 0.0))
        ptIds.append(pts.InsertNextPoint(0.25, -0.5, 0.0))
        self.glyph.GetPolys().InsertNextCell(3, ptIds)


class TopRightTri(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.25, 0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, 0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, -0.25, 0.0))
        self.glyph.GetPolys().InsertNextCell(3, ptIds)


class Dot(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        res = 10
        ptIds = vtk.vtkIdList()
        ptIds.SetNumberOfIds(res)
        x = [0, 0, 0]
        theta = 2.0 * math.pi / res
        for i in range(res):
            x[0] = 0.35 * math.cos(i * theta)
            x[1] = 0.35 * math.sin(i * theta)
            ptIds.SetId(i, pts.InsertNextPoint(x))
        self.glyph.GetPolys().InsertNextCell(ptIds)


class CheckerBoard(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.5, 0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.0, 0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.0, 0.0, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.5, 0.0, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)

        ptIds1 = []
        ptIds1.append(pts.InsertNextPoint(0.0, 0.0, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.5, 0.0, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.5, -0.5, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.0, -0.5, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds1)


class HorizStripe(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.5, -0.25, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, -0.25, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, 0.25, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.5, 0.25, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)


class VertStripe(HorizStripe):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.25, -0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.25, -0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.25, 0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.25, 0.5, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)


class HorizDash(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.35, -0.10, 0.0))
        ptIds.append(pts.InsertNextPoint(0.35, -0.10, 0.0))
        ptIds.append(pts.InsertNextPoint(0.35, 0.10, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.35, 0.10, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)


class VertDash(HorizDash):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.10, -0.35, 0.0))
        ptIds.append(pts.InsertNextPoint(0.10, -0.35, 0.0))
        ptIds.append(pts.InsertNextPoint(0.10, 0.35, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.10, 0.35, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)


class DashStripe(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.35, -0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.15, -0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.15, 0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.35, 0.5, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)
        ptIds1 = []
        ptIds1.append(pts.InsertNextPoint(0.35, -0.5, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.35, 0.5, 0.0))
        self.glyph.GetLines().InsertNextCell(2, ptIds1)


class ThinDiagDownRight(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.5, 0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, -0.5, 0.0))
        self.glyph.GetLines().InsertNextCell(2, ptIds)


class ThickDiagDownRight(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.5, 0.25, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.5, 0.75, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, -0.25, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, -0.75, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)


class ThinDiagUpRight(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(0.5, 0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.5, -0.5, 0.0))
        self.glyph.GetLines().InsertNextCell(2, ptIds)


class ThickDiagUpRight(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.5, -0.25, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.5, -0.75, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, 0.25, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, 0.75, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)


class XCross(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.5, 0.35, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.5, 0.65, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, -0.35, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, -0.65, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)
        ptIds1 = []
        ptIds1.append(pts.InsertNextPoint(-0.5, -0.35, 0.0))
        ptIds1.append(pts.InsertNextPoint(-0.5, -0.65, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.5, 0.35, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.5, 0.65, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds1)


class DoubleCross(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = vtk.vtkIdList()
        ptIds.SetNumberOfIds(13)
        ptIds.SetId(0, pts.InsertNextPoint(-0.5, -0.1, 0.0))
        ptIds.SetId(1, pts.InsertNextPoint(-0.1, -0.1, 0.0))
        ptIds.SetId(2, pts.InsertNextPoint(-0.1, -0.5, 0.0))
        ptIds.SetId(3, pts.InsertNextPoint(0.1, -0.5, 0.0))
        ptIds.SetId(4, pts.InsertNextPoint(0.1, -0.1, 0.0))
        ptIds.SetId(5, pts.InsertNextPoint(0.5, -0.1, 0.0))
        ptIds.SetId(6, pts.InsertNextPoint(0.5, 0.1, 0.0))
        ptIds.SetId(7, pts.InsertNextPoint(0.1, 0.1, 0.0))
        ptIds.SetId(8, pts.InsertNextPoint(0.1, 0.5, 0.0))
        ptIds.SetId(9, pts.InsertNextPoint(-0.1, 0.5, 0.0))
        ptIds.SetId(10, pts.InsertNextPoint(-0.1, 0.1, 0.0))
        ptIds.SetId(11, pts.InsertNextPoint(-0.5, 0.1, 0.0))
        ptIds.SetId(12, ptIds.GetId(0))
        self.glyph.GetLines().InsertNextCell(ptIds)


class Diamond(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(0.0, -0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, 0.0, 0.0))
        ptIds.append(pts.InsertNextPoint(0.0, 0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.5, 0.0, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)


class DoubleDiamond(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.5, 0.0, 0.0))
        ptIds.append(pts.InsertNextPoint(0.0, 0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.5, 0.0, 0.0))
        ptIds.append(pts.InsertNextPoint(0.0, -0.5, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)
        t1PtId = []
        t1PtId.append(pts.InsertNextPoint(-0.5, -0.5, 0.0))
        t1PtId.append(pts.InsertNextPoint(-0.5, -0.25, 0.0))
        t1PtId.append(pts.InsertNextPoint(-0.25, -0.5, 0.0))
        self.glyph.GetPolys().InsertNextCell(3, t1PtId)
        t2PtId = []
        t2PtId.append(pts.InsertNextPoint(0.5, -0.5, 0.0))
        t2PtId.append(pts.InsertNextPoint(0.5, -0.25, 0.0))
        t2PtId.append(pts.InsertNextPoint(0.25, -0.5, 0.0))
        self.glyph.GetPolys().InsertNextCell(3, t2PtId)
        t3PtId = []
        t3PtId.append(pts.InsertNextPoint(0.5, 0.5, 0.0))
        t3PtId.append(pts.InsertNextPoint(0.5, 0.25, 0.0))
        t3PtId.append(pts.InsertNextPoint(0.25, 0.5, 0.0))
        self.glyph.GetPolys().InsertNextCell(3, t3PtId)
        t4PtId = []
        t4PtId.append(pts.InsertNextPoint(-0.5, 0.5, 0.0))
        t4PtId.append(pts.InsertNextPoint(-0.5, 0.25, 0.0))
        t4PtId.append(pts.InsertNextPoint(-0.25, 0.5, 0.0))
        self.glyph.GetPolys().InsertNextCell(3, t4PtId)


class Bubble(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.40, -0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.0, -0.5, 0.0))
        ptIds.append(pts.InsertNextPoint(0.0, -0.10, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.40, -0.10, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)
        ptIds1 = []
        ptIds1.append(pts.InsertNextPoint(-0.40, 0.0, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.40, 0.0, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.40, 0.40, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.0, 0.40, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds1)


class Snake(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        ptIds = []
        ptIds.append(pts.InsertNextPoint(-0.45, -0.25, 0.0))
        ptIds.append(pts.InsertNextPoint(0.0, -0.25, 0.0))
        ptIds.append(pts.InsertNextPoint(0.0, 0.25, 0.0))
        ptIds.append(pts.InsertNextPoint(-0.45, 0.25, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds)
        ptIds1 = []
        ptIds1.append(pts.InsertNextPoint(0.25, 0.40, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.25, -0.25, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.45, -0.25, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.45, 0.40, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds1)


class Bullseye(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        res = 10
        ptIds = vtk.vtkIdList()
        ptIds.SetNumberOfIds(res + 1)
        x = [0, 0, 0]
        theta = 2.0 * math.pi / res
        for i in range(res):
            x[0] = 0.30 * math.cos(i * theta)
            x[1] = 0.30 * math.sin(i * theta)
            ptIds.SetId(i, pts.InsertNextPoint(x))
        ptIds.SetId(res, ptIds.GetId(0))
        self.glyph.GetLines().InsertNextCell(ptIds)
        ptIds1 = []
        ptIds1.append(pts.InsertNextPoint(-0.05, -0.40, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.05, -0.40, 0.0))
        ptIds1.append(pts.InsertNextPoint(0.05, 0.40, 0.0))
        ptIds1.append(pts.InsertNextPoint(-0.05, 0.40, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds1)
        ptIds2 = []
        ptIds2.append(pts.InsertNextPoint(-0.40, -0.05, 0.0))
        ptIds2.append(pts.InsertNextPoint(0.40, -0.05, 0.0))
        ptIds2.append(pts.InsertNextPoint(0.40, 0.05, 0.0))
        ptIds2.append(pts.InsertNextPoint(-0.40, 0.05, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, ptIds2)

pattern_list = [Pattern, BottomLeftTri, TopRightTri, Dot, CheckerBoard,
                HorizStripe, VertStripe, HorizDash, VertDash, DashStripe,
                ThinDiagDownRight, ThickDiagDownRight, ThinDiagUpRight, ThickDiagUpRight,
                XCross, DoubleCross, Diamond, DoubleDiamond, Bubble, Snake, Bullseye]
