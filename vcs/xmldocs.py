plot_keywords_doc = """
    :param xaxis: Axis object to replace the slab -1 dim axis.
        Keyword parameter.
    :param yaxis: Axis object to replace the slab -2 dim axis, only if slab has more than 1D.
        Keyword parameter.
    :param zaxis: Axis object to replace the slab -3 dim axis, only if slab has more than 2D.
        Keyword parameter.
    :param taxis: Axis object to replace the slab -4 dim axis, only if slab has more than 3D.
        Keyword parameter.
    :param waxis: Axis object to replace the slab -5 dim axis, only if slab has more than 4D.
        Keyword parameter.
    :param xrev: reverse x axis.
        Keyword parameter.
    :param yrev: reverse y axis, only if slab has more than 1D.
        Keyword parameter.
    :param xarray: Values to use instead of x axis.
        Keyword parameter.
    :param yarray: Values to use instead of y axis, only if var has more than 1D.
        Keyword parameter.
    :param zarray: Values to use instead of z axis, only if var has more than 2D.
        Keyword parameter.
    :param tarray: Values to use instead of t axis, only if var has more than 3D.
        Keyword parameter.
    :param warray: Values to use instead of w axis, only if var has more than 4D.
        Keyword parameter.
    :param continents: continents type number.
        Keyword parameter.
    :param name: replaces variable name on plot.
        Keyword parameter.
    :param time: replaces time name on plot.
        Keyword parameter.
    :param units: replaces units value on plot.
        Keyword parameter.
    :param ymd: replaces year/month/day on plot.
        Keyword parameter.
    :param hms: replaces hh/mm/ss on plot.
        Keyword parameter.
    :param file_comment: replaces file_comment on plot.
        Keyword parameter.
    :param xbounds: Values to use instead of x axis bounds values.
        Keyword parameter.
    :param ybounds: Values to use instead of y axis bounds values (if exist).
        Keyword parameter.
    :param xname: replace xaxis name on plot.
        Keyword parameter.
    :param yname: replace yaxis name on plot (if exists).
        Keyword parameter.
    :param zname: replace zaxis name on plot (if exists).
        Keyword parameter.
    :param tname: replace taxis name on plot (if exists).
        Keyword parameter.
    :param wname: replace waxis name on plot (if exists).
        Keyword parameter.
    :param xunits: replace xaxis units on plot.
        Keyword parameter.
    :param yunits: replace yaxis units on plot (if exists).
        Keyword parameter.
    :param zunits: replace zaxis units on plot (if exists).
        Keyword parameter.
    :param tunits: replace taxis units on plot (if exists).
        Keyword parameter.
    :param wunits: replace waxis units on plot (if exists).
        Keyword parameter.
    :param xweights: replace xaxis weights used for computing mean.
        Keyword parameter.
    :param yweights: replace xaxis weights used for computing mean.
        Keyword parameter.
    :param comment1: replaces comment1 on plot.
        Keyword parameter.
    :param comment2: replaces comment2 on plot.
        Keyword parameter.
    :param comment3: replaces comment3 on plot.
        Keyword parameter.
    :param comment4: replaces comment4 on plot.
        Keyword parameter.
    :param long_name: replaces long_name on plot.
        Keyword parameter.
    :param grid: replaces array grid (if exists).
        Keyword parameter.
    :param bg: plots in background mode.
        Keyword parameter.
    :param ratio: sets the y/x ratio ,if passed as a string with 't' at the end, will aslo moves the ticks.
        Keyword parameter.
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
colorsdoc = """
    Sets the color_1 and color_2 properties of the object.

    :param color1: Sets the :py:attr:`color_1` value on the object
    :type color1: int

    :param color2: Sets the :py:attr:`color_2` value on the object
    :type color2: int
    """

extsdoc = """
    Sets the ext_1 and ext_2 values on the object.

    :param ext1: Sets the :py:attr:`ext_1` value on the object. 'y' sets it to True, 'n' sets it to False.
    :type ext1: str

    :param ext2: Sets the :py:attr:`ext_2` value on the object. 'y' sets it to True, 'n' sets it to False.
    :type ext2: str
           """
ticlabelsdoc = """
    Sets the %sticlabels1 and %sticlabels2 values on the object

    :param %stl1: Sets the object's value for :py:attr:`%sticlabels1`.
                  Must be  a str, or a dictionary object with float:str mappings.
    :type %stl1: {float:str} or str

    :param %stl2: Sets the object's value for :py:attr:`%sticlabels2`.
                  Must be a str, or a dictionary object with float:str mappings.
    :type %stl2: {float:str} or str
           """
xticlabelsdoc = ticlabelsdoc % (('x',) * 8)
yticlabelsdoc = ticlabelsdoc % (('y',) * 8)

mticsdoc = """
    Sets the %smtics1 and %smtics2 values on the object

    :param %smt1: Value for :py:attr:`%smtics1`. Must be a str, or a dictionary object with float:str mappings.
    :type %smt1: {float:str} or str

    :param %smt2: Value for :py:attr:`%smtics2`. Must be a str, or a dictionary object with float:str mappings.
    :type %smt2: {float:str} or str
    """
xmticsdoc = mticsdoc % (('x',) * 8)
ymticsdoc = mticsdoc % (('y',) * 8)

datawcdoc = """
    Sets the data world coordinates for object

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

        .. doctest:: xyscale_%s

            >>> a=vcs.init()
            >>> ex=a.create%s('xyscale_ex') # create a boxfill to work with
            >>> ex.xyscale(xat='linear', yat='linear') # set xaxisconvert and yaxisconvert to 'linear'

    :param xat: Set value for x axis conversion.
    :type xat: str

    :param yat: Set value for y axis conversion.
    :type yat: str
    """
listdoc = """ Lists the current values of object attributes"""


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
    for obj_type in type_dict.keys():
        for obj_name in type_dict[obj_type].keys():
            # default values. Change as necessary.
            example1 = ''
            example2 = ''
            d['type'] = obj_type
            d['name'] = d['sp_name'] = obj_name
            d['parent'] = type_dict[obj_type][obj_name]['parent']
            d['parent2'] = type_dict[obj_type][obj_name]['parent2']
            d['sp_parent'] = ''
            d['tc'] = ''
            d['ex2'] = ''
            d['rtype'] = type_dict[obj_type][obj_name]['rtype']
            if type_dict[obj_type][obj_name]['title']:
                d['cap'] = d['name'].title()
            else:
                d['cap'] = d['name']
            if obj_name in ['3d_vector', '3d_scalar', '3d_dual_scalar']:
                d['sp_name'] = 'dv3d'
            elif obj_name in ['1d', 'scatter', 'textcombined', 'xyvsy']:
                if obj_name == 'textcombined':
                    d['tc'] = """
            >>> try: # try to create a new textcombined, in case none exist
            ...     vcs.createtextcombined('EXAMPLE_tt', 'qa', 'EXAMPLE_tto', '7left')
            ... except:
            ...     pass"""
                    d['sp_parent'] = "'EXAMPLE_tt', 'EXAMPLE_tto'"
                elif obj_name == '1d':
                    d['sp_parent'] = "'default'"
                else:
                    sp_parent = 'default_'+obj_name+'_'
                    d['sp_parent'] = "'%s'" % sp_parent
                    d['parent'] = d['sp_parent']
        # section for manageElements 'get' methods
            if method == 'get':
                example1 = """%(tc)s
            >>> ex=vcs.get%(name)s(%(sp_parent)s)  # instance of '%(parent)s' %(name)s %(type)s%(plot)s"""
                # set up d['plot'] and d['plot2']
                plot = ''
                plot2 = ''
                numslabs = type_dict[obj_type][obj_name]['slabs']
                d['slabs'] = ''
                d['args'] = ''
                if numslabs > 0:
                    # TODO: replace with something that can actually be plotted by taylordiagram()
                    if obj_name is "taylordiagram":
                        d['slabs'] = """
            >>> import cdms2 # Need cdms2 to create a slab
            >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # use cdms2 to open a data file
            >>> slab1 = f('u') # use the data file to create a cdms2 slab"""
                    else:
                        d['slabs'] = """
            >>> import cdms2 # Need cdms2 to create a slab
            >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # use cdms2 to open a data file
            >>> slab1 = f('u') # use the data file to create a cdms2 slab"""
                    d['args'] = ", slab1"
                    if numslabs == 2:
                        slab2 = """
            >>> slab2 = f('v') # need 2 slabs, so get another"""
                        d['slabs'] = d['slabs'] + slab2
                        d['args'] = d['args'] + ", slab2"
            # for vcs objects that have a self-named plotting function, i.e. fillarea()
                if type_dict[obj_type][obj_name]['callable']:
                    plot = """%(slabs)s
            >>> a.%(name)s(ex%(args)s) # plot using specified %(name)s object
            <vcs.displayplot.Dp ...>"""
                    # set up plot2
                    plot2 = """
            >>> a.%(name)s(ex2%(args)s) # plot using specified %(name)s object
            <vcs.displayplot.Dp ...>"""
            # for objects like template, where a call to plot() needs to be made
            # objects in the list cannot be plotted without a graphics method
                elif obj_name not in ['textorientation', 'texttable', 'colormap', 'projection', 'template']:
                    plot = """%(slabs)s
            >>> a.plot(ex%(args)s) # plot using specified %(name)s object
            <vcs.displayplot.Dp ...>"""
                    plot2 = """
            >>> a.plot(ex2%(args)s) # plot using specified %(name)s object
            <vcs.displayplot.Dp ...>"""
                d['plot'] = plot % d
                d['ex1'] = example1 % d
                if d['parent2']:
                    example2 = """
            >>> ex2=vcs.get%(name)s('%(parent2)s')  # instance of '%(parent2)s' %(name)s %(type)s%(plot2)s
                    """
                    d['plot2'] = plot2 % d
                    d['ex2'] = example2 % d
        # section for manageElements 'create' methods
            elif method == 'create':
                # if obj_name is tc, d['tc'] should be populated by code that creates a tc at this point
                if obj_name == "textcombined":
                    example1 = d['tc'] + """
            >>> vcs.listelements('%(name)s') # should now contain 'EXAMPLE_tt:::EXAMPLE_tto'
            [...'EXAMPLE_tt:::EXAMPLE_tto'...]"""
                else:
                    example1 = """
            >>> ex=vcs.create%(name)s('%(name)s_ex1') # Create '%(name)s_ex1'; inherits 'default'
            >>> vcs.listelements('%(name)s') # should now contain '%(name)s_ex1'
            [...'%(name)s_ex1'...]"""
                d['ex1'] = example1 % d
                if d['parent2']:
                    example2 = """
            >>> ex2=vcs.create%(name)s('%(name)s_ex2','%(parent2)s') # create '%(name)s_ex2'; inherits '%(parent2)s'
            >>> vcs.listelements('%(name)s') # should now contain '%(name)s_ex2'
            [...'%(name)s_ex2'...]"""
                    d['ex2'] = example2 % d
            elif method == 'script':
                if obj_name == "textcombined":
                    d['call'] = obj_name
                    d['name'] = 'text table and text orientation'
                else:
                    d['call'] = d['name']
            target_dict[obj_name] = docstring % d
            d.clear()

