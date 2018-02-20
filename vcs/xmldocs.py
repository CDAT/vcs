plot_keywords_doc = """
    :param xaxis: Axis object to replace the slab -1 dim axis.
         (**keyword parameter**)
    :param yaxis: Axis object to replace the slab -2 dim axis, only if slab has more than 1D.
         (**keyword parameter**)
    :param zaxis: Axis object to replace the slab -3 dim axis, only if slab has more than 2D.
         (**keyword parameter**)
    :param taxis: Axis object to replace the slab -4 dim axis, only if slab has more than 3D.
         (**keyword parameter**)
    :param waxis: Axis object to replace the slab -5 dim axis, only if slab has more than 4D.
         (**keyword parameter**)
    :param xrev: reverse x axis.
         (**keyword parameter**)
    :param yrev: reverse y axis, only if slab has more than 1D.
         (**keyword parameter**)
    :param xarray: Values to use instead of x axis.
         (**keyword parameter**)
    :param yarray: Values to use instead of y axis, only if var has more than 1D.
         (**keyword parameter**)
    :param zarray: Values to use instead of z axis, only if var has more than 2D.
         (**keyword parameter**)
    :param tarray: Values to use instead of t axis, only if var has more than 3D.
         (**keyword parameter**)
    :param warray: Values to use instead of w axis, only if var has more than 4D.
         (**keyword parameter**)
    :param continents: continents type number.
         (**keyword parameter**)
    :param name: replaces variable name on plot.
         (**keyword parameter**)
    :param time: replaces time name on plot.
         (**keyword parameter**)
    :param units: replaces units value on plot.
         (**keyword parameter**)
    :param ymd: replaces year/month/day on plot.
         (**keyword parameter**)
    :param hms: replaces hh/mm/ss on plot.
         (**keyword parameter**)
    :param file_comment: replaces file_comment on plot.
         (**keyword parameter**)
    :param xbounds: Values to use instead of x axis bounds values.
         (**keyword parameter**)
    :param ybounds: Values to use instead of y axis bounds values (if exist).
         (**keyword parameter**)
    :param xname: replace xaxis name on plot.
         (**keyword parameter**)
    :param yname: replace yaxis name on plot (if exists).
         (**keyword parameter**)
    :param zname: replace zaxis name on plot (if exists).
         (**keyword parameter**)
    :param tname: replace taxis name on plot (if exists).
         (**keyword parameter**)
    :param wname: replace waxis name on plot (if exists).
         (**keyword parameter**)
    :param xunits: replace xaxis units on plot.
         (**keyword parameter**)
    :param yunits: replace yaxis units on plot (if exists).
         (**keyword parameter**)
    :param zunits: replace zaxis units on plot (if exists).
         (**keyword parameter**)
    :param tunits: replace taxis units on plot (if exists).
         (**keyword parameter**)
    :param wunits: replace waxis units on plot (if exists).
         (**keyword parameter**)
    :param xweights: replace xaxis weights used for computing mean.
         (**keyword parameter**)
    :param yweights: replace xaxis weights used for computing mean.
         (**keyword parameter**)
    :param comment1: replaces comment1 on plot.
         (**keyword parameter**)
    :param comment2: replaces comment2 on plot.
         (**keyword parameter**)
    :param comment3: replaces comment3 on plot.
         (**keyword parameter**)
    :param comment4: replaces comment4 on plot.
         (**keyword parameter**)
    :param long_name: replaces long_name on plot.
         (**keyword parameter**)
    :param grid: replaces array grid (if exists).
         (**keyword parameter**)
    :param bg: plots in background mode.
         (**keyword parameter**)
    :param ratio: sets the y/x ratio ,if passed as a string with 't' at the end, will aslo moves the ticks.
         (**keyword parameter**)
    :type xaxis: cdms2.axis.TransientAxis
    :type yaxis: cdms2.axis.TransientAxis
    :type zaxis: cdms2.axis.TransientAxis
    :type taxis: cdms2.axis.TransientAxis
    :type waxis: cdms2.axis.TransientAxis
    :type xrev: bool
    :type yrev: bool
    :type xarray: array
    :type yarray: array
    :type zarray: array
    :type tarray: array
    :type warray: array
    :type continents: int
    :type name: str
    :type time: A cdtime object
    :type units: str
    :type ymd: str
    :type hms: str
    :type file_comment: str
    :type xbounds: array
    :type ybounds: array
    :type xname: str
    :type yname: str
    :type zname: str
    :type tname: str
    :type wname: str
    :type xunits: str
    :type yunits: str
    :type zunits: str
    :type tunits: str
    :type wunits: str
    :type xweights: array
    :type yweights: array
    :type comment1: str
    :type comment2: str
    :type comment3: str
    :type comment4: str
    :type long_name: str
    :type grid: cdms2.grid.TransientRectGrid
    :type bg: bool/int
    :type ratio: int/str
"""  # noqa

