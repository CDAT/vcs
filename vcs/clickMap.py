
import random
import vcs
import struct
import numpy


class Param(object):
    def __init__(self, area, target):
        self.area = area
        self.target = target


def createAreaTag(parameters):
    """Create an area tag to go along with an html map tag
    input: parameters object
    At the minimum parameter object needs thew following two attributes:
    "area": which describe the area polygon to be mapped
    "target":
    """
    area = parameters.area
    target = parameters.target
    tooltip = getattr(parameters, "tooltip", "")
    extras = getattr(parameters, "extras", "")
    clss = getattr(parameters, "classes", "")
    if tooltip.strip() != "":
        tooltip = 'tooltip="%s" onmouseover="cvi_tip._show(event);"' % tooltip
        tooltip += ' onmouseout="cvi_tip._hide(event);" onmousemove="cvi_tip._move(event);"'
    tag = "<area class='noborder iopacity35 {}' {} href='{}' {} shape='poly' ".format(
        clss, tooltip, target, extras)
    tag += " coords='" + ",".join(["%i, %i" % (x, y)
                                   for (x, y) in zip(area[0], area[1])]) + "'>\n"
    return tag


def mapPng(image, areas, targets=[], tooltips=[], classes=[],
           extras=[], width=None, height=None, name=None):
    """Return <map> and <img> code to map area of an image to various targets

    areas coords are assumed to be already mapped to witdth/height if passed

    :Example:

        .. doctest:: utils_mapPng

            >>> a=vcs.init(bg=True)
            >>> box=vcs.createboxfill()
            >>> array=[range(10) for _ in range(10)]
            >>> a.plot(box,array) # plot something on canvas
            <vcs.displayplot.Dp ...>
            >>> a.png('box.png', width=1536, height=1186) # make a png
            >>> fnm = cdat_info.get_sampledata_path()+"/clt.nc"
            >>> f=cdms2.open(fnm)
            >>> clt=f("clt",time=slice(0,1),squeeze=1)
            >>> mesh = clt.getGrid().getMesh()
            >>> template = vcs.createtemplate()
            >>> areas = meshToPngCoords(mesh, template,
                                     worldCoordinates=[gm.datawc_x1, gm.datawc_x2, gm.datawc_y1, gm.datawc_y2],
                                     png='box.png')
            >>> targets = clt.asma().ravel().astype(str).tolist()
            >>> img = mapPng('box.png',areas,targets,width=1536,height=1186)

    :param image: String specifying the path to a .png file
    :type image: `str`_

    :param areas: list of each polygon coordinate on the image
    :type areas: `list`_

    :param targets: list of target URL for each area tag. List will be completed with '#'s to match length of areas
    :type targets: `list`_

    :param tooltips: list of tooltips html code for each area tag. List will be completed with ''s
                     to match length of areas
    :type tooltips: `list`_

    :param classes: list of classes for each area tag. List will be completed with ''s
                    to match length of areas
    :type tooltips: `list`_

    :param extras: list of extras attributes to add to the area tag. List will be completed with ''s
                   to match length of areas
    :type tooltips: `list`_

    :param width: width of image on html page
    :type width: `int`_

    :param height: height of image on html page
    :type height: `int`_

    :param name: name <map> tag to use
    :type name: `str`_

    :return: A string containing the html code for mapping to image
    :rtype: `str`_
    """
    if width is not None:
        width = " width=%i" % width
    else:
        width = ""
    if height is not None:
        height = " height=%i" % height
    else:
        height = ""
    if name is None:
        name = "map_%i" % random.randint(0, 999999)
    # HTML5 requires both to be identical
    st = "<map id='%s' name='%s'>\n" % (name, name)

    params = []

    for i, a in enumerate(areas):
        try:
            target = targets[i]
        except Exception:
            target = "#"
        p = Param(a, target)
        try:
            tip = tooltips[i]
            p.tooltip = tip
        except Exception:
            pass
        try:
            xtra = extras[i]
            p.extras = xtra
        except Exception:
            pass
        try:
            clss = classes[i]
            p.classes = clss
        except Exception:
            pass
        params.append(p)

    area_tags = list(map(createAreaTag, params))
    st += "".join(area_tags)
    st += "</map>\n"
    st += "<div><img class='mapper' src='%s' %s %s usemap='#%s'></div>" % (
        image, width, height, name)
    return st