# contains VCS object details used to build Example doctests and fill in docstrings
#   Keys:
#       "callable"(bool): specifies whether the object has a self-named plotting function, i.e. fillarea()
#       "parent"(str): specifies the name of the object to be used in inheritance for a first example.
#           Usually 'default', but it can change based on situation.
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
            "parent": "EXAMPLE_tt:::EXAMPLE_tto",
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
# this will be used to populate all the docstrings in the same for loop (should better utilize locality)
docstrings = {}

scriptdoc = """
    Saves out a copy of the %(name)s %(type)s in JSON, or Python format to a designated file.

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

            >>> a=vcs.init() # Make a Canvas object to work with%(tc)s
            >>> ex=a.get%(call)s(%(sp_parent)s) # Get default %(call)s
            >>> ex.script('filename.py') # Append to a Python script named 'filename.py'
            >>> ex.script('filename','w') # Create or overwrite a JSON file 'filename.json'.

    :param script_filename: Output name of the script file. If no extension is specified, a .json object is created.
    :type script_filename: str

    :param mode: Either 'w' for replace, or 'a' for append. Defaults to 'a', if not specified.
    :type mode: str
    """


queries_is_doc = """
    Check to see if this object is a VCS %(name)s %(type)s.

    :Example:

        .. doctest:: queries_is

            >>> a=vcs.init() # Make a VCS Canvas object to work with:%(tc)s
            >>> a.show('%(name)s') # Show all available %(name)s
            *******************%(cap)s Names List**********************
            ...
            *******************End %(cap)s Names List**********************
            >>> ex = a.get%(name)s(%(sp_parent)s) # To  test an existing %(name)s object
            >>> vcs.queries.is%(name)s(ex)
            1

    :param obj: A VCS object
    :type obj: VCS Object

    :returns: An integer indicating whether the object is a %(name)s %(type)s (1), or not (0).
    :rtype: int
    """