data_time = """
            .. py:attribute:: datawc_timeunits (str)

                (Ex: 'days since 2000') units to use when displaying time dimension auto tick

            .. py:attribute:: datawc_calendar (int)

                (Ex: 135441) calendar to use when displaying time dimension auto tick, default is proleptic gregorian calendar

"""  # noqa
graphics_method_core_notime = """
            .. py:attribute:: xmtics1 (str/{float:str})

                (Ex: '') dictionary with location of intermediate tics as keys for 1st side of y axis

            .. py:attribute:: xmtics2 (str/{float:str})

                (Ex: '') dictionary with location of intermediate tics as keys for 2nd side of y axis

            .. py:attribute:: ymtics1 (str/{float:str})

                (Ex: '') dictionary with location of intermediate tics as keys for 1st side of y axis

            .. py:attribute:: ymtics2 (str/{float:str})

                (Ex: '') dictionary with location of intermediate tics as keys for 2nd side of y axis

            .. py:attribute:: xticlabels1 (str/{float:str})

                (Ex: '*') values for labels on 1st side of x axis

            .. py:attribute:: xticlabels2 (str/{float:str})

                (Ex: '*') values for labels on 2nd side of x axis

            .. py:attribute:: yticlabels1 (str/{float:str})

                (Ex: '*') values for labels on 1st side of y axis

            .. py:attribute:: yticlabels2 (str/{float:str})

                (Ex: '*') values for labels on 2nd side of y axis

            .. py:attribute:: projection (str/vcs.projection.Proj)

                (Ex: 'default') projection to use, name or object

            .. py:attribute:: datawc_x1 (float)

                (Ex: 1.E20) first value of xaxis on plot

            .. py:attribute:: datawc_x2 (float)

                (Ex: 1.E20) second value of xaxis on plot

            .. py:attribute:: datawc_y1 (float)

                (Ex: 1.E20) first value of yaxis on plot

            .. py:attribute:: datawc_y2 (float)

                (Ex: 1.E20) second value of yaxis on plot
            """  # noqa
graphics_method_core = """
    %s
    %s
    """ % (graphics_method_core_notime, data_time)
axisconvert = """
    :param {axis}axisconvert: (Ex: 'linear') converting {axis}axis linear/log/log10/ln/exp/area_wt
    :type {axis}axisconvert: str\n"""
xaxisconvert = axisconvert.format(axis="x")
yaxisconvert = axisconvert.format(axis="y")
axesconvert = xaxisconvert + yaxisconvert
# for these docs, use string.format() when you use them
#    Keys:
#       {name}: String name to complete the call to vcs.(get|create)$OBJ_TYPE()
#       {parent}: String argument for calls to vcs.(get|create)$OBJ_TYPE() that require specification of an obj to
#           inherit from. Mainly used for get1d, but possible uses for text objects also exist (maybe others too).
#           If providing a parent name, use either double quotes in a string literal, or a string literal in double
#           quotes (i.e. '"$PARENT"' or "'$PARENT'"). Else, use an empty string.
#       {data}: String used for plugging in plotting information. Plug in whatever data is set up in the docstring
#           in a way that VCS will correctly plot the object.
#       {x_y}: Literally will be the string "x" or "y".
#       {axis}: "lat" or "lon", corresponding to the value you put in for {x_y}

colorsdoc = """
    Sets the color_1 and color_2 properties of the object.

    .. note::

        color_1 and color_2 control which parts of the colormap to use for the
        plot. It defaults to the full range of the colormap (0-255), but if you
        use fewer colors, it will break up your data into precisely that many
        discrete colors.

    :Example:

        .. doctest:: %(name)s_colors

            >>> a=vcs.init()
            >>> array=[range(10) for _ in range(10)]
            >>> ex=a.create%(name)s()
            >>> ex.colors(0, 64) # use colorcells 0-64 of colormap
            >>> a.plot(ex, %(data)s)
            <vcs.displayplot.Dp object at 0x...>

    :param color1: Sets the :py:attr:`color_1` value on the object.
    :type color1: int

    :param color2: Sets the :py:attr:`color_2` value on the object.
    :type color2: int
    """

extsdoc = """
    Sets the ext_1 and ext_2 values on the object.

    :Example:

        .. doctest {name}_exts

            >>> a=vcs.init()
            >>> array=[range(10) for _ in range(10)]
            >>> ex=a.create{name}()
            >>> ex.exts(True, True) # arrows on both ends
            >>> a.plot(ex, {data})
            <vcs.displayplot.Dp object at 0x...>

    :param ext1: Sets the :py:attr:`ext_1` value on the object.
        'y' sets it to True, 'n' sets it to False.
        True or False can be used in lieu of 'y' and 'n'.
    :type ext1: str or bool

    :param ext2: Sets the :py:attr:`ext_2` value on the object.
        'y' sets it to True, 'n' sets it to False.
        True or False can be used in lieu of 'y' and 'n'.
    :type ext2: str or bool
    """
mticsdoc = """
    Sets the {x_y}mtics1 and {x_y}mtics2 values on the object.

    .. note::

        The mtics attributes are not inherently plotted by the default template.
        The example below shows how to apply a custom template and enable it to
        plot mtics. To plot a the {name} after setting the mtics and template,
        refer to :py:func:`vcs.Canvas.plot` or :py:func:`vcs.Canvas.{name}`.

    :Example:

        .. doctest:: {name}_{x_y}mtics

            >>> a=vcs.init()
            >>> ex=vcs.create{name}()
            >>> ex.{x_y}mtics("{axis}5") # minitick every 5 degrees
            >>> tmp=vcs.createtemplate() # custom template to plot minitics
            >>> tmp.{x_y}mintic1.priority = 1 # plotting shows {x_y}mtics

    :param {x_y}mt1: Value for :py:attr:`{x_y}mtics1`.
        Must be a str, or a dictionary object with float:str mappings.
    :type {x_y}mt1: dict or str

    :param {x_y}mt2: Value for :py:attr:`{x_y}mtics2`.
        Must be a str, or a dictionary object with float:str mappings.
    :type {x_y}mt2: dict or str
    """
