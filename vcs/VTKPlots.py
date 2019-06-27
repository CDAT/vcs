import cdutil
import warnings
import vtk
from vtk.util import numpy_support as VN
import vcs
from . import vcs2vtk
import numpy
import math
import os
import traceback
import sys
import cdms2
import cdtime
import inspect
import json
import subprocess
import tempfile
import shutil
from . import VTKAnimate
from . import vcsvtk


def _makeEven(val):
    if (val & 0x1):
        val -= 1
    return val


def updateNewElementsDict(display, master):
    newelts = getattr(display, "newelements", {})
    for key in newelts:
        if key in master:
            master[key] += newelts[key]
        else:
            master[key] = newelts[key]
    return master


class ImageDataWrapperItem(object):
    def __init__(self, image, scale=1.0, offset=[0.0, 0.0]):
        self.scale = scale
        self.xOffset = offset[0]
        self.yOffset = offset[1]
        self.imageData = image

    def Initialize(self, vtkSelf):
        return True

    def Paint(self, vtkSelf, context2D):
        scalars = self.imageData.GetPointData().GetScalars()
        if scalars:
            context2D.DrawImage(self.xOffset, self.yOffset, self.scale, self.imageData)
            return True

        print('ERROR: vtkImageData has no active scalars, unable to draw image')
        return False


class VcsLogoItem(object):
    def __init__(self, image, opacity=1.0, scale=1.0, offset=[0.0, 0.0],
                 transparentColor=[1.0, 1.0, 1.0]):
        self.scale = scale
        self.opacity = opacity
        self.xOffset = offset[0]
        self.yOffset = offset[1]
        self.transparentColor = transparentColor
        self.imageData = image
        self.ready = False

    def Initialize(self, vtkSelf):
        scalars = self.imageData.GetPointData().GetScalars()
        if not scalars:
            print('ERROR: vtkImageData has no active scalars, unable to draw logo')
            self.ready = False
        else:
            self.ready = True
            if self.opacity < 1.0:
                self.ready = self.ApplyOpacityToScalars()

        return self.ready

    def ApplyOpacityToScalars(self):
        # FIXME: This is the only way we can currently affect the opacity of
        # FIXME: the logo, as the vtKContext2D API does not yet provide any
        # FIXME: to set the opacity of a drawn image.  So we do is this way
        # FIXME: until that API can be provided.
        scalars = self.imageData.GetPointData().GetScalars()
        numComps = scalars.GetNumberOfComponents()

        if numComps != 4:
            wrngMsg = """WARNING: VcsLogoItem ignoring opacity because
            vtkImageData active scalars has {0} components instead of
            4""".format(numComps)
            print(wrngMsg)
            return False

        as_numpy = VN.vtk_to_numpy(scalars)
        as_numpy[:, 3] = as_numpy[:, 3] * self.opacity

        return True

    def Paint(self, vtkSelf, context2D):
        if self.ready:
            brush = context2D.GetBrush()
            brushColor = [0.0, 0.0, 0.0, 0.0]
            brush.GetColorF(brushColor)
            brush.SetColorF(self.transparentColor)

            context2D.DrawImage(self.xOffset, self.yOffset, self.scale, self.imageData)

            brush.SetColorF(brushColor[:3])
            return True

        # print('ERROR: VcsLogoItem is unable to Paint(), see earlier warnings')
        return False


class PopupInfoItem(object):
    def __init__(self, bgColor, fgColor, vp, text):
        self.bgColor = bgColor
        self.fgColor = fgColor
        self.vp = vp
        self.text = text
        self.bgRectDims = None

    def Initialize(self, vtkSelf):
        return True

    def Paint(self, vtkSelf, context2D):
        # Compute the size of the rectangle behind the text
        if not self.bgRectDims:
            stringBounds = [0, 0, 0, 0]
            context2D.ComputeStringBounds(self.text, stringBounds)
            self.bgRectDims = stringBounds[2:]

        rw, rh = self.bgRectDims

        # Save the previous brush color
        brush = context2D.GetBrush()
        prevBrushColor = [0.0, 0.0, 0.0, 0.0]
        prevBrushOpacity = brush.GetOpacityF()
        brush.GetColorF(prevBrushColor)

        # Save the previous pen color
        pen = context2D.GetPen()
        prevPenColor = [0.0, 0.0, 0.0]
        pen.GetColorF(prevPenColor)

        # Apply the quad color
        brush.SetColorF(*self.fgColor)
        brush.SetOpacityF(1.0)
        pen.SetColorF(*self.fgColor)

        x, y = self.vp[:2]

        # Compute the quad vertices
        xmin = x
        xmax = x + rw
        ymin = y
        ymax = y + rh

        context2D.DrawQuad(xmin, ymin,
                           xmin, ymax,
                           xmax, ymax,
                           xmax, ymin)

        pen.SetColorF(0.0, 0.0, 0.0)

        textProp = context2D.GetTextProp()
        prevJustification = textProp.GetJustification()
        prevTextColor = textProp.GetColor()
        textProp.SetColor(0, 0, 0)
        textProp.SetJustificationToLeft()
        context2D.ApplyTextProp(textProp)

        hh = rh * 0.5
        context2D.DrawString(x, y + hh, self.text)

        textProp.SetColor(prevTextColor)
        textProp.SetJustification(prevJustification)
        context2D.ApplyTextProp(textProp)

        # Restore pen/brush state
        pen.SetColorF(prevPenColor)
        brush.SetColorF(prevBrushColor[:3])
        brush.SetOpacityF(prevBrushOpacity)

        return True


class VCSInteractorStyle(vtk.vtkInteractorStyleUser):

    def __init__(self, parent):
        self.AddObserver("LeftButtonPressEvent", parent.leftButtonPressEvent)
        self.AddObserver(
            "LeftButtonReleaseEvent",
            parent.leftButtonReleaseEvent)
        self.AddObserver("ConfigureEvent", parent.configureEvent)
        if sys.platform == "darwin":
            self.AddObserver("RenderEvent", parent.renderEvent)