def getPngDimensions(pngFile):
    """Returns png dimensions

    :param pngFile: png file to extract dimensions from
    :type pngFile: `str`_

    :return: A tuple contain the png width,height
    :rtype: `tuple`_
    """

    with open(pngFile, "rb") as f:
        data = f.read()

    w, h = struct.unpack('>LL', data[16:24])
    width = int(w)
    height = int(h)
    return width, height


def worldToPixel(coords, mn, mx, p1, p2):
    """Maps world coordinates to pixels

    :param coords: array-like of values in worldcoordinate
    :type coords: `numpy.ndarray`_

    :param mn: value at first pixel to be mapped
    :type mn: `float`_

    :param mx: value at second pixel to be mapped
    :type mx: `float`_

    :param p1: value of first pixel we are mapping into
    :type p1: `float`_

    :param p2: value of second pixel we are mapping into
    :type p2: `float`_

    :return: An array with pixels corresponding to the value passed in
    :rtype: `numpy.ndarray`_
    """
    if isinstance(coords, (list, tuple)):
        coords = numpy.array(coords)
    span = mx - mn
    length = p2 - p1
    pixels = ((coords - mn) / span * length) + p1
    # crop to domain
    pixels = numpy.where(numpy.less(pixels, p1), p1, pixels)
    pixels = numpy.where(numpy.greater(pixels, p2), p2, pixels)
    return pixels


def axisToPngCoords(values, gm, template, axis='x1', worldCoordinates=[
                 0, 360, -90, 90], png=None, geometry=None):
    """
    Given a set of axis values/labels, a graphic method and a template, maps each label to an area on pmg
    Warning does not handle projections yet.
    :Example:

        .. doctest:: utils_axisToPngCoords

            >>> a=vcs.init(bg=True)
            >>> box=vcs.createboxfill()
            >>> array=[range(10) for _ in range(10)]
            >>> a.plot(box,array) # plot something on canvas
            <vcs.displayplot.Dp ...>
            >>> a.png('box.png', width=1536, height=1186) # make a png
            >>> fnm = cdat_info.get_sampledata_path()+"/clt.nc"
            >>> f=cdms2.open(fnm)
            >>> clt=f("clt",time=slice(0,1),squeeze=1)
            >>> box = vcs.createboxfill()
            >>> template = vcs.createtemplate()
            >>> areas = axisToPngCoords(clt.getLongitude(), box, template)
    """
    if png is None and geometry is None:
        x = vcs.init()
        x.open()
        ci = x.canvasinfo()
        x.close()
        del(x)
        pwidth = width = ci["width"]
        pheight = height = ci["height"]
    if png is not None:
        pwidth, pheight = getPngDimensions(png)
        if geometry is None:
            width, height = pwidth, pheight
    if geometry is not None:
        width, height = geometry
    if isinstance(template, str):
        template = vcs.gettemplate(template)
    x = vcs.init(geometry=(width, height), bg=True)

    # x/y ratio to original png
    xRatio = float(width) / pwidth
    yRatio = float(height) / pheight

    # Prepare dictionary of values, labels pairs

    mapped = []
    direction = axis[0]
    if direction == "x":
        other_direction = "y"
        c1 = int(width * template.data.x1 * xRatio)
        c2 = int(width * template.data.x2 * xRatio)
    else:
        other_direction = "x"
        c1 = int(height * template.data.y1 * yRatio)
        c2 = int(height * template.data.y2 * yRatio)

    location = axis[-1]

    datawc1 = getattr(gm, "datawc_{}1".format(direction))

    if datawc1 == 1.e20:
        start = values[0]
        end = values[-1]
    else:
        start = datawc1
        end = getattr(gm, "datawc_{}2".format(direction))

    label = getattr(template, "{}label{}".format(direction, location))
    Tt_source = label.texttable
    To_source = label.textorientation

    text = vcs.createtext(Tt_source=Tt_source, To_source=To_source)
    setattr(text, other_direction, getattr(label, other_direction))

    if direction == "x":
        text.worldcoordinate = [start, end, 0, 1]
    else:
        text.worldcoordinate = [0, 1, start, end]

    ticlabels = getattr(gm, "{}ticlabels{}".format(direction, location))

    if ticlabels == "*":
        lbls = vcs.mklabels(vcs.mkscale(start, end))
    else:
        lbls = ticlabels
    # now loops thru all labels and get extents
    for v, l in lbls.items():
        if start <= v and v <= end:
            text.string = str(l)
            setattr(text, direction, v)
            box = x.gettextbox(text)[0]
            if direction == "x":
                xs = worldToPixel(box[0], start, end, c1, c2).tolist()
                ys = [height * yRatio * (1 - c) for c in box[1]]
            else:
                xs = [width * xRatio * c for c in box[0]]
                ys = (height * yRatio - worldToPixel(box[1],
                                                     start,
                                                     end,
                                                     c1, c2)).tolist()
            mapped.append([xs, ys])
    return numpy.array(mapped)