xmticsdoc = mticsdoc.format(x_y="x", axis="lon", name="{name}")
ymticsdoc = mticsdoc.format(x_y="x", axis="lat", name="{name}")
datawcdoc = """
    Sets the data world coordinates for object

    :Example:

        .. doctest:: datawc_{name}

            >>> a=vcs.init()
            >>> ex=a.create{name}('{name}_dwc')
            >>> ex.datawc(0.0, 0.1, 1.0, 1.1) # sets datawc y1, y2, x1, x2
            >>> ex.datawc_y1, ex.datawc_y2, ex.datawc_x1, ex.datawc_x2
            (0.0, 0.1, 1.0, 1.1)

    :param dsp1: Sets the :py:attr:`datawc_y1` property of the object.
    :type dsp1: float

    :param dsp2: Sets the :py:attr:`datawc_y2` property of the object.
    :type dsp2: float

    :param dsp3: Sets the :py:attr:`datawc_x1` property of the object.
    :type dsp3: float

    :param dsp4: Sets the :py:attr:`datawc_x2` property of the object.
    :type dsp4: float
    """
xyscaledoc = """
    Sets xaxisconvert and yaxisconvert values for the object.

    :Example:

        .. doctest:: xyscale_{name}

            >>> a=vcs.init()
            >>> ex=a.create{name}('{name}_xys') # make a {name}
            >>> ex.xyscale(xat='linear', yat='linear')

    :param xat: Set value for x axis conversion.
    :type xat: str

    :param yat: Set value for y axis conversion.
    :type yat: str
    """
listdoc = """Lists the current values of object attributes

    :Example:

        .. doctest:: listdoc

            >>> a=vcs.init()
            >>> obj=a.get{name}({parent}) # default
            >>> obj.list() # print {name} attributes
            ---------- ... ----------
            ...
    """
# due to the labels being plugged in below, we have to use a dictionary to format this docstring.
# .format() messes up because it tries to interpret the labels dictionary as a keyword.
ticlabelsdoc = """
    Sets the %(x_y)sticlabels1 and %(x_y)sticlabels2 values on the object

    :Example:

        .. doctest:: %(name)s_%(x_y)sticlabels

            >>> a = vcs.init()
            >>> import cdms2 # Need cdms2 to create a slab
            >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # open data file
            >>> ex = a.create%(name)s()
            >>> ex.%(x_y)sticlabels(%(labels)s)
            >>> a.plot(ex, %(data)s) # plot shows labels
            <vcs.displayplot.Dp object at 0x...>

    :param %(x_y)stl1: Sets the object's value for :py:attr:`%(x_y)sticlabels1`.
        Must be  a str, or a dictionary object with float:str mappings.
    :type %(x_y)stl1: dict or str

    :param %(x_y)stl2: Sets the object's value for :py:attr:`%(x_y)sticlabels2`.
        Must be a str, or a dictionary object with float:str mappings.
    :type %(x_y)stl2: dict or str
    """
xticlabelsdoc = ticlabelsdoc % {"x_y": "x",
                                "labels": '{0: "Prime Meridian", -121.7680: "Livermore", 37.6173: "Moscow"}',
                                "name": "%(name)s", "data": "%(data)s"}
yticlabelsdoc = ticlabelsdoc % {"x_y": "y", "labels": '{0: "Eq.", 37.6819: "L", 55.7558: "M"}', "name": "%(name)s",
                                "data": "%(data)s"}