class VTKVCSBackend(object):

    def __init__(self, canvas, renWin=None,
                 debug=False, bg=None):
        self._lastSize = None
        self.canvas = canvas
        self.renWin = renWin
        self.contextView = None
        self.debug = debug
        self.bg = bg
        self.type = "vtk"
        self.plotApps = {}
        self.plotRenderers = set()
        # Maps priorities to renderers
        self.text_renderers = {}
        self.logoContextArea = None
        self.logoContextItem = None
        self.logoContextItemPython = None
        self.renderer = None
        self._renderers = {}
        self._plot_keywords = [
            'cdmsfile',
            'cell_coordinates',
            # dataset bounds in lon/lat coordinates
            'dataset_bounds',
            # This may be smaller than the data viewport. It is used
            # if autot is passed
            'ratio_autot_viewport',
            # used to render the dataset for clicked point info (hardware
            # selection)
            'surface_renderer',
            # (xScale, yScale) - datasets can be scaled using the window ratio
            'surface_scale',
            # the same as vcs.utils.getworldcoordinates for now. getworldcoordinates uses
            # gm.datawc_... or, if that is not set, it uses data axis margins
            # (without bounds).
            'plotting_dataset_bounds',
            # dataset bounds before masking
            'vtk_dataset_bounds_no_mask',
            'renderer',
            'vtk_backend_grid',
            # vtkGeoTransform used for geographic transformation
            'vtk_backend_geo',
            # "vtk_backend_pipeline_context_area",
            "vtk_backend_viewport_scale",
            "vtk_backend_draw_area_bounds",
        ]
        self.numberOfPlotCalls = 0
        self.renderWindowSize = None
        self.clickRenderer = None
        # Turn on anti-aliasing by default
        # Initially set to 16x Multi-Sampled Anti-Aliasing
        self.antialiasing = 8

        self.popupInfoContextArea = None

        if renWin is not None:
            self.renWin = renWin
            if renWin.GetInteractor() is None and self.bg is False:
                self.createDefaultInteractor()

        if sys.platform == "darwin":
            self.reRender = False
            self.oldCursor = None

        self._animationActorTransforms = {}

    def setAnimationStepper(self, stepper):
        for plot in list(self.plotApps.values()):
            plot.setAnimationStepper(stepper)

    def interact(self, *args, **kargs):
        if self.renWin is None:
            warnings.warn("Cannot interact if you did not open the canvas yet")
            return
        interactor = self.renWin.GetInteractor()
        # Mac seems to handle events a bit differently
        # Need to add observers on renWin
        # Linux is fine w/o it so no need to do it
        if sys.platform == "darwin":
            self.renWin.AddObserver("RenderEvent", self.renderEvent)
            self.renWin.AddObserver(
                "LeftButtonPressEvent",
                self.leftButtonPressEvent)
            self.renWin.AddObserver(
                "LeftButtonReleaseEvent",
                self.leftButtonReleaseEvent)
            self.renWin.AddObserver("ConfigureEvent", self.configureEvent)
            self.renWin.AddObserver("EndEvent", self.endEvent)
        if interactor is None:
            warnings.warn("Cannot start interaction. Blank plot?")
            return
        warnings.warn(
            "Press 'Q' to exit interactive mode and continue script execution")
        self.showGUI()
        interactor.Start()

    def endEvent(self, obj, event):
        if self.renWin is not None:
            if self.reRender:
                self.reRender = False
                self.renWin.Render()

    def renderEvent(self, caller, evt):
        # print('renderEvent')
        renwin = self.renWin if (caller is None) else caller
        window_size = renwin.GetSize()
        if (window_size != self.renderWindowSize):
            self.configureEvent(caller, evt)
            self.renderWindowSize = window_size

    def leftButtonPressEvent(self, obj, event):
        pipelineItems = None
        dataset = None
        targetDisplay = None
        st = ''

        for dnm in self.canvas.display_names:
            d = vcs.elements["display"][dnm]
            if d.array[0] is None:
                continue
            else:
                targetDisplay = d
                dataset = d.backend['vtk_backend_grid']
                pipelineItems = d.backend['vtk_backend_actors']

        if (pipelineItems is not None and
                len(pipelineItems) > 0 and
                dataset is not None):
            # FIXME: This render call is needed to work around a bug somewhere in the
            # FIXME: vtkContextTransform code, where the transformation represented by
            # FIXME: Map[To|From]Scene() isn't set up properly until after a render call.
            # FIXME: In this particular case, the issue only affected Python 3
            self.renWin.Render()

            # Just the first vtkContextItem within the backend context area
            # should have the transformation information required to map the
            # screen coords to world coords
            item = pipelineItems[0][0]

            xy = self.renWin.GetInteractor().GetEventPosition()

            screenPos = vtk.vtkVector2f(xy[0], xy[1])
            worldCoords = item.MapFromScene(screenPos)

            cellLocator = vtk.vtkCellLocator()
            cellLocator.SetDataSet(dataset)
            cellLocator.BuildLocator()

            testPoint = [worldCoords[0], worldCoords[1], 0.0]
            closestPoint = [0, 0, 0]
            distance = vtk.mutable(-1)
            cellId = vtk.mutable(-1)
            subId = vtk.mutable(-1)
            cellLocator.FindClosestPoint(testPoint, closestPoint, cellId, subId, distance)

            globalIds = dataset.GetCellData().GetGlobalIds()
            if globalIds:
                globalId = [0]
                globalIds.GetTypedTuple(cellId, globalId)
                globalId = globalId[0]
            else:
                print('ERROR: no globalIds, cannot handle left button press')
                return

            st += "Var: %s\n" % targetDisplay.array[0].id

            attributes = dataset.GetCellData().GetScalars()
            if (attributes is None):
                attributes = dataset.GetCellData().GetVectors()
            elementId = globalId

            geoTransform = targetDisplay.backend['vtk_backend_geo']
            if (geoTransform):
                geoTransform.Inverse()

            worldCoords = [worldCoords[0], worldCoords[1], 0.0]
            lonLat = worldCoords
            if (attributes is None):
                # if point dataset, return the value for the
                # closest point
                cell = dataset.GetCell(globalId)
                closestPoint = [0, 0, 0]
                subId = vtk.mutable(0)
                pcoords = [0, 0, 0]
                dist2 = vtk.mutable(0)
                weights = [0] * cell.GetNumberOfPoints()
                cell.EvaluatePosition(worldCoords, closestPoint,
                                      subId, pcoords, dist2, weights)
                indexMax = numpy.argmax(weights)
                pointId = cell.GetPointId(indexMax)
                attributes = dataset.GetPointData().GetScalars()
                if (attributes is None):
                    attributes = dataset.GetPointData().GetVectors()
                elementId = pointId
            if (geoTransform):
                geoTransform.InternalTransformPoint(
                    worldCoords, lonLat)
                geoTransform.Inverse()
            if (float("inf") not in lonLat):
                st += "X=%4.1f\nY=%4.1f\n" % (
                    lonLat[0], lonLat[1])
            # get the cell value or the closest point value
            if (attributes):
                if (attributes.GetNumberOfComponents() > 1):
                    v = attributes.GetTuple(elementId)
                    st += "Value: (%g, %g)" % (v[0], v[1])
                else:
                    value = attributes.GetValue(elementId)
                    st += "Value: %g" % value

        if st == "":
            return

        if not self.popupInfoContextArea:
            # print('Building the popup stuff')
            self.popupInfoContextArea = vtk.vtkContextArea()
            self.contextView.GetScene().AddItem(self.popupInfoContextArea)

            [renWinWidth, renWinHeight] = self.renWin.GetSize()
            screenGeom = vtk.vtkRecti(0, 0, renWinWidth, renWinHeight)
            drawAreaBounds = vtk.vtkRectd(0.0, 0.0, float(renWinWidth), float(renWinHeight))
            vcs2vtk.configureContextArea(self.popupInfoContextArea, drawAreaBounds, screenGeom)

            popupPythonItem = PopupInfoItem(bgColor=[.96, .96, .86],
                                            fgColor=[.93, .91, .67],
                                            vp=[xy[0], xy[1], min(xy[0] + .2, 1.), min(xy[1] + .2, 1)],
                                            text=st)
            popupItem = vtk.vtkPythonItem()
            popupItem.SetPythonObject(popupPythonItem)
            self.popupInfoContextArea.GetDrawAreaItem().AddItem(popupItem)

            self.renWin.Render()

    def leftButtonReleaseEvent(self, obj, event):
        if self.popupInfoContextArea:
            # print('Cleaning up the popup stuff')
            self.popupInfoContextArea.ClearItems()
            self.contextView.GetScene().RemoveItem(self.popupInfoContextArea)
            self.popupInfoContextArea = None

            self.renWin.Render()

    def configureEvent(self, obj, ev):
        if not self.renWin:
            return

        if self.get3DPlot() is not None:
            return

        sz = self.renWin.GetSize()
        if self._lastSize == sz:
            # We really only care about resize event
            # this is mainly to avoid segfault vwith Vistraisl which does
            # not catch configure Events but only modifiedEvents....
            return

        self._lastSize = sz
        plots_args = []
        key_args = []

        new = {}
        original_displays = list(self.canvas.display_names)
        for dnm in self.canvas.display_names:
            d = vcs.elements["display"][dnm]
            # displays keep a reference of objects that were internally created
            # so that we can clean them up
            # it is stored in display.newelements
            # here we compile the list of all these objects
            new = updateNewElementsDict(d, new)

            # Now we need to save all that was plotted so that we can replot
            # on the new sized template
            # that includes keywords passed
            parg = []
            if d.g_type in ["text", "textcombined"]:
                continue
            for a in d.array:
                if a is not None:
                    parg.append(a)
            parg.append(d._template_origin)
            parg.append(d.g_type)
            parg.append(d.g_name)
            plots_args.append(parg)
            # remember display used so we cna re-use
            key = {"display_name": dnm}
            if d.ratio is not None:
                key["ratio"] = d.ratio
            key["continents"] = d.continents
            key["continents_line"] = d.continents_line
            key_args.append(key)

        # Have to pull out the UI layer so it doesn't get borked by the z
        self.hideGUI()

        if self.canvas.configurator is not None:
            restart_anim = self.canvas.configurator.animation_timer is not None
        else:
            restart_anim = False

        # clear canvas no render and preserve display
        # so that we can replot on same display object
        self.canvas.clear(render=False, preserve_display=True)

        # replots on new sized canvas
        for i, pargs in enumerate(plots_args):
            self.canvas.plot(*pargs, render=False, **key_args[i])

        # compiled updated list of all objects created internally
        for dnm in self.canvas.display_names:
            d = vcs.elements["display"][dnm]
            new = updateNewElementsDict(d, new)

        # Now clean the object created internally that are no longer
        # in use
        for e in new:
            if e == "display":
                continue
            # Loop for all types
            for k in new[e]:
                # Loop through all elements created internally for that type
                if k in vcs.elements[e]:
                    found = False
                    # Loop through all existing displays
                    for d in list(vcs.elements["display"].values()):
                        if d.g_type == e and d.g_name == k:
                            # Ok this is still in use on some display
                            found = True
                    # object is no longer associated with any display
                    # and it was created internally
                    # we can safely remove it
                    if not found:
                        del(vcs.elements[e][k])

        # Only keep original displays since we replotted on them
        for dnm in self.canvas.display_names:
            if dnm not in original_displays:
                del(vcs.elements["display"][dnm])
        # restore original displays
        self.canvas.display_names = original_displays

        if self.canvas.animate.created() and self.canvas.animate.frame_num != 0:
            self.canvas.animate.draw_frame(
                allow_static=False,
                render_offscreen=False)

        self.showGUI(render=False)
        if self.renWin.GetSize() != (0, 0):
            self.scaleLogo()
        if restart_anim:
            self.canvas.configurator.start_animating()

    def clear(self, render=True):
        if self.renWin is None:  # Nothing to clear
            return
        renderers = self.renWin.GetRenderers()
        renderers.InitTraversal()
        ren = renderers.GetNextItem()
        self.text_renderers = {}
        hasValidRenderer = True if ren is not None else False

        for gm in self.plotApps:
            app = self.plotApps[gm]
            app.plot.quit()

        self.hideGUI()

        if self.contextView:
            if self.popupInfoContextArea:
                # print('Cleaning up the popup stuff')
                self.popupInfoContextArea.ClearItems()
                self.contextView.GetScene().RemoveItem(self.popupInfoContextArea)
                self.popupInfoContextArea = None

            self.contextView.GetScene().ClearItems()
            r, g, b = [c / 255. for c in self.canvas.backgroundcolor]
            self.contextView.GetRenderer().SetBackground(r, g, b)

            if self.logoContextItem:
                self.logoContextArea.ClearItems()
                self.contextView.GetScene().RemoveItem(self.logoContextArea)
                self.logoContextArea = None
                self.logoContextItem = None
                self.logoContextItemPython = None

        self._animationActorTransforms = {}

        self.showGUI(render=False)

        if hasValidRenderer and self.renWin.IsDrawable() and render:
            self.renWin.Render()
        self.numberOfPlotCalls = 0
        self.logoRenderer = None
        self.createLogo()
        self._renderers = {}

    def createDefaultInteractor(self, ren=None):
        # defaultInteractor = self.renWin.GetInteractor()
        defaultInteractor = self.contextView.GetInteractor()
        if defaultInteractor is None:
            if self.bg:
                # this is only used to pass event to vtk objects
                # it does not listen to events form the window
                # it is used in vtkweb
                defaultInteractor = vtk.vtkGenericRenderWindowInteractor()
            else:
                defaultInteractor = vtk.vtkRenderWindowInteractor()
        self.vcsInteractorStyle = VCSInteractorStyle(self)
        if ren:
            self.vcsInteractorStyle.SetCurrentRenderer(ren)
        defaultInteractor.SetInteractorStyle(self.vcsInteractorStyle)
        defaultInteractor.SetRenderWindow(self.renWin)
        self.vcsInteractorStyle.On()

    def createRenWin(self, *args, **kargs):
        if self.contextView is None:
            self.contextView = vtk.vtkContextView()

        if self.renWin is None:
            self.renWin = self.contextView.GetRenderWindow()

            self.renWin.SetWindowName("VCS Canvas %i" % self.canvas._canvas_id)
            self.renWin.SetAlphaBitPlanes(1)
            # turning on Stencil for Labels on iso plots
            self.renWin.SetStencilCapable(1)
            # turning off antialiasing by default
            # mostly so that pngs are same accross platforms
            self.renWin.SetMultiSamples(self.antialiasing)

            width = self.canvas.width
            height = self.canvas.height

            if "width" in kargs and kargs["width"] is not None:
                width = kargs["width"]
            if "height" in kargs and kargs["height"] is not None:
                height = kargs["height"]
            self.initialSize(width, height)

        if self.renderer is None:
            self.renderer = self.contextView.GetRenderer()
            r, g, b = [c / 255. for c in self.canvas.backgroundcolor]
            self.renderer.SetBackground(r, g, b)
            self.createDefaultInteractor(self.renderer)

        if self.bg:
            self.renWin.SetOffScreenRendering(True)

        if "open" in kargs and kargs["open"]:
            self.renWin.Render()

    def createRenderer(self, *args, **kargs):
        if not self.renderer:
            self.createRenWin(*args, **kargs)
        return self.renderer

    def update(self, *args, **kargs):
        self._lastSize = None
        if self.renWin:
            if self.get3DPlot():
                plots_args = []
                key_args = []
                for dnm in self.canvas.display_names:
                    d = vcs.elements["display"][dnm]
                    parg = []
                    for a in d.array:
                        if a is not None:
                            parg.append(a)
                    parg.append(d._template_origin)
                    parg.append(d.g_type)
                    parg.append(d.g_name)
                    plots_args.append(parg)
                    if d.ratio is not None:
                        key_args.append({"ratio": d.ratio})
                    else:
                        key_args.append({})
                for i, args in enumerate(plots_args):
                    self.canvas.plot(*args, **key_args[i])
            else:
                self.configureEvent(None, None)

    def canvasinfo(self):
        if self.renWin is None:
            mapstate = False
            width = self.canvas.width
            height = self.canvas.height
            depth = None
            x = 0
            y = 0
        else:
            try:  # mac but not linux
                mapstate = self.renWin.GetWindowCreated()
            except Exception:
                mapstate = True
            width, height = self.renWin.GetSize()
            depth = self.renWin.GetDepthBufferSize()
            try:  # mac not linux
                x, y = self.renWin.GetPosition()
            except Exception:
                x, y = 0, 0
        info = {
            "mapstate": mapstate,
            "height": height,
            "width": width,
            "depth": depth,
            "x": x,
            "y": y,
        }
        return info

    def orientation(self, *args, **kargs):
        canvas_info = self.canvasinfo()
        w = canvas_info["width"]
        h = canvas_info["height"]
        if w > h:
            return "landscape"
        else:
            return "portrait"

    def resize_or_rotate_window(self, W=-99, H=-99, x=-99, y=-99, clear=0):
        # Resize and position window to the provided arguments except when the
        # values are default and negative. In the latter case, it should just
        # rotate the window.
        if clear:
            self.clear()
        if self.renWin is None:
            if W != -99:
                self.canvas.width = W
                self.canvas.height = H
            else:
                W = self.canvas.width
        else:
            self.setsize(W, H)
            self.canvas.width = W
            self.canvas.height = H

    def portrait(self, W=-99, H=-99, x=-99, y=-99, clear=0):
        self.resize_or_rotate_window(W, H, x, y, clear)

    def landscape(self, W=-99, H=-99, x=-99, y=-99, clear=0):
        self.resize_or_rotate_window(W, H, x, y, clear)

    def initialSize(self, width=None, height=None):
        import vtkmodules
        if hasattr(vtkmodules.vtkRenderingOpenGL2Python, "vtkXOpenGLRenderWindow") and\
                isinstance(self.renWin, vtkmodules.vtkRenderingOpenGL2Python.vtkXOpenGLRenderWindow):
            if os.environ.get("DISPLAY", None) is None:
                raise RuntimeError("No DISPLAY set. Set your DISPLAY env variable or install mesalib conda package")

        # Gets user physical screen dimensions
        if isinstance(width, int) and isinstance(height, int):
            self.setsize(width, height)
            self._lastSize = (width, height)
            return

        screenSize = self.renWin.GetScreenSize()
        try:
            # following works on some machines but not all
            # Creates the window to be 60% of user's screen's width
            cw = int(screenSize[0] * .6)
            ch = int(cw / self.canvas.size)
            if ch > screenSize[1]:
                # If still too big use 60% of height
                # typical case: @doutriaux1 screens
                ch = int(screenSize[1] * .6)
                cw = int(ch * self.canvas.size)
        except Exception:
            cw = self.canvas.width
        # Respect user chosen aspect ratio
        ch = int(cw / self.canvas.size)
        # Sets renWin dimensions
        # make the dimensions even for Macs
        cw = _makeEven(cw)
        ch = _makeEven(ch)
        self.canvas.width = cw
        self.canvas.height = ch
        self.setsize(cw, ch)
        self._lastSize = (cw, ch)

    def open(self, width=None, height=None, **kargs):
        self.createRenWin(open=True, width=width, height=height)

    def close(self):
        if self.renWin is None:
            return
        self.clear()
        self.renWin.Finalize()
        self.renWin = None

    def isopened(self):
        if self.renWin is None:
            return False
        elif self.renWin.GetOffScreenRendering() and self.bg:
            # IN bg mode
            return False
        else:
            return True

    def geometry(self, *args):
        if len(args) == 0:
            return {'width': self.canvas.width, 'height': self.canvas.height}
        if len(args) < 2:
            raise TypeError("Function takes zero or two <width, height> "
                            "or more than two arguments. Got " + len(*args))
        x = args[0]
        y = args[1]

        self.canvas.width = x
        self.canvas.height = y
        if self.renWin is not None:
            self.setsize(x, y)
        self._lastSize = (x, y)

    def setsize(self, x, y):
        self.renWin.SetSize(x, y)
        self.configureEvent(None, None)

    def flush(self):
        if self.renWin is not None:
            self.renWin.Render()

    def plot(self, data1, data2, template, gtype, gname, bg, *args, **kargs):
        self.numberOfPlotCalls += 1
        # these are keyargs that can be reused later by the backend.
        returned = {}
        if self.bg is None:
            if bg:
                self.bg = True
            else:
                self.bg = False
        self.createRenWin(**kargs)
        if self.bg:
            self.renWin.SetOffScreenRendering(True)
        self.cell_coordinates = kargs.get('cell_coordinates', None)
        self.canvas.initLogoDrawing()
        if gtype == "text":
            tt, to = gname.split(":::")
            tt = vcs.elements["texttable"][tt]
            to = vcs.elements["textorientation"][to]
            gm = tt
        elif gtype in ("xvsy", "xyvsy", "yxvsx", "scatter"):
            gm = vcs.elements["1d"][gname]
        else:
            gm = vcs.elements[gtype][gname]
        tpl = vcs.elements["template"][template]

        if kargs.get("renderer", None) is None:
            if (gtype in ["3d_scalar", "3d_dual_scalar", "3d_vector"]) and (
                    self.renderer is not None):
                ren = self.renderer
        else:
            ren = kargs["renderer"]

        vtk_backend_grid = kargs.get("vtk_backend_grid", None)
        vtk_dataset_bounds_no_mask = kargs.get(
            "vtk_dataset_bounds_no_mask", None)
        vtk_backend_geo = kargs.get("vtk_backend_geo", None)
        bounds = vtk_dataset_bounds_no_mask if vtk_dataset_bounds_no_mask else None

        pipeline = vcsvtk.createPipeline(gm, self, kargs)
        if pipeline is not None:
            returned.update(pipeline.plot(data1, data2, tpl,
                                          vtk_backend_grid, vtk_backend_geo, **kargs))
        elif gtype in ["3d_scalar", "3d_dual_scalar", "3d_vector"]:
            cdms_file = kargs.get('cdmsfile', None)
            cdms_var = kargs.get('cdmsvar', None)
            if cdms_var is not None:
                raise Exception()
            if cdms_file is not None:
                gm.addPlotAttribute('file', cdms_file)
                gm.addPlotAttribute('filename', cdms_file)
                gm.addPlotAttribute('url', cdms_file)
            returned.update(self.plot3D(data1, data2, tpl, gm, ren, **kargs))
        elif gtype in ["text"]:
            if tt.priority != 0:
                # FIXME: May eventually want to use this key to store the context
                # FIXME: area we create so that we don't have to recompute the projected
                # FIXME: bounds.
                # tt_key = (
                #     tt.priority, tuple(
                #         tt.viewport), tuple(
                #         tt.worldcoordinate), tt.projection)

                if vcs.elements["projection"][tt.projection].type != "linear":
                    plotting_bounds = kargs.get(
                        "plotting_dataset_bounds", None)
                    if plotting_bounds:
                        newbounds = vcs2vtk.getProjectedBoundsForWorldCoords(
                            plotting_bounds, tt.projection)
                        if all([not math.isinf(b) for b in newbounds]):
                            bounds = newbounds

                view = self.contextView

                area = vtk.vtkContextArea()
                view.GetScene().AddItem(area)

                vp = self.canvas._viewport
                wc = self.canvas._worldcoordinate

                [renWinWidth, renWinHeight] = self.renWin.GetSize()
                geom = vtk.vtkRecti(int(round(vp[0] * renWinWidth)),
                                    int(round(vp[2] * renWinHeight)),
                                    int(round((vp[1] - vp[0]) * renWinWidth)),
                                    int(round((vp[3] - vp[2]) * renWinHeight)))

                rect = vtk.vtkRectd(0.0, 0.0, float(renWinWidth), float(renWinHeight))

                vcs2vtk.configureContextArea(area, rect, geom)

                returned["vtk_backend_text_actors"] = vcs2vtk.genTextActor(
                    area,
                    to=to,
                    tt=tt,
                    cmap=self.canvas.colormap, geoBounds=bounds, geo=vtk_backend_geo)
        elif gtype == "line":
            if gm.priority != 0:
                vcs2vtk.prepLine(self, gm, geoBounds=bounds, cmap=self.canvas.colormap)
                # FIXME: we may need to keeep track of the context items generated here
                # returned["vtk_backend_line_actors"] = actors

        elif gtype == "marker":
            if gm.priority != 0:
                view = self.contextView

                area = vtk.vtkContextArea()
                view.GetScene().AddItem(area)

                vp = gm.viewport
                wc = gm.worldcoordinate

                [renWinWidth, renWinHeight] = self.renWin.GetSize()
                geom = vtk.vtkRecti(int(round(vp[0] * renWinWidth)),
                                    int(round(vp[2] * renWinHeight)),
                                    int(round((vp[1] - vp[0]) * renWinWidth)),
                                    int(round((vp[3] - vp[2]) * renWinHeight)))

                xScale, yScale, xc, yc, yd, flipX, flipY = self.computeScaleToFitViewport(
                    vp,
                    wc=wc,
                    geoBounds=None,
                    geo=None)

                newWc = [wc[0] * xScale, wc[1] * xScale, wc[2] * yScale, wc[3] * yScale]

                rect = vtk.vtkRectd(newWc[0], newWc[2], newWc[1] - newWc[0], newWc[3] - newWc[2])
                vcs2vtk.configureContextArea(area, rect, geom)

                actors = vcs2vtk.prepMarker(gm, [geom[2], geom[3]], scale=[xScale, yScale], cmap=self.canvas.colormap)
                returned["vtk_backend_marker_actors"] = actors

                for g, pd, geo in actors:
                    item = vtk.vtkPolyDataItem()
                    item.SetPolyData(g)

                    item.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_CELL_DATA)
                    colorArray = g.GetCellData().GetArray('Colors')

                    item.SetMappedColors(colorArray)
                    area.GetDrawAreaItem().AddItem(item)

        elif gtype == "fillarea":
            if gm.priority != 0:
                actors = vcs2vtk.prepFillarea(self, self.renWin, gm,
                                              cmap=self.canvas.colormap)
                returned["vtk_backend_fillarea_actors"] = actors
        else:
            raise Exception(
                "Graphic type: '%s' not re-implemented yet" %
                gtype)
        self.scaleLogo()

        if not kargs.get("donotstoredisplay", False) and kargs.get(
                "render", True):
            self.renWin.Render()

        return returned

    def setLayer(self, renderer, priority):
        n = self.numberOfPlotCalls + (priority - 1) * 200 + 1
        nMax = max(self.renWin.GetNumberOfLayers(), n + 1)
        self.renWin.SetNumberOfLayers(nMax)
        renderer.SetLayer(n)

    def plot3D(self, data1, data2, tmpl, gm, ren, **kargs):
        from DV3D.Application import DV3DApp
        requiresFileVariable = True
        self.canvas.drawLogo = False
        if (data1 is None) or (requiresFileVariable and not (isinstance(
                data1, cdms2.fvariable.FileVariable) or isinstance(data1, cdms2.tvariable.TransientVariable))):
            traceback.print_stack()
            raise Exception(
                "Error, must pass a cdms2 variable object as the first input to the dv3d gm ( found '%s')" %
                (data1.__class__.__name__))
        g = self.plotApps.get(gm, None)
        if g is None:
            g = DV3DApp(self.canvas, self.cell_coordinates)
            n_overview_points = 500000
            roi = None  # ( 0, 0, 50, 50 )
            g.gminit(
                data1,
                data2,
                roi=roi,
                axes=gm.axes,
                n_overview_points=n_overview_points,
                n_cores=gm.NumCores,
                renwin=ren.GetRenderWindow(),
                plot_attributes=gm.getPlotAttributes(),
                gmname=gm.g_name,
                cm=gm.cfgManager,
                **kargs)  # , plot_type = PlotType.List  )
            self.plotApps[gm] = g
            self.plotRenderers.add(g.plot.renderer)
        else:
            g.update(tmpl)
        return {}

    def onClosing(self, cell):
        for plot in list(self.plotApps.values()):
            if hasattr(plot, 'onClosing'):
                plot.onClosing(cell)

    def plotContinents(self, continentType, wc, projection, wrap, vp, priority, **kargs):
        if continentType in [0, None]:
            return
        continents_path = self.canvas._continentspath(continentType)
        if continents_path is None:
            return (None, 1, 1)
        xforward = vcs.utils.axisConvertFunctions[kargs.get('xaxisconvert', 'linear')]['forward']
        yforward = vcs.utils.axisConvertFunctions[kargs.get('yaxisconvert', 'linear')]['forward']
        contData = vcs2vtk.prepContinents(continents_path, xforward, yforward)
        contData = vcs2vtk.doWrapData(contData, wc, fastClip=False)

        if projection.type != "linear":
            cpts = contData.GetPoints()
            # we use plotting coordinates for doing the projection so
            # that parameters such that central meridian are set correctly.
            _, gcpts = vcs2vtk.project(cpts, projection, wc)
            contData.SetPoints(gcpts)

        contLine = self.canvas.getcontinentsline()

        # Color
        if contLine.colormap:
            cmap = vcs.getcolormap(contLine.colormap)
        else:
            cmap = self.canvas.getcolormap()

        if type(contLine.color[0]) in (float, int):
            c_index = int(contLine.color[0])
            color = cmap.index[c_index]
        else:
            color = contLine.color[0]

        color = [int((c / 100.0) * 255) for c in color]

        # view and interactive area
        view = self.contextView
        contBounds = kargs.get("vtk_backend_draw_area_bounds", None)

        area = vtk.vtkContextArea()
        view.GetScene().AddItem(area)

        [renWinWidth, renWinHeight] = self.renWin.GetSize()
        geom = vtk.vtkRecti(int(round(vp[0] * renWinWidth)),
                            int(round(vp[2] * renWinHeight)),
                            int(round((vp[1] - vp[0]) * renWinWidth)),
                            int(round((vp[3] - vp[2]) * renWinHeight)))

        vcs2vtk.configureContextArea(area, contBounds, geom)

        color_arr = vtk.vtkUnsignedCharArray()
        color_arr.SetNumberOfComponents(4)
        color_arr.SetName("Colors")

        for i in range(contData.GetNumberOfCells()):
            if len(color) == 4:
                color_arr.InsertNextTypedTuple(color)
            else:
                color_arr.InsertNextTypedTuple([color[0], color[1], color[2], 255])

        contData.GetCellData().AddArray(color_arr)

        # Handle line drawing properties (line width + stipple)
        intValue = vtk.vtkIntArray()
        intValue.SetNumberOfComponents(1)
        intValue.SetName("StippleType")
        intValue.InsertNextValue(vcs2vtk.getStipple(contLine.type[0]))
        contData.GetFieldData().AddArray(intValue)

        floatValue = vtk.vtkFloatArray()
        floatValue.SetNumberOfComponents(1)
        floatValue.SetName("LineWidth")
        floatValue.InsertNextValue(contLine.width[0])
        contData.GetFieldData().AddArray(floatValue)

        item = vtk.vtkPolyDataItem()
        item.SetPolyData(contData)
        item.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_CELL_DATA)
        item.SetMappedColors(color_arr)
        area.GetDrawAreaItem().AddItem(item)

    def renderTemplate(self, tmpl, data, gm, taxis,
                       zaxis, X=None, Y=None, **kargs):
        # view and interactive area
        view = self.contextView

        area = vtk.vtkContextArea()
        view.GetScene().AddItem(area)

        vp = self.canvas._viewport

        [renWinWidth, renWinHeight] = self.renWin.GetSize()
        geom = vtk.vtkRecti(int(round(vp[0] * renWinWidth)),
                            int(round(vp[2] * renWinHeight)),
                            int(round((vp[1] - vp[0]) * renWinWidth)),
                            int(round((vp[3] - vp[2]) * renWinHeight)))

        rect = vtk.vtkRectd(0.0, 0.0, float(renWinWidth), float(renWinHeight))

        vcs2vtk.configureContextArea(area, rect, geom)

        # ok first basic template stuff, let's store the displays
        # because we need to return actors for min/max/mean
        kargs["taxis"] = taxis
        kargs["zaxis"] = zaxis
        displays = tmpl.plot(
            self.canvas,
            data,
            gm,
            bg=self.bg,
            X=X,
            Y=Y,
            **kargs)
        returned = {}
        for d in displays:
            if d is None:
                continue
            texts = d.backend.get("vtk_backend_text_actors", [])
            for t in texts:
                # ok we had a text actor, let's see if it's min/max/mean
                txt = t.GetInput()
                s0 = txt.split()[0]
                if s0 in ["Min", "Max", "Mean"]:
                    returned["vtk_backend_%s_text_actor" % s0] = t
                else:
                    returned[
                        "vtk_backend_%s_text_actor" %
                        d.backend["vtk_backend_template_attribute"]] = t
            self.canvas.display_names.remove(d.name)
            del(vcs.elements["display"][d.name])
        # Sometimes user passes "date" as an attribute to replace date
        if hasattr(data, "user_date"):
            taxis = cdms2.createAxis(
                [cdtime.s2r(data.user_date, "days since 1900").value])
            taxis.designateTime()
            taxis.units = "days since 1900"
            if zaxis is not None and zaxis.isTime():
                zaxis = taxis
        if taxis is not None:
            try:
                tstr = str(
                    cdtime.reltime(
                        taxis[0],
                        taxis.units).tocomp(
                        taxis.getCalendar()))
                # ok we have a time axis let's display the time
                crdate = vcs2vtk.applyAttributesFromVCStmpl(tmpl, "crdate")
                crdate.string = tstr.split()[0].replace("-", "/")
                crtime = vcs2vtk.applyAttributesFromVCStmpl(tmpl, "crtime")
                crtime.string = tstr.split()[1]
                tt, to = crdate.name.split(":::")
                tt = vcs.elements["texttable"][tt]
                to = vcs.elements["textorientation"][to]
                if crdate.priority > 0:
                    actors = vcs2vtk.genTextActor(area, to=to, tt=tt)
                    returned["vtk_backend_crdate_text_actor"] = actors[0]
                del(vcs.elements["texttable"][tt.name])
                del(vcs.elements["textorientation"][to.name])
                del(vcs.elements["textcombined"][crdate.name])
                tt, to = crtime.name.split(":::")
                tt = vcs.elements["texttable"][tt]
                to = vcs.elements["textorientation"][to]
                if crtime.priority > 0:
                    actors = vcs2vtk.genTextActor(area, to=to, tt=tt)
                    returned["vtk_backend_crtime_text_actor"] = actors[0]
                del(vcs.elements["texttable"][tt.name])
                del(vcs.elements["textorientation"][to.name])
                del(vcs.elements["textcombined"][crtime.name])
            except:  # noqa
                pass
        if zaxis is not None:
            try:
                # ok we have a zaxis to draw
                zname = vcs2vtk.applyAttributesFromVCStmpl(tmpl, "zname")
                zname.string = zaxis.id
                zvalue = vcs2vtk.applyAttributesFromVCStmpl(tmpl, "zvalue")
                if zaxis.isTime():
                    zvalue.string = str(zaxis.asComponentTime()[0])
                else:
                    zvalue.string = "%g" % zaxis[0]
                tt, to = zname.name.split(":::")
                tt = vcs.elements["texttable"][tt]
                to = vcs.elements["textorientation"][to]
                if zname.priority > 0:
                    vcs2vtk.genTextActor(area, to=to, tt=tt)
                del(vcs.elements["texttable"][tt.name])
                del(vcs.elements["textorientation"][to.name])
                del(vcs.elements["textcombined"][zname.name])
                if hasattr(zaxis, "units"):
                    zunits = vcs2vtk.applyAttributesFromVCStmpl(tmpl, "zunits")
                    zunits.string = zaxis.units
                    if zunits.priority > 0:
                        tt, to = zunits.name.split(":::")
                        tt = vcs.elements["texttable"][tt]
                        to = vcs.elements["textorientation"][to]
                        vcs2vtk.genTextActor(area, to=to, tt=tt)
                        del(vcs.elements["texttable"][tt.name])
                        del(vcs.elements["textorientation"][to.name])
                        del(vcs.elements["textcombined"][zunits.name])
                tt, to = zvalue.name.split(":::")
                tt = vcs.elements["texttable"][tt]
                to = vcs.elements["textorientation"][to]
                if zvalue.priority > 0:
                    actors = vcs2vtk.genTextActor(area, to=to, tt=tt)
                    returned["vtk_backend_zvalue_text_actor"] = actors[0]
                del(vcs.elements["texttable"][tt.name])
                del(vcs.elements["textorientation"][to.name])
                del(vcs.elements["textcombined"][zvalue.name])
            except:  # noqa
                pass
        return returned

    def renderColorBar(self, tmpl, levels, colors, legend, cmap,
                       style=['solid'], index=[1], opacity=[],
                       pixelspacing=[15, 15], pixelscale=12):
        if tmpl.legend.priority > 0:
            tmpl.drawColorBar(
                colors,
                levels,
                x=self.canvas,
                legend=legend,
                cmap=cmap,
                style=style,
                index=index,
                opacity=opacity,
                pixelspacing=pixelspacing,
                pixelscale=pixelscale)
        return {}

    def put_png_on_canvas(
            self, filename, zoom=1, xOffset=0, yOffset=0,
            units="percent", fitToHeight=True, *args, **kargs):
        return self.put_img_on_canvas(
            filename, zoom, xOffset, yOffset, units, fitToHeight, *args, **kargs)

    def put_img_on_canvas(
            self, filename, zoom=1, xOffset=0, yOffset=0,
            units="percent", fitToHeight=True, *args, **kargs):
        self.createRenWin()
        winSize = self.renWin.GetSize()
        self.hideGUI()

        readerFactory = vtk.vtkImageReader2Factory()
        reader = readerFactory.CreateImageReader2(filename)
        reader.SetFileName(filename)
        reader.Update()
        imageData = reader.GetOutput()

        spc = imageData.GetSpacing()
        ext = imageData.GetExtent()

        imageWidth = ((ext[1] - ext[0]) + 1) * spc[0]
        imageHeight = ((ext[3] - ext[2]) + 1) * spc[1]

        if fitToHeight:
            yd = imageHeight
        else:
            yd = winSize[1]

        heightInWorldCoord = yd / zoom
        # window pixel in world (image) coordinates
        pixelInWorldCoord = heightInWorldCoord / winSize[1]

        if units[:7].lower() == "percent":
            xoff = winSize[0] * (xOffset / 100.) * pixelInWorldCoord
            yoff = winSize[1] * (yOffset / 100.) * pixelInWorldCoord
        elif units[:6].lower() == "pixels":
            xoff = xOffset * pixelInWorldCoord
            yoff = yOffset * pixelInWorldCoord
        else:
            raise RuntimeError(
                "vtk put image does not understand %s for offset units" %
                units)

        ctx2dScale = winSize[1] / heightInWorldCoord

        # compute scaled width/height of image
        sw = ctx2dScale * imageWidth
        sh = ctx2dScale * imageHeight

        # center of scaled image
        imgCx = sw * 0.5
        imgCy = sh * 0.5

        # center of canvas
        canCx = winSize[0] * 0.5
        canCy = winSize[1] * 0.5

        ctx2dxOff = (canCx - imgCx) + (xoff * ctx2dScale)
        ctx2dyOff = (canCy - imgCy) + (yoff * ctx2dScale)

        view = self.contextView

        area = vtk.vtkContextArea()
        view.GetScene().AddItem(area)

        screenGeom = vtk.vtkRecti(0, 0, winSize[0], winSize[1])
        dataBounds = vtk.vtkRectd(0.0, 0.0, winSize[0], winSize[1])

        vcs2vtk.configureContextArea(area, dataBounds, screenGeom)

        item = vtk.vtkPythonItem()
        item.SetPythonObject(ImageDataWrapperItem(imageData, scale=ctx2dScale, offset=[ctx2dxOff, ctx2dyOff]))
        area.GetDrawAreaItem().AddItem(item)

        self.showGUI(render=False)
        self.renWin.Render()
        return

    def hideGUI(self):
        plot = self.get3DPlot()

        if plot:
            plot.hideWidgets()
        elif not self.bg:
            from .vtk_ui.manager import get_manager, manager_exists
            if manager_exists(self.renWin.GetInteractor()):
                manager = get_manager(self.renWin.GetInteractor())
                manager.showing = False
                self.renWin.RemoveRenderer(manager.renderer)
                self.renWin.RemoveRenderer(manager.actor_renderer)

    def showGUI(self, render=True):
        plot = self.get3DPlot()

        if plot:
            plot.showWidgets()
        elif not self.bg:
            from .vtk_ui.manager import get_manager, manager_exists
            if manager_exists(self.renWin.GetInteractor()):
                manager = get_manager(self.renWin.GetInteractor())
                self.renWin.AddRenderer(manager.renderer)
                self.renWin.AddRenderer(manager.actor_renderer)
                manager.showing = True
                # Bring the manager's renderer to the top of the stack
                manager.elevate()
            if render:
                self.renWin.Render()

    def get3DPlot(self):
        from .dv3d import Gfdv3d
        plot = None
        for key in list(self.plotApps.keys()):
            if isinstance(key, Gfdv3d):
                plot = self.plotApps[key]
                break
        return plot

    def postscript(self, file, width=None, height=None,
                   units=None, textAsPaths=True):
        # create a temporary path we can use to write the pdf
        temporaryDirectoryName = tempfile.mkdtemp()
        tempPdfPath = os.path.join(temporaryDirectoryName, 'intermediate.pdf')

        # issue the call to create the pdf
        self.pdf(tempPdfPath, width, height, units, textAsPaths)

        # use supprocess.popen to use "pdf2ps" command-line on pdf file
        pdf2psArgs = [
            'pdf2ps',
            tempPdfPath,
            file
        ]

        proc = subprocess.Popen(pdf2psArgs,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        proc.wait()

        # We could checkout stdout and stderr, or just assume everything
        # went fine.

        # out = proc.stdout.read()
        # if out != "":
        #     print('pdf2ps output: {0}'.format(out))

        # errors = proc.stderr.read()
        # if errors != "":
        #     print('pdf2ps errors: {0}'.format(errors))

        # Delete the temporary path to clean up.
        shutil.rmtree(temporaryDirectoryName)

    def pdf(self, file, width=None, height=None, units=None, textAsPaths=True):
        self.hideGUI()

        exporter = vtk.vtkPDFExporter()
        exporter.SetRenderWindow(self.contextView.GetRenderWindow())
        exporter.SetFileName(file)
        exporter.Write()

        plot = self.get3DPlot()
        if plot:
            plot.showWidgets()

        self.showGUI()

    def svg(self, file, width=None, height=None, units=None, textAsPaths=True):
        self.hideGUI()

        exporter = vtk.vtkSVGExporter()
        exporter.SetRenderWindow(self.contextView.GetRenderWindow())
        exporter.SetFileName(file)
        # For large polydata, we can limit the number of triangles emitted during gradient subdivision.
        exporter.SetSubdivisionThreshold(10.0)
        exporter.Write()

        plot = self.get3DPlot()
        if plot:
            plot.showWidgets()

        self.showGUI()

    def gif(self, filename='noname.gif', merge='r', orientation=None,
            geometry='1600x1200'):
        raise RuntimeError("gif method not implemented in VTK backend yet")

    def png(self, file, width=None, height=None,
            units=None, draw_white_background=True, **args):

        if self.renWin is None:
            raise Exception("Nothing to dump aborting")

        if not file.split('.')[-1].lower() in ['png']:
            file += '.png'

        try:
            os.remove(file)
        except Exception:
            pass

        user_dims = None

        sz = self.renWin.GetSize()
        if width is not None and height is not None:
            if sz != (width, height):
                wrn = """You are saving to png of size different from the current canvas.
It is recommended to set the windows size before plotting or at init time.
This will lead to faster execution as well.
e.g
x=vcs.init(geometry=(1200,800))
#or
x=vcs.init()
x.geometry(1200,800)
"""
                warnings.warn(wrn)
                user_dims = (sz[0], sz[1])
                self.canvas.width = width
                self.canvas.height = height
                self.setsize(self.canvas.width, self.canvas.height)

        imgfiltr = vtk.vtkWindowToImageFilter()
        imgfiltr.SetInput(self.renWin)
        ignore_alpha = args.get('ignore_alpha', False)
        if ignore_alpha or draw_white_background:
            imgfiltr.SetInputBufferTypeToRGB()
        else:
            imgfiltr.SetInputBufferTypeToRGBA()

        self.hideGUI()
        self.renWin.Render()
        self.showGUI(render=False)

        writer = vtk.vtkPNGWriter()
        compression = args.get('compression', 5)  # get compression from user
        writer.SetCompressionLevel(compression)  # set compression level
        writer.SetInputConnection(imgfiltr.GetOutputPort())
        writer.SetFileName(file)
        # add text chunks to the writer
        m = args.get('metadata', {})
        for k, v in m.items():
            writer.AddText(k, json.dumps(v))
        writer.Write()
        if user_dims is not None:
            self.canvas.width, self.canvas.height = user_dims
            self.setsize(self.canvas.width, self.canvas.height)
            self.renWin.Render()

    def cgm(self, file):
        if self.renWin is None:
            raise Exception("Nothing to dump aborting")

        self.hideGUI()

        if not file.split('.')[-1].lower() in ['cgm']:
            file += '.cgm'

        try:
            os.remove(file)
        except Exception:
            pass

        plot = self.get3DPlot()
        if plot:
            plot.hideWidgets()

        writer = vtk.vtkIOCGM.vtkCGMWriter()
        writer.SetFileName(file)
        R = self.renWin.GetRenderers()
        r = R.GetFirstRenderer()
        A = r.GetActors()
        A.InitTraversal()
        a = A.GetNextActor()
        while a is not None:
            m = a.GetMapper()
            m.Update()
            writer.SetInputData(m.GetInput())
            writer.Write()
            a = A.GetNextActor()

        self.showGUI()

    def Animate(self, *args, **kargs):
        return VTKAnimate.VTKAnimate(*args, **kargs)

    def gettextextent(self, textorientation, texttable, angle=None):
        # Ensure renwin exists
        self.createRenWin()

        if isinstance(textorientation, str):
            textorientation = vcs.gettextorientation(textorientation)
        if isinstance(texttable, str):
            texttable = vcs.gettexttable(texttable)

        from .vtk_ui.text import text_box

        text_property = vtk.vtkTextProperty()
        info = self.canvasinfo()
        win_size = info["width"], info["height"]
        vcs2vtk.prepTextProperty(
            text_property,
            win_size,
            to=textorientation,
            tt=texttable)

        dpi = self.renWin.GetDPI()

        length = max(len(texttable.string), len(texttable.x), len(texttable.y))

        strings = texttable.string + \
            [texttable.string[-1]] * (length - len(texttable.string))
        xs = texttable.x + [texttable.x[-1]] * (length - len(texttable.x))
        ys = texttable.y + [texttable.y[-1]] * (length - len(texttable.y))

        labels = list(zip(strings, xs, ys))

        extents = []

        for s, x, y in labels:
            if angle is None:
                coords = text_box(
                    s, text_property, dpi, -textorientation.angle)
            else:
                coords = text_box(s, text_property, dpi, -angle)
            vp = texttable.viewport
            coords[0] = x +\
                (texttable.worldcoordinate[1] - texttable.worldcoordinate[0]) *\
                float(coords[0]) / win_size[0] / abs(vp[1] - vp[0])
            coords[1] = x +\
                (texttable.worldcoordinate[1] - texttable.worldcoordinate[0]) *\
                float(coords[1]) / win_size[0] / abs(vp[1] - vp[0])
            coords[2] = y +\
                (texttable.worldcoordinate[3] - texttable.worldcoordinate[2]) *\
                float(coords[2]) / win_size[1] / abs(vp[3] - vp[2])
            coords[3] = y +\
                (texttable.worldcoordinate[3] - texttable.worldcoordinate[2]) *\
                float(coords[3]) / win_size[1] / abs(vp[3] - vp[2])
            extents.append(coords)
        return extents

    def getantialiasing(self):
        if self.renWin is None:
            return self.antialiasing
        else:
            return self.renWin.GetMultiSamples()

    def setantialiasing(self, antialiasing):
        self.antialiasing = antialiasing
        if self.renWin is not None:
            self.renWin.SetMultiSamples(antialiasing)

    def createLogo(self):
        if self.canvas.drawLogo:
            if self.logoContextItem is None:
                defaultLogoFile = os.path.join(
                    vcs.vcs_egg_path,
                    "cdat.png")
                reader = vtk.vtkPNGReader()
                reader.SetFileName(defaultLogoFile)
                reader.Update()
                logo_input = reader.GetOutput()

                imgExtent = logo_input.GetExtent()
                imgWidth = imgExtent[1] - imgExtent[0] + 1.0
                imgHeight = imgExtent[3] - imgExtent[2] + 1.0

                item = vtk.vtkPythonItem()
                logoBgColor = [c / 255. for c in self.canvas.logo_transparentcolor]
                pythonItem = VcsLogoItem(logo_input, opacity=0.8,
                                         transparentColor=logoBgColor)
                item.SetPythonObject(pythonItem)

                position = [0.895, 0.0]
                position2 = [0.10, 0.05]

                [renWinWidth, renWinHeight] = self.renWin.GetSize()
                vpLowerLeftX = position[0] * renWinWidth
                vpLowerLeftY = position[1] * renWinHeight
                vpWidth = position2[0] * renWinWidth
                vpHeight = position2[1] * renWinHeight

                imgAspect = float(imgWidth) / imgHeight
                vpAspect = vpWidth / vpHeight

                if vpAspect > imgAspect:
                    # We'll use the full vp height and adjust it's width so that it's
                    # aspect ratio matches that of the image (so no stretching of the
                    # image occurs).  The image should be centered, so we'll offset
                    # position x value by half the difference.
                    vpWidth = vpHeight * imgAspect
                    halfDiff = ((position2[0] * renWinWidth) - vpWidth) / 2.0
                    vpLowerLeftX += halfDiff
                else:
                    # Similar to above, but in this case we choose to keep the vp width
                    # and adjust it's height.
                    vpHeight = vpWidth / imgAspect
                    halfDiff = ((position2[1] * renWinHeight) - vpHeight) / 2.0
                    vpLowerLeftY += halfDiff

                view = self.contextView

                area = vtk.vtkContextArea()
                view.GetScene().AddItem(area)

                dataBounds = vtk.vtkRectd(0.0, 0.0, imgWidth, imgHeight)
                screenGeom = vtk.vtkRecti(int(round(vpLowerLeftX)),
                                          int(round(vpLowerLeftY)),
                                          int(round(vpWidth)),
                                          int(round(vpHeight)))

                vcs2vtk.configureContextArea(area, dataBounds, screenGeom)
                area.GetDrawAreaItem().AddItem(item)

                self.logoContextArea = area
                self.logoContextItem = item
                self.logoContextItemPython = pythonItem

    def scaleLogo(self):
        if self.canvas.drawLogo:
            if self.renWin is not None:
                self.createLogo()

    def computeScaleToFitViewport(self, vp, wc, geoBounds=None, geo=None):
        vp = tuple(vp)
        Xrg = [float(wc[0]), float(wc[1])]
        Yrg = [float(wc[2]), float(wc[3])]

        sc = self.renWin.GetSize()

        if Yrg[0] > Yrg[1]:
            # Yrg=[Yrg[1],Yrg[0]]
            # T.RotateY(180)
            Yrg = [Yrg[1], Yrg[0]]
            flipY = True
        else:
            flipY = False
        if Xrg[0] > Xrg[1]:
            Xrg = [Xrg[1], Xrg[0]]
            flipX = True
        else:
            flipX = False

        if geo is not None and geoBounds is not None:
            Xrg = geoBounds[0:2]
            Yrg = geoBounds[2:4]

        wRatio = float(sc[0]) / float(sc[1])
        dRatio = (Xrg[1] - Xrg[0]) / (Yrg[1] - Yrg[0])
        vRatio = float(vp[1] - vp[0]) / float(vp[3] - vp[2])

        if wRatio > 1.:  # landscape orientated window
            yScale = 1.
            xScale = vRatio * wRatio / dRatio
        else:
            xScale = 1.
            yScale = dRatio / (vRatio * wRatio)

        xc = xScale * float(Xrg[1] + Xrg[0]) / 2.
        yc = yScale * float(Yrg[1] + Yrg[0]) / 2.
        yd = yScale * float(Yrg[1] - Yrg[0]) / 2.

        return (xScale, yScale, xc, yc, yd, flipX, flipY)

    def update_input(self, vtkobjects, array1, array2=None, update=True):
        if "vtk_backend_grid" in vtkobjects:
            # Ok ths is where we update the input data
            vg = vtkobjects["vtk_backend_grid"]
            vcs2vtk.setArray(vg, array1.filled(0).flat, "scalar",
                             isCellData=vg.GetCellData().GetScalars(),
                             isScalars=True)

            if "vtk_backend_filter" in vtkobjects:
                vtkobjects["vtk_backend_filter"].Update()
            if "vtk_backend_missing_mapper" in vtkobjects:
                missingMapper, color, cellData = vtkobjects[
                    "vtk_backend_missing_mapper"]
                missingMapper2 = vcs2vtk.putMaskOnVTKGrid(
                    array1,
                    vg,
                    color,
                    cellData,
                    deep=False)
            else:
                missingMapper = None
            if "vtk_backend_contours" in vtkobjects:
                for c in vtkobjects["vtk_backend_contours"]:
                    c.Update()
                ports = vtkobjects["vtk_backend_contours"]
            elif "vtk_backend_geofilters" in vtkobjects:
                ports = vtkobjects["vtk_backend_geofilters"]
            else:
                # Vector plot
                # TODO: this does not work with wrapping
                ports = vtkobjects["vtk_backend_glyphfilters"]
                w = vcs2vtk.generateVectorArray(array1, array2, vg)
                vg.GetPointData().AddArray(w)
                ports[0].SetInputData(vg)

            if "vtk_backend_actors" in vtkobjects:
                i = 0
                for a in vtkobjects["vtk_backend_actors"]:
                    beItem = a[0]
                    if a[1] is missingMapper:
                        i -= 1
                        mapper = missingMapper2
                    else:
                        # Labeled contours are a different kind
                        if "vtk_backend_luts" in vtkobjects:
                            lut, rg = vtkobjects["vtk_backend_luts"][i]
                            mapper = vtk.vtkPolyDataMapper()
                        elif "vtk_backend_labeled_luts" in vtkobjects:
                            lut, rg = vtkobjects["vtk_backend_labeled_luts"][i]
                            mapper = vtk.vtkLabeledContourMapper()

                        algo_i = ports[i]
                        coloring = None
                        scalarRange = None

                        if lut is not None:
                            if mapper.IsA("vtkPolyDataMapper"):
                                coloring = 'points'
                            else:
                                stripper = vtk.vtkStripper()
                                stripper.SetInputConnection(
                                    ports[i].GetOutputPort())
                                mapper.SetInputConnection(
                                    stripper.GetOutputPort())
                                algo_i = stripper
                                coloring = 'points'
                                scalarRange = rg

                            if rg[2]:
                                coloring = 'cells'

                            scalarRange = rg

                        algo_i.Update()
                        new_pd = algo_i.GetOutput()

                        beItem.SetPolyData(new_pd)

                        if coloring:
                            attrs = new_pd.GetPointData()
                            beItem.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_POINT_DATA)

                            if coloring == 'cells':
                                attrs = new_pd.GetCellData()
                                beItem.SetScalarMode(vtk.VTK_SCALAR_MODE_USE_CELL_DATA)

                            colorByArray = attrs.GetScalars()

                            if scalarRange:
                                lut.SetRange(scalarRange[0], scalarRange[1])

                            mappedColors = lut.MapScalars(colorByArray, vtk.VTK_COLOR_MODE_DEFAULT, 0)
                            beItem.SetMappedColors(mappedColors)
                            mappedColors.FastDelete()

                    i += 1

        taxis = array1.getTime()
        if taxis is not None:
            tstr = str(
                cdtime.reltime(
                    taxis[0],
                    taxis.units).tocomp(
                    taxis.getCalendar()))
        else:
            tstr = None
        # Min/Max/Mean
        for att in ["Min", "Max", "Mean", "crtime", "crdate", "zvalue"]:
            if "vtk_backend_%s_text_actor" % att in vtkobjects:
                t = vtkobjects["vtk_backend_%s_text_actor" % att]
                if att == "Min":
                    t.SetInput("Min %g" % array1.min())
                elif att == "Max":
                    t.SetInput("Max %g" % array1.max())
                elif att == "Mean":
                    if not inspect.ismethod(getattr(array1, 'mean')):
                        meanstring = "Mean: %s" % getattr(array1, "mean")
                    else:
                        try:
                            meanstring = 'Mean %.4g' % \
                                float(cdutil.averager(array1, axis=" ".join(["(%s)" %
                                                                             S for S in array1.getAxisIds()])))
                        except Exception:
                            try:
                                meanstring = 'Mean %.4g' % array1.mean()
                            except Exception:
                                meanstring = 'Mean %.4g' % numpy.mean(
                                    array1.filled())
                    t.SetInput(meanstring)
                elif att == "crdate" and tstr is not None:
                    t.SetInput(tstr.split()[0].replace("-", "/"))
                elif att == "crtime" and tstr is not None:
                    t.SetInput(tstr.split()[1])
                elif att == "zvalue":
                    if len(array1.shape) > 2:
                        tmp_l = array1.getAxis(-3)
                        if tmp_l.isTime():
                            t.SetInput(str(tmp_l.asComponentTime()[0]))
                        else:
                            t.SetInput("%g" % tmp_l[0])

        if update:
            self.renWin.Render()

    def png_dimensions(self, path):
        reader = vtk.vtkPNGReader()
        reader.SetFileName(path)
        reader.Update()
        img = reader.GetOutput()
        size = img.GetDimensions()
        return size[0], size[1]

    def raisecanvas(self):
        if self.renWin is None:
            warnings.warn("Cannot raise if you did not open the canvas yet.")
            return
        self.renWin.MakeCurrent()