get_methods_doc = """
    VCS contains a list of %(type)ss. This function will create a
    %(sp_name)s class object from an existing VCS %(sp_name)s %(type)s. If
    no %(sp_name)s name is given, then %(parent)s %(sp_name)s will be used.

    .. note::

        VCS does not allow the modification of 'default' attribute sets.
        However, a 'default' attribute set that has been copied under a
        different name can be modified. (See the :py:func:`vcs.manageElements.create%(name)s` function.)

    :Example:

        .. doctest:: manageElements_get

            >>> a=vcs.init()
            >>> vcs.listelements('%(name)s') # Show all the existing %(name)s %(type)ss
            [...]%(ex1)s%(ex2)s"""

create_methods_doc = """
    Create a new %(sp_name)s %(type)s given the the name and the existing
    %(sp_name)s %(type)s to copy the attributes from. If no existing
    %(sp_name)s %(type)s is given, then the default %(sp_name)s %(type)s will be used as the graphics method
    to which the attributes will be copied from.

    .. note::

        If the name provided already exists, then an error will be returned. %(type)s
        names must be unique.

    :Example:

        .. doctest:: manageElements_create

            >>> vcs.show('%(name)s') # show all available %(name)s
            *******************%(cap)s Names List**********************
            ...
            *******************End %(cap)s Names List**********************%(ex1)s%(ex2)s
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
for method in docstrings.keys():
    populate_docstrings(obj_details, docstrings[method][0], docstrings[method][1], method)

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
    :return: Display Plot object representing the plot.
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