def populate_docstrings(type_dict, target_dict, docstring, method):
    """
    A function to populate docstrings from a dictionary.
    Structure of the function is pretty specific to type_dicts shaped like xmldoc.obj_details.

    Indentation of the docstring snippets is screwy because they need to maintain alignment
    with the original docstring entries for Sphinx to pick them up correctly.

    :param type_dict: The dictionary to parse for values used to fill in the docstring
    :param target_dict: An empty dictionary to be populated with docstrings
    :param docstring: The template docstring
    :param method: The method that the docstring is for

    :return: Has no return, but at the end target_dict should be full of formatted docstrings
    """
    d = {}
    for obj_type in list(type_dict.keys()):
        for obj_name in list(type_dict[obj_type].keys()):
            # default values. Change as necessary.
            example1 = ''
            example2 = ''
            d['type'] = obj_type
            d['name'] = d['sp_name'] = obj_name
            d['parent'] = type_dict[obj_type][obj_name]['parent']
            d['parent2'] = type_dict[obj_type][obj_name]['parent2']
            d['sp_parent'] = ''
            d['tc'] = ''
            d['rtype'] = type_dict[obj_type][obj_name]['rtype']
            if type_dict[obj_type][obj_name]['title']:
                d['cap'] = d['name'].title()
            else:
                d['cap'] = d['name']
            if obj_name in ['3d_vector', '3d_scalar', '3d_dual_scalar']:
                d['sp_name'] = 'dv3d'
            elif obj_name in ['1d', 'scatter', 'textcombined', 'xyvsy']:
                if obj_name == 'textcombined':
                    d['tc'] = """>>> try: # try to create a new textcombined, in case none exist
            ...     tc = vcs.createtextcombined('EX_tt', 'qa', 'EX_tto', '7left')
            ... except:
            ...     pass
            """
                    d['sp_parent'] = "'EX_tt', 'EX_tto'"
                elif obj_name == '1d':
                    d['sp_parent'] = "'default'"
                else:
                    sp_parent = 'default_'+obj_name+'_'
                    d['sp_parent'] = "'%s'" % sp_parent
                    d['parent'] = d['sp_parent']
        # From here to the end of the inner for loop is intended to be a section for specific use-cases for the template
        #   string keywords. This section aims to take the 'method' parameter and use it to insert proper examples for
        #   that method.

        # section for manageElements 'get' methods
            if method == 'get':
                example1 = """>>> ex=vcs.get%(name)s(%(sp_parent)s)  # '%(parent)s' %(name)s"""
                if d['tc'] is not '':
                    example1 = d['tc'] + example1
                # set up d['plot'] and d['plot2']
                plot = ''
                plot2 = ''
                numslabs = type_dict[obj_type][obj_name]['slabs']
                d['slabs'] = ''
                d['args'] = ''
                if numslabs > 0:
                    if obj_name is "taylordiagram":
                        d['slabs'] = """
            >>> slab1 = [[0, 1, 2, 3, 4], [0.1, 0.2, 0.3, 0.4, 0.5]] # data"""
                    else:
                        d['slabs'] = """
            >>> import cdms2 # Need cdms2 to create a slab
            >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # get data with cdms2
            >>> slab1 = f('u') # take a slab from the data"""
                    d['args'] = ", slab1"
                    if numslabs == 2:
                        slab2 = """
            >>> slab2 = f('v') # need 2 slabs, so get another"""
                        d['slabs'] += slab2
                        d['args'] += ", slab2"
            # for vcs objects that have a self-named plotting function, i.e. fillarea()
                if type_dict[obj_type][obj_name]['callable']:
                    plot = """
            >>> a.%(name)s(ex%(args)s) # plot %(name)s
            <vcs.displayplot.Dp ...>"""
                    # set up plot2
                    plot2 = """
            >>> a.%(name)s(ex2%(args)s) # plot %(name)s
            <vcs.displayplot.Dp ...>""" % d
            # for objects like template, where a call to plot() needs to be made
            # objects in the list cannot be plotted without a graphics method
                elif obj_name not in ['textorientation', 'texttable', 'colormap', 'projection', 'template', 'display']:
                    plot = """
            >>> a.plot(ex%(args)s) # plot %(name)s
            <vcs.displayplot.Dp ...>
            """
                    plot2 = """
            >>> a.plot(ex2%(args)s) # plot %(name)s
            <vcs.displayplot.Dp ...>"""
                if obj_name.find('3d') >= 0:
                    if obj_name is "3d_vector":
                        plot = ""
#            >>> a.plot(ex%(args)s) # plot %(name)s
#            Sample rate: 6
#            Sample rate: 6
#            initCamera: Camera => (...)
#            <vcs.displayplot.Dp ...>
#            """
                    else:
                        plot = ""
#            >>> a.plot(ex%(args)s) # plot %(name)s
#            initCamera: Camera => (...)
#            <vcs.displayplot.Dp ...>
#            """

                if d['slabs'] is not '':
                    plot = d['slabs'] + plot
                example1 += plot
                d['example'] = example1 % d
                if d['parent2']:
                    example2 = """
            >>> ex2=vcs.get%(name)s('%(parent2)s')  # %(name)s #2"""
                    example2 += plot2
                    d['example'] += example2 % d
        # section for manageElements 'create' methods
            elif method == 'create':
                # if obj_name is tc, d['tc'] should be populated by code that creates a tc at this point
                if obj_name == "textcombined":
                    example1 = d['tc'] + """>>> vcs.listelements('%(name)s') # includes new object
            [...'EX_tt:::EX_tto'...]"""
                else:
                    example1 = """>>> ex=vcs.create%(name)s('%(name)s_ex1')
            >>> vcs.listelements('%(name)s') # includes new object
            [...'%(name)s_ex1'...]
            """
                d['example'] = example1 % d
                if d['parent2']:
                    example2 = """>>> ex2=vcs.create%(name)s('%(name)s_ex2','%(parent2)s')
            >>> vcs.listelements('%(name)s') # includes new object
            [...'%(name)s_ex2'...]
            """
                    d['example'] += example2 % d
            elif method == 'script':
                d['example'] = """>>> ex=a.get%(call)s(%(sp_parent)s)
            >>> ex.script('filename.py') # append to 'filename.py'
            >>> ex.script('filename','w') # make/overwrite 'filename.json'"""
                if obj_name == "textcombined":
                    d['call'] = obj_name
                    d['name'] = 'text table and text orientation'
                    d['example'] = d['tc'] + d['example']
                else:
                    d['call'] = d['name']
                d['example'] %= d
            elif method == 'is':
                example = """>>> a.show('%(name)s') # available %(name)ss
            *******************%(cap)s Names List**********************
            ...
            *******************End %(cap)s Names List**********************
            >>> ex = a.get%(name)s(%(sp_parent)s)
            >>> vcs.queries.is%(name)s(ex)
            1
            """
                if d['tc'] is not '':
                    example = d['tc'] + example
                d['example'] = example % d
            target_dict[obj_name] = docstring % d
            d.clear()


