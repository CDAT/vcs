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
                y = [c * self.scale for c in x]
                pts.SetPoint(i, y)
        else:
            a = math.radians(self.rotation)
            for i in range(npts):
                x = pts.GetPoint(i)
                xt = x[0] * math.cos(a) - x[1] * math.sin(a)
                yt = x[0] * math.sin(a) + x[1] * math.cos(a)
                y = [xt, yt, 0]
                y = [c * self.scale for c in y]
                pts.SetPoint(i, y)


class BottomLeftTri(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        self.ptIds = []
        self.ptIds.append(pts.InsertNextPoint(-0.5, -0.5, 0.0))
        self.ptIds.append(pts.InsertNextPoint(-0.5, 0.25, 0.0))
        self.ptIds.append(pts.InsertNextPoint(0.25, -0.5, 0.0))
        self.glyph.GetPolys().InsertNextCell(3, self.ptIds)


class TopRightTri(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        self.ptIds = []
        self.ptIds.append(pts.InsertNextPoint(-0.25, 0.5, 0.0))
        self.ptIds.append(pts.InsertNextPoint(0.5, 0.5, 0.0))
        self.ptIds.append(pts.InsertNextPoint(0.5, -0.25, 0.0))
        self.glyph.GetPolys().InsertNextCell(3, self.ptIds)


class Dot(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        res = 10
        self.ptIds = vtk.vtkIdList()
        self.ptIds.SetNumberOfIds(res)
        x = [0, 0, 0]
        theta = 2.0 * math.pi / res
        for i in range(res):
            x[0] = 0.45 * math.cos(i * theta)
            x[1] = 0.45 * math.sin(i * theta)
            self.ptIds.SetId(i, pts.InsertNextPoint(x))
        self.glyph.GetPolys().InsertNextCell(self.ptIds)


class CheckerBoard(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        self.ptIds = []
        self.ptIds.append(pts.InsertNextPoint(-0.5, 0.5, 0.0))
        self.ptIds.append(pts.InsertNextPoint(0.0, 0.5, 0.0))
        self.ptIds.append(pts.InsertNextPoint(0.0, 0.0, 0.0))
        self.ptIds.append(pts.InsertNextPoint(-0.5, 0.0, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, self.ptIds)

        self.ptIds1 = []
        self.ptIds1.append(pts.InsertNextPoint(0.0, 0.0, 0.0))
        self.ptIds1.append(pts.InsertNextPoint(0.5, 0.0, 0.0))
        self.ptIds1.append(pts.InsertNextPoint(0.5, -0.5, 0.0))
        self.ptIds1.append(pts.InsertNextPoint(0.0, -0.5, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, self.ptIds1)


class HorizStripe(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        self.ptIds = []
        self.ptIds.append(pts.InsertNextPoint(-1.55, -0.25, 0.0))
        self.ptIds.append(pts.InsertNextPoint(1.55, -0.25, 0.0))
        self.ptIds.append(pts.InsertNextPoint(1.55, 0.25, 0.0))
        self.ptIds.append(pts.InsertNextPoint(-1.55, 0.25, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, self.ptIds)


class VertStripe(HorizStripe):

    def paint(self):
        pts = self.glyph.GetPoints()
        self.ptIds = []
        self.ptIds.append(pts.InsertNextPoint(-0.25, -1.55, 0.0))
        self.ptIds.append(pts.InsertNextPoint(0.25, -1.55, 0.0))
        self.ptIds.append(pts.InsertNextPoint(0.25, 1.55, 0.0))
        self.ptIds.append(pts.InsertNextPoint(-0.25, 1.55, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, self.ptIds)


class HorizDash(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        self.ptIds = []
        self.ptIds.append(pts.InsertNextPoint(-0.35, -0.10, 0.0))
        self.ptIds.append(pts.InsertNextPoint(0.35, -0.10, 0.0))
        self.ptIds.append(pts.InsertNextPoint(0.35, 0.10, 0.0))
        self.ptIds.append(pts.InsertNextPoint(-0.35, 0.10, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, self.ptIds)


class VertDash(HorizDash):

    def paint(self):
        pts = self.glyph.GetPoints()
        self.ptIds = []
        self.ptIds.append(pts.InsertNextPoint(-0.10, -0.35, 0.0))
        self.ptIds.append(pts.InsertNextPoint(0.10, -0.35, 0.0))
        self.ptIds.append(pts.InsertNextPoint(0.10, 0.35, 0.0))
        self.ptIds.append(pts.InsertNextPoint(-0.10, 0.35, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, self.ptIds)


class ThinDiagDownRight(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        self.ptIds = []
        self.ptIds.append(pts.InsertNextPoint(-0.5, 0.5, 0.0))
        self.ptIds.append(pts.InsertNextPoint(0.5, -0.5, 0.0))
        self.glyph.GetLines().InsertNextCell(2, self.ptIds)


class ThickDiagDownRight(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        self.ptIds = []
        self.ptIds.append(pts.InsertNextPoint(-1.55, 1.25, 0.0))
        self.ptIds.append(pts.InsertNextPoint(-1.55, 1.75, 0.0))
        self.ptIds.append(pts.InsertNextPoint(1.55, -1.25, 0.0))
        self.ptIds.append(pts.InsertNextPoint(1.55, -1.75, 0.0))
        self.glyph.GetPolys().InsertNextCell(4, self.ptIds)


class ThinDiagUpRight(Pattern):

    def paint(self):
        pts = self.glyph.GetPoints()
        self.ptIds = []
        self.ptIds.append(pts.InsertNextPoint(0.5, 0.5, 0.0))
        self.ptIds.append(pts.InsertNextPoint(-0.5, -0.5, 0.0))
        self.glyph.GetLines().InsertNextCell(2, self.ptIds)

#class DiagStripe(HorizStripe):
#
#    def paint(self):
#        HorizStripe.paint(self)
#        self.glyph.SetRotationAngle(45)
#
#
#class ReverseDiagStripe(DiagStripe):
#
#    def paint(self):
#        DiagStripe.paint(self)
#        self.glyph.SetRotationAngle(-45)
#
#
#class Cross(Pattern):
#
#    def paint(self):
#        self.glyph.CrossOn()
#        self.glyph.SetScale2(0.1)
#
#
#class FilledCross(Cross):
#
#    def paint(self):
#        self.glyph.SetGlyphTypeToThickCross()
#        self.glyph.FilledOn()
#
#
#class XCross(Cross):
#
#    def paint(self):
#        Cross.paint(self)
#        self.glyph.SetScale(self.scale * 2.0)
#        self.glyph.SetRotationAngle(45.0)
#
#
#class Diamond(Pattern):
#
#    def paint(self):
#        self.glyph.SetGlyphTypeToDiamond()
#
#
#class FilledDiamond(Diamond):
#
#    def paint(self):
#        Diamond.paint(self)
#        self.glyph.FilledOn()
#
#
#class Square(Pattern):
#
#    def paint(self):
#        self.glyph.SetGlyphTypeToSquare()
#
#
#class FilledSquare(Square):
#
#    def paint(self):
#        Square.paint(self)
#        self.glyph.FilledOn()
#
#
#class CircleCross(Pattern):
#
#    def paint(self):
#        self.glyph.SetGlyphTypeToCircle()
#        self.glyph.SetScale2(1.5)
#        self.glyph.CrossOn()
#
#
#class EdgeArrow(Pattern):
#
#    def paint(self):
#        self.glyph.SetGlyphTypeToEdgeArrow()
#
#
#class EdgeArrowInverted(EdgeArrow):
#
#    def paint(self):
#        EdgeArrow.paint(self)
#        self.glyph.SetRotationAngle(180)


# Patterns are 1-indexed, so we always skip the 0th element in this list
# pattern_list = [Pattern, LowerTriangle, UpperTriangle, Dot, FilledDot,
#                 HorizStripe, VertStripe, HorizDash, VertDash,
#                 DiagStripe, ReverseDiagStripe,
#                 Cross, FilledCross, XCross, Diamond, FilledDiamond,
#                 Square, FilledSquare, CircleCross, EdgeArrow, EdgeArrowInverted]
pattern_list = [Pattern, BottomLeftTri, TopRightTri, Dot, CheckerBoard,
                HorizStripe, VertStripe, HorizDash, VertDash, ThinDiagDownRight,
                ThickDiagDownRight, ThinDiagUpRight] #XDash, ThinDiagDownRight,
#                ThickDiagRownRight, ThinDiagUpRight, ThickDiagUpRight, ThickThinVertStripe,
#                ThickThinHorizStripe, LargeRectDot, Diamond, Bubble, Snake, EmptyCircle]