def meshToPngCoords(mesh, template, worldCoordinates=[
                 0, 360, -90, 90], png=None, geometry=None):
    """
    Given a mesh object, a vcs template and a graphic methods woorldcoordinate, maps each 'box' to an area on png
    Warning does not handle projections yet.
    Would only work for boxfill and meshfill. May be adapted in the future to isofill as well.
    :Example:

        .. doctest:: utils_meshToPngCoords

            >>> a=vcs.init(bg=True)
            >>> box=vcs.createboxfill()
            >>> array=[range(10) for _ in range(10)]
            >>> a.plot(box,array) # plot something on canvas
            <vcs.displayplot.Dp ...>
            >>> a.png('box.png', width=1536, height=1186) # make a png
            >>> fnm = cdat_info.get_sampledata_path()+"/clt.nc"
            >>> f=cdms2.open(fnm)
            >>> clt=f("clt",time=slice(0,1),squeeze=1)
            >>> mesh = clt.getGrid().getMesh()
            >>> template = vcs.createtemplate()
            >>> areas = meshToPngCoords(mesh, template,
                                     worldCoordinates=[gm.datawc_x1, gm.datawc_x2, gm.datawc_y1, gm.datawc_y2],
                                     png='box.png')

    :param mesh: array of shape (Nelements,2,nVertices) defining the polygon of each cell
    :type : `numpy.ndarray`_

    :param template: template used by vcs when plotting
    :type template: `vcs.template.P`_

    :param worldCoordinates: list of world coordinates for the "data" area of the templte [x1, x2, y1, y2]
    :type worldCoordinates: `list`_

    :param png: png file produced by vcs (used to get dimensions)
    :type png: `str`_

    :param geometry: (width, height) of image on html page
    :type width: `list`_

    :return: A numpy array of pixels mapping the input mesh onto the png passed
    :rtype: `numpy.ndarray`_
    """
    mesh = mesh * 1.  # essentially copy it
    if png is None and geometry is None:
        x = vcs.init()
        x.open()
        ci = x.canvasinfo()
        x.close()
        del(x)
        pwidth = width = ci["width"]
        pheight = height = ci["height"]
    if png is not None:
        pwidth, pheight = getPngDimensions(png)
        if geometry is None:
            width, height = pwidth, pheight
    if geometry is not None:
        width, height = geometry
    if isinstance(template, str):
        template = vcs.gettemplate(template)
    # print("WC:",worldCoordinates)
    # x/y ratio to original png
    xRatio = float(width) / pwidth
    yRatio = float(height) / pheight
    # print("RATIOS",xRatio,yRatio)
    # Determine pixels where data actually sits, on the destination
    x1 = int(width * template.data.x1 * xRatio)
    x2 = int(width * template.data.x2 * xRatio)
    y1 = int(height * template.data.y1 * yRatio)
    y2 = int(height * template.data.y2 * yRatio)
    # html (0,0) is top/left vcs is bottom/left
    mesh[:, 0] = height * yRatio - \
        worldToPixel(mesh[:, 0], worldCoordinates[2],
                     worldCoordinates[3], y1, y2)
    mesh[:, 1] = worldToPixel(
        mesh[:, 1], worldCoordinates[0], worldCoordinates[1], x1, x2)
    # expecting xs first we need to flip
    mesh = mesh[:, ::-1]
    return mesh.astype(int)