# obj_details contains VCS object details used to build Example doctests and fill in docstrings
#   Keys:
#       "graphics method" / "secondary method" : These top-level keys specify the type of objects described within
#       "callable"(bool): specifies whether the object has a self-named plotting function, i.e. fillarea()
#       "parent"(str): specifies the name of the object to be used in inheritance for a first example.
#           Usually 'default', but it can change based on situation (textcombined, 1d, xyvsy, etc.).
#       "parent2"(str): specifies a name for object inheritance in a second example. If there is no reliable second
#           object, (i.e. vcs only has a 'default' object pre-made), use an empty string.
#       "rtype"(VCS object type): the type of the object to be returned. This is only used for manageElements 'get' and
#           'create' docstrings.
#       "slabs"(int): used to specify how many slabs are needed to plot an object of the given type. 0 for none.
#       "title"(bool): specifies whether to TitleCase the object's name for the output on vcs.show()
obj_details = {
    "graphics method": {
        "taylordiagram": {
            "callable": True,
            "parent": "default",
            "parent2": "",
            "rtype": "vcs.taylor.Gtd",
            "slabs": 1,
            "title": True,
        },
        "3d_scalar": {
            "callable": False,
            "parent": "default",
            "parent2": "",
            "rtype": "vcs.dv3d.Gf3Dscalar",
            "slabs": 1,
            "title": False,
        },
        "3d_dual_scalar": {
            "callable": False,
            "parent": "default",
            "parent2": "",
            "rtype": "vcs.dv3d.Gf3DDualScalar",
            "slabs": 2,
            "title": False,
        },
        "3d_vector": {
            "callable": False,
            "parent": "default",
            "parent2": "",
            "rtype": "vcs.dv3d.Gf3Dvector",
            "slabs": 2,
            "title": False,
        },
        "vector": {
            "callable": True,
            "parent": "default",
            "parent2": "",
            "rtype": "vcs.vector.Gv",
            "slabs": 2,
            "title": True,

        },
        "streamline": {
            "callable": True,
            "parent": "default",
            "parent2": "",
            "rtype": "vcs.streamline.Gs",
            "slabs": 2,
            "title": True,

        },
        "scatter": {
            "callable": True,
            "parent": "default_scatter_",
            "parent2": "",
            "rtype": "vcs.unified1D.G1d",
            "slabs": 2,
            "title": True,
        },
        "yxvsx": {
            "callable": True,
            "parent": "default_yxvsx_",
            "parent2": "",
            "rtype": "vcs.unified1D.G1d",
            "slabs": 1,
            "title": True,
        },
        "xyvsy": {
            "callable": True,
            "parent": "default_xyvsy_",
            "parent2": "",
            "rtype": "vcs.unified1D.G1d",
            "slabs": 1,
            "title": True,
        },
        "xvsy": {
            "callable": True,
            "parent": "default_xvsy_",
            "parent2": "",
            "rtype": "vcs.unified1D.G1d",
            "slabs": 2,
            "title": True,
        },
        "1d": {
            "callable": False,
            "parent": "default",
            "parent2": "",
            "rtype": "vcs.unified1D.G1d",
            "slabs": 1,
            "title": False,
        },
        "boxfill": {
            "callable": True,
            "parent": "default",
            "parent2": "polar",
            "rtype": "vcs.boxfill.Gfb",
            "slabs": 1,
            "title": True,
        },
        "isofill": {
            "callable": True,
            "parent": "default",
            "parent2": "polar",
            "rtype": "vcs.isofill.Gfi",
            "slabs": 1,
            "title": True,
        },
        "isoline": {
            "callable": True,
            "parent": "default",
            "parent2": "polar",
            "rtype": "vcs.isoline.Gi",
            "slabs": 1,
            "title": True,
        },
        "template": {
            "callable": False,
            "parent": "default",
            "parent2": "polar",
            "rtype": "vcs.template.P",
            "slabs": 1,
            "title": True,
        },
        "projection": {
            "callable": False,
            "parent": "default",
            "parent2": "orthographic",
            "rtype": "vcs.projection.Proj",
            "slabs": 1,
            "title": True,
        },
        "meshfill": {
            "callable": True,
            "parent": "default",
            "parent2": "a_polar_meshfill",
            "rtype": "vcs.meshfill.Gfm",
            "slabs": 1,
            "title": True,
        },
    },
    "secondary method": {
        "fillarea": {
            "callable": True,
            "parent": "default",
            "parent2": "",
            "rtype": "vcs.fillarea.Tf",
            "slabs": 0,
            "title": True,
        },
        "line": {
            "callable": True,
            "parent": "default",
            "parent2": "red",
            "rtype": "vcs.line.Tl",
            "slabs": 0,
            "title": True,
        },
        "marker": {
            "callable": True,
            "parent": "default",
            "parent2": "red",
            "rtype": "vcs.marker.Tm",
            "slabs": 0,
            "title": True,
        },
        "colormap": {
            "callable": False,
            "parent": "default",
            "parent2": "rainbow",
            "rtype": "vcs.colormap.Cp",
            "slabs": 0,
            "title": True,
        },
        "textcombined": {
            "callable": True,
            "parent": "EX_tt:::EX_tto",
            "parent2": "",
            "rtype": "vcs.textcombined.Tc",
            "slabs": 0,
            "title": True,
        },
        "texttable": {
            "callable": False,
            "parent": "default",
            "parent2": "bigger",
            "rtype": "vcs.texttable.Tt",
            "slabs": 0,
            "title": True,
        },
        "textorientation": {
            "callable": False,
            "parent": "default",
            "parent2": "bigger",
            "rtype": "vcs.textorientation.To",
            "slabs": 0,
            "title": True,
        },
    }
}
# docstrings is a dictionary to store all docstring dictionaries and their associated docstrings
# this will be used to populate all the docstrings in the same for loop (should better utilize locality (maybe))
docstrings = {}

# keywords in these docstring tmeplates relate somewhat to keys described in obj_details above.
# Population of these strings is taken care of in the populate_docstrings function.

# For the sanity of future developers, I'll document the meaning of the keys I used and the convention I followed:
# Keys:
#   'name' : the name of the VCS object being referred to (boxfill, 1d, textorientation, etc.). This is used to talk
#       about the object and to call the object's get/create functions in most cases.
#   'type' : the type of object we are dealing with. Mostly just 'secondary method' or 'graphics method'.
#   'sp_parent' : used if the object doesn't have a sensible default for its *get* function. Examples of objects which
#       need this are the 1d family of objects and textcombined objects. If the object does have a sensible default,
#       (e.g. getboxfill()) this key should be an empty string. When providing a string to 'sp_parent', it should be
#       of format "'blah'" or '"blah"', and if multiple arguments are needed, they should be provided ('"blah", "blah"')
#   'tc'    : no textcombined objects exist by default in VCS, so this key is for an entry that will create one when
#       it is needed for an example. All other times, it will be an empty string.
#   'example'   : this should be filled in with code examples in doctest format. Maintain indentation with the origin
#       docstring. Most of the time, this means 3 indents (12 spaces) from the left side is where all your doctest
#       lines should start. Look above, in populate_docstrings() to see what I'm tlaking about.
scriptdoc = """Saves out a copy of the %(name)s %(type)s,
    in JSON or Python format to a designated file.

        .. note::

            If the the filename has a '.py' at the end, it will produce a
            Python script. If no extension is given, then by default a
            .json file containing a JSON serialization of the object's
            data will be produced.

        .. warning::

            VCS Scripts Deprecated.
            SCR script files are no longer generated by this function.

    :Example:

        .. doctest:: script_examples

            >>> a=vcs.init()
            %(example)s

    :param script_filename: Output name of the script file.
        If no extension is specified, a .json object is created.
    :type script_filename: str

    :param mode: Either 'w' for replace, or 'a' for append.
        Defaults to 'a', if not specified.
    :type mode: str
    """


queries_is_doc = """
    Check to see if this object is a VCS %(name)s %(type)s.

    :Example:

        .. doctest:: queries_is

            >>> a=vcs.init()
            %(example)s

    :param obj: A VCS object
    :type obj: VCS Object

    :returns: An integer indicating whether the object is a
        %(name)s %(type)s (1), or not (0).
    :rtype: int
    """

get_methods_doc = """VCS contains a list of %(type)ss. This function
    will create a %(sp_name)s object from an existing
    VCS %(sp_name)s %(type)s. If no %(sp_name)s name is given,
    then %(parent)s %(sp_name)s will be used.

    .. note::

        VCS does not allow the modification of 'default' attribute sets.
        However, a 'default' attribute set that has been copied under a
        different name can be modified.
        (See the :py:func:`vcs.manageElements.create%(name)s` function.)

    :Example:

        .. doctest:: manageElements_get

            >>> a=vcs.init()
            >>> vcs.listelements('%(name)s') # list all %(name)ss
            [...]
            %(example)s
    """

create_methods_doc = """
    Create a new %(sp_name)s %(type)s given the the name and
    the existing %(sp_name)s %(type)s to copy attributes from.
    If no existing %(sp_name)s %(type)s is given,
    the default %(sp_name)s %(type)s will be used as the
    graphics method from which attributes will be copied.

    .. note::

        If the name provided already exists, then an error will be returned.
        %(type)s names must be unique.

    :Example:

        .. doctest:: manageElements_create

            >>> vcs.listelements('%(name)s') # list %(name)ss
            [...]
            %(example)s
            """

scriptdocs = {}
docstrings['script'] = [scriptdocs, scriptdoc]
is_docs = {}
docstrings['is'] = [is_docs, queries_is_doc]
get_docs = {}
docstrings['get'] = [get_docs, get_methods_doc]
create_docs = {}
docstrings['create'] = [create_docs, create_methods_doc]

# populate all the docstrings
for method in list(docstrings.keys()):
    populate_docstrings(obj_details, docstrings[method][0], docstrings[method][1], method)

#############################################################################
#                                                                           #
# Attributes section                                                        #
#                                                                           #
#############################################################################

exts_attrs = """
            .. py:attribute:: ext_1 (str)

                Draws an extension arrow on right side (values less than first range value)

            .. py:attribute:: ext_2 (str)

                Draws an extension arrow on left side (values greater than last range value)
    """

fillarea_colors_attr = """
            .. py:attribute:: fillareacolors ([int,...])

                Colors to use for each level
    """

fillarea_attrs = """
            .. py:attribute:: fillareastyle (str)

                Style to use for levels filling: solid/pattern/hatch

            .. py:attribute:: fillareaindices ([int,...])

                List of patterns to use when filling a level and using pattern/hatch
    """

legend_attr = """
            .. py:attribute:: legend (None/{float:str})

                Replaces the legend values in the dictionary keys with their associated string
    """