def vcsToHtml(data, gm, template, targets=None,
              plot=True, canvas=None, png=None):
    """For a single vcs plot call streamlines the process of plotting and producing the mapping html

    :Example:

        .. doctest:: utils_vcsToHtml

            >>> a=vcs.init(bg=True)
            >>> box=vcs.createboxfill()
            >>> array=[range(10) for _ in range(10)]
            >>> a.plot(box,array) # plot something on canvas
            <vcs.displayplot.Dp ...>
            >>> a.png('box.png', width=1536, height=1186) # make a png
            >>> fnm = cdat_info.get_sampledata_path()+"/clt.nc"
            >>> f=cdms2.open(fnm)
            >>> clt=f("clt",time=slice(0,1),squeeze=1)
            >>> template  = vcs.createtemplate()
            >>> html = vcsToHtml(clt, box, template)

    :param data: a gridded MV2
    :type data: `cdms2.tvariable.TransientVariable`_

    :param gm: a vcs graphic method (boxfill or meshfill)
    :type gm: `vcs.boxfill.Gfb/vcs.meshfill.Gfm`_

    :param template: a vcs template object
    :type template: `vcs.template.P`_

    :param targets: target to link a cell to in html, default to value in data
    :type targets: `list`_

    :param plot: do we also genrate the plot and png?
    :type plot: `bool`_

    :param canvas: vcs canvas on which to plot
    :type canvas: `vcs.Canvas.Canvas`_

    :param png: name of png file
    :type png: `str`_

    :return: html code string
    :rtype: `str`_
    """
    if not isinstance(gm, (vcs.boxfill.Gfb, vcs.meshfill.Gfm)):
        raise BaseException("Only works on boxfill and meshfill for now")
    if plot:
        if gm.datawc_x1 == 1.e20:
            gm.datawc_x1 = data.getLongitude()[:].min()
        if gm.datawc_x2 == 1.e20:
            gm.datawc_x2 = data.getLongitude()[:].max()
        if gm.datawc_y1 == 1.e20:
            gm.datawc_y1 = data.getLatitude()[:].min()
        if gm.datawc_y2 == 1.e20:
            gm.datawc_y2 = data.getLatitude()[:].max()
        if canvas is None:
            canvas = vcs.init()
        canvas.plot(data, gm, template)
        if png is None:
            png = "map_%i.png" % random.randint(0, 99999)
        canvas.png(png)
    g = data.getGrid()
    m = g.getMesh()
    areas = meshToPngCoords(
        m,
        template,
        worldCoordinates=[
            gm.datawc_x1,
            gm.datawc_x2,
            gm.datawc_y1,
            gm.datawc_y2],
        png=png)
    geometry = getPngDimensions(png)
    # Creating a list of target that will be the value of the cell
    tooltips = targets = data.asma().ravel().astype(str).tolist()
    img = mapPng(
        png,
        areas,
        targets,
        tooltips,
        width=geometry[0],
        height=geometry[1])
    return img