level_attrs = """
            .. py:attribute:: level_1 (float)

                Sets the value of the legend's first level

            .. py:attribute:: level_2 (float)

                Sets the value of the legend's end level
    """

levels_attr = """
            .. py:attribute:: levels ([float,...]/[[float,float],...])

                Sets the levels range to use, can be either a list of contiguous levels, or list of tuples
                indicating first and last value of the range.
    """

missing_attr = """
            .. py:attribute:: missing (int)

                Color to use for missing value or values not in defined ranges
    """

# 3d plot attributes
toggle_vs = """
            .. py:attribute:: Toggle{v_s}Plot (vcs.on or vcs.off)

                Toggles the visibility of the :ref:`dv3d-{v_s}` ({i_e}) plot constituent.

                **Interact Mode:** Toggle visibility with button click.
"""
toggle_volume = toggle_vs.format(v_s="Volume", i_e="volume render")
toggle_surface = toggle_vs.format(v_s="Surface", i_e="isosurface")
axisslider = """
            .. py:attribute:: {axis}Slider (float, vcs.on or vcs.off)

                Sets the position and visibility of the {axis} :term:`Slice` plane.
                The position is in {coord} coordinates.

                **Interact Mode:** Adjust position with the slider.
"""
xslider = axisslider.format(axis="X", coord="longitude")
yslider = axisslider.format(axis="Y", coord="latitude")
zslider = axisslider.format(axis="Z", coord="relative (0.0 = bottom, > 1.0 = top)")
verticalscaling = """
            .. py:attribute:: VerticalScaling (float)

                Scales the vertical dimension of the plot.

                Accepts values from ~ 0.1 -- 10.0

                **Interact Mode:** Adjust position with the slider.
"""
scalecolormap = """
            .. py:attribute:: ScaleColormap (floats: [max,min])

                Sets the value range of the current colormap.
                Initialized to the max (full) range value of the data.

                **Interact Mode:** Adjust colormap range (min, max) with the pair of sliders.
"""
scaletransferfunction = """
            .. py:attribute:: ScaleTransferFunction (floats: [max,min])

                Sets the value range of the :term:`Volume` plot constituent, which maps this range of variable
                values to opacity. Initialized to the max (full) range value of the data.

                **Interact Mode:** Adjust TF range (min, max) with the pair of sliders.
"""
toggleclipping = """
            .. py:attribute:: ToggleClipping (Up to six floats: [ xmin, xmax, ymin, ymax, zmin, zmax ])

                Sets the clip bounds for the :term:`Volume` plot constituent.

                **Interact Mode:** Drag the spheres on the adjustable frame.
"""
isosurfacevalue = """
            .. py:attribute:: IsosurfaceValue (float between the variable max and min values)

                Sets the variable value that defines the isosurface (:term:`Surface`).

                **Interact Mode:** Adjust the isosurface value using the slider.
"""
scaleopacity = """
            .. py:attribute:: ScaleOpacity (floats: [ max, min ])

                Sets the opacity range of the :term:`Volume` plot constituent,
                which maps the selected range of variable values to this opacity range.
                Initialized to [1,1]

                **Interact Mode:** Adjust opacity range (min, max) with the pair of sliders.
"""
basemapopacity = """
            .. py:attribute:: BasemapOpacity (float between 0.0 and 1.0.)

                Sets the opacity of the underlying earth map.

                **Interact Mode:** Adjust the opacity with the slider.
"""
camera = """
            .. py:attribute:: Camera (dict with three keys: 'Position', 'ViewUp', and 'FocalPoint')

                Sets the position and orientation of the camera.

                The values of Position and FocalPoint are positions in model coordinates, and ViewUp is a unit vector.

                **Interact Mode:** Left-click in window and drag to rotate. Right-click and drag to zoom/pan.
                Shift-Left-click and drag to translate.
"""
meshfill_doc = """
    %s
    %s
    %s
    %s
    %s
    %s
    """ % (levels_attr, fillarea_colors_attr, fillarea_attrs, legend_attr, exts_attrs, missing_attr)
isofill_doc = meshfill_doc
fillareadoc = """
        .. py:attribute:: fillareacolor (int)

            color to use for outfilling

        .. py:attribute:: fillareastyle (str)

            style to use for levels filling: solid/pattenr/hatch

        .. py:attribute:: fillareaindex (int)

            pattern to use when filling a level and using pattern/hatch
    """  # noqa
linesdoc = """
        .. py:attribute:: line ([str,...]/[vcs.line.Tl,...]/[int,...])

            line type to use for each isoline, can also pass a line object or line object name

        .. py:attribute:: linecolors ([int,...])

            colors to use for each isoline

        .. py:attribute:: linewidths ([float,...])

            list of width for each isoline
    """  # noqa
linedoc = """
        .. py:attribute:: line ([str,...]/[vcs.line.Tl,...]/[int,...])

            line type to use for each isoline, can also pass a line object or line object name

        .. py:attribute:: linecolor (int)

            color to use for each isoline

        .. py:attribute:: linewidth (float)

            width for each isoline
    """  # noqa
textsdoc = """
        .. py:attribute:: text (None/[vcs.textcombined.Tc,...])

            text objects or text objects names to use for each countour label

        .. py:attribute:: textcolors (None/[int,...])

            colors to use for each countour label
    """  # noqa
markerdoc = """
        .. py:attribute:: marker (None/int/str/vcs.marker.Tm)

            markers type to use

        .. py:attribute:: markercolor (None/int)

            color to use for markers

        .. py:attribute:: markersize (None/int)

            size of markers
    """
color_one_two_doc = """
        .. py:attribute:: color_1 (float)

            Used in conjunction with boxfill_type linear/log10,
            sets the first value of the legend's color range.

        .. py:attribute:: color_2 (float)

            Used in conjunction with boxfill_type linear/log10.
            Sets the last value of the legend's color range.
    """
#############################################################################
#                                                                           #
# Graphics Method input section.                                            #
#                                                                           #
#############################################################################

create_GM_input = """
    :param new_GM_name: (Ex: 'my_awesome_gm') name of the new graphics method
        object. If no name is given, then one will be created for use.
    :type new_GM_name: str

    :param source_GM_name: (Ex: 'default') copy the contents of the source
        object to the newly created one. If no name is given, the 'default'
        graphics method contents are copied over to the new object.
    :type source_GM_name: str
    """  # noqa

get_GM_input = """
    :param GM_name: (Ex: 'default') retrieve the graphics method object of the
        given name. If no name is given, retrieve the 'default' graphics method.
    :type GM_name: str
    """  # noqa

plot_1D_input = """
    :param slab: (Ex: [1, 2]) Data at least 1D, last dimension will be plotted
    :type slab: array
    """  # noqa

plot_2D_input = """
    :param slab: (Ex: [[0, 1]]) Data at least 2D, last 2 dimensions will be plotted
    :type slab: array
    """  # noqa

plot_2_1D_input = """
    :param slab_or_primary_object: Data at least 1D, last dimension(s) will be
        plotted, or secondary vcs object
    :type slab_or_primary_object: array
    """  # noqa
plot_2_1D_options = """
    :param slab2: Data at least 1D, last dimension(s) will be plotted
    :param template: ('default') vcs template to use
    :param gm: (Ex: 'default') graphic method to use
    :type slab2: array
    :type template: str/vcs.template.P
    :type gm: VCS graphics method object
    """  # noqa
#############################################################################
#                                                                           #
# Graphics Method output section.                                           #
#                                                                           #
#############################################################################
plot_output = """
    :return: A VCS displayplot object.
    :rtype: vcs.displayplot.Dp
    """
boxfill_output = """
       boxfill :: (Ex: 0) no default
    """
isofill_output = """
       isofill :: (Ex: 0) no default
    """
isoline_output = """
       isoline :: (Ex: 0) no default
    """
yxvsx_output = """
       yxvsx :: (Ex: 0) no default
    """
xyvsy_output = """
       xyvsy :: (Ex: 0) no default
    """
xvsy_output = """
       xvsy :: (Ex: 0) no default
    """
scatter_output = """
       scatter :: (Ex: 0) no default
    """
outfill_output = """
       outfill :: (Ex: 0) no default
    """
outline_output = """
       outline :: (Ex: 0) no default
    """
#############################################################################
#                                                                           #
# Parameters section                                                        #
#                                                                           #
#############################################################################
name = """
        :param name: Name of the object to be created.
        :type name: `str`_
        """
priority = """
        :param priority: The layer on which the object will be drawn.
        :type priority: `int`_
        """
color = """
        :param color: A color name from the
            `X11 Color Names list <https://en.wikipedia.org/wiki/X11_color_names>`_,
            or an integer value from 0-255, or an RGB/RGBA tuple/list
            (e.g. (0,100,0), (100,100,0,50))
        :type color: `str`_ or `int`_ or `tuple`_
        """
viewport = """
        :param viewport: 4 floats between 0 and 1 which specify the area that
            X/Y values are mapped to inside of the canvas.
        :type viewport: list of floats
        """
worldcoordinate = """
        :param worldcoordinate: List of 4 floats (xmin, xmax, ymin, ymax)
        :type worldcoordinate: `list`_
        """
x_y_coords = """
        :param x: List of lists of x coordinates. Values must be floats between
            worldcoordinate[0] and worldcoordinate[1].
        :type x: `list`_

        :param y: List of lists of y coordinates. Values must be floats between
            worldcoordinate[2] and worldcoordinate[3].
        :type y: `list`_
        """
projection = """
        :param projection: Specifies a geographic projection used to convert x/y
            from spherical coordinates into 2D coordinates.
            Can be a VCS projection or a string name of a projection
        :type projection: `str`_ or :py:class:`vcs.projection.Proj`
        """
bg = """
        :param bg: Boolean value. True => object drawn in background (not shown on canvas).
            False => object shown on canvas.
        :type bg: bool
        """
output_width = """
        :param width: Float specifying the desired width of the output,
            in the specified unit of measurement.
        :type width: `float`_
        """
output_file = """
        :param file: Desired string name of the output file
        :type file: `str`_
        """
output_height = """
        :param height: Float specifying the desired height of the output,
            measured in the chosen units
        :type height: `float`_
        """
output_units = """
        :param units: One of ['inches', 'in', 'cm', 'mm', 'pixel', 'pixels',
            'dot', 'dots']. Defaults to 'inches'.
        :type units: `str`_
        """
canvas_width = """
        :param width: Width of the canvas, in pixels
        :type width: `int`_
        """
canvas_height = """
        :param height: Height of the canvas, in pixels
        :type height: `int`_
        """
canvas_clear = """
        :param clear: Indicates the canvas should be cleared (1),
            or should not be cleared (0), when orientation is changed.
        :type clear: `int`_
        """
