import vcs
plot_keywords_doc = """
    :param xaxis: Axis object to replace the slab -1 dim axis
    :param yaxis: Axis object to replace the slab -2 dim axis, only if slab has more than 1D
    :param zaxis: Axis object to replace the slab -3 dim axis, only if slab has more than 2D
    :param taxis: Axis object to replace the slab -4 dim axis, only if slab has more than 3D
    :param waxis: Axis object to replace the slab -5 dim axis, only if slab has more than 4D
    :param xrev: reverse x axis
    :param yrev: reverse y axis, only if slab has more than 1D
    :param xarray: Values to use instead of x axis
    :param yarray: Values to use instead of y axis, only if var has more than 1D
    :param zarray: Values to use instead of z axis, only if var has more than 2D
    :param tarray: Values to use instead of t axis, only if var has more than 3D
    :param warray: Values to use instead of w axis, only if var has more than 4D
    :param continents: continents type number
    :param name: replaces variable name on plot
    :param time: replaces time name on plot
    :param units: replaces units value on plot
    :param ymd: replaces year/month/day on plot
    :param hms: replaces hh/mm/ss on plot
    :param file_comment: replaces file_comment on plot
    :param xbounds: Values to use instead of x axis bounds values
    :param ybounds: Values to use instead of y axis bounds values (if exist)
    :param xname: replace xaxis name on plot
    :param yname: replace yaxis name on plot (if exists)
    :param zname: replace zaxis name on plot (if exists)
    :param tname: replace taxis name on plot (if exists)
    :param wname: replace waxis name on plot (if exists)
    :param xunits: replace xaxis units on plot
    :param yunits: replace yaxis units on plot (if exists)
    :param zunits: replace zaxis units on plot (if exists)
    :param tunits: replace taxis units on plot (if exists)
    :param wunits: replace waxis units on plot (if exists)
    :param xweights: replace xaxis weights used for computing mean
    :param yweights: replace xaxis weights used for computing mean
    :param comment1: replaces comment1 on plot
    :param comment2: replaces comment2 on plot
    :param comment3: replaces comment3 on plot
    :param comment4: replaces comment4 on plot
    :param long_name: replaces long_name on plot
    :param grid: replaces array grid (if exists)
    :param bg: plots in background mode
    :param ratio: sets the y/x ratio ,if passed as a string with 't' at the end, will aslo moves the ticks
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

    :param %stl1: Sets the object's value for :py:attr:`%sticlabels1`. Must be  a str, or a dictionary object with float:str mappings.
    :type %stl1: {float:str} or str

    :param %stl2: Sets the object's value for :py:attr:`%sticlabels2`. Must be a str, or a dictionary object with float:str mappings.
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

# Scriptdocs section

# Use this dictionary for string replacements
#   dict keys are 'type', 'name', and 'call'
#       'type' : The type of VCS object it is (i.e. Graphics method, secondary method, etc.)
#       'name' : The name of the VCS object (i.e. boxfill, isofill, etc.)
#       'call' : The function call for the object. Mostly, this is == name.
#                   Some rare cases, like textcombined, require adjustment of this value.
dict = {}
dict['name'] = dict['type'] = dict['call'] = 'REPLACE_ME'


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

            >>> a=vcs.init() # Make a Canvas object to work with:
            >>> ex=a.get%(call)s() # Get default %(call)s
            >>> ex.script('filename.py') # Append to a Python script named 'filename.py'
            >>> ex.script('filename','w') # Create or overwrite a JSON file 'filename.json'.

    :param script_filename: Output name of the script file. If no extension is specified, a .json object is created.
    :type script_filename: str

    :param mode: Either 'w' for replace, or 'a' for append. Defaults to 'a', if not specified.
    :type mode: str
"""
scriptdocs = {}

# Graphics Method scriptdocs
dict['type'] = 'graphics method'
dict['name'] = dict['call'] = 'colormap'
colormap_script = scriptdoc % dict

dict['name'] = dict['call'] = 'boxfill'
boxfill_script = scriptdoc % dict

dict['name'] = dict['call'] = 'isoline'
isoline_script = scriptdoc % dict

dict['name'] = dict['call'] = 'isofill'
isofill_script = scriptdoc % dict

dict['name'] = dict['call'] = 'yxvsx'
yxvsx_script = scriptdoc % dict

dict['name'] = dict['call'] = 'meshfill'
meshfill_script = scriptdoc % dict

dict['name'] = dict['call'] = 'fillarea'
fillarea_script = scriptdoc % dict

dict['name'] = dict['call'] = 'marker'
marker_script = scriptdoc % dict

dict['name'] = dict['call'] = 'line'
line_script = scriptdoc % dict

dict['name'] = 'text table and text orientation'
dict['call'] = 'textcombined'
textcombined_script = scriptdoc % dict

dict['name'] = dict['call'] = 'textorientation'
textorientation_script = scriptdoc % dict

dict['name'] = dict['call'] = 'texttable'
texttable_script = scriptdoc % dict

dict['name'] = dict['call'] = 'vector'
vector_script = scriptdoc % dict

# Object scriptdocs
dict['type'] = 'object'
dict['name'] = dict['call'] = 'template'
template_script = scriptdoc % dict

# Secondary Method scriptdocs
dict['type'] = 'secondary method'
dict['name'] = dict['call'] = 'projection'
projection_script = scriptdoc % dict
dict.clear()

# dict['parent'] is for rare cases where there is no 'default' object to inherit from.
dict['parent'] = 'REPLACE_ME'
dict['tc_example'] = dict['to'] = ''
queries_is_doc= """
    Check to see if this object is a VCS %(type)s %(name)s %(method_type)s.

    :Example:

        .. doctest:: queries_is

            >>> a=vcs.init() # Make a VCS Canvas object to work with:
            %(tc_example)s
            >>> a.show('%(name)s') # Show all available %(name)s
            *******************%(cap)s Names List**********************
            ...
            *******************End %(cap)s Names List**********************
            >>> ex = a.get%(name)s('%(parent)s'%(to)s) # To  test an existing %(name)s object
            >>> vcs.queries.is%(name)s(ex)
            1

    :param obj: A VCS object
    :type obj: VCS Object

    :returns: An integer indicating whether the object is a %(name)s %(method_type)s (1), or not (0).
    :rtype: int
    """
is_docs = {}
# queries.is[PRIMARY_OBJECT]
dict['type'] = 'primary'
dict['parent'] = 'default'
dict['method_type'] = 'graphics method'

dict['name'] = 'vector'
dict['cap'] = dict['name'].title()
isvector_doc = queries_is_doc % dict
dict['name'] = 'taylordiagram'
dict['cap'] = dict['name'].title()
istaylordiagram_doc = queries_is_doc % dict
dict['name'] = 'meshfill'
dict['cap'] = dict['name'].title()
ismeshfill_doc = queries_is_doc % dict
dict['name'] = 'boxfill'
dict['cap'] = dict['name'].title()
isboxfill_doc= queries_is_doc % dict
dict['name'] = 'isofill'
dict['cap'] = dict['name'].title()
isisofill_doc= queries_is_doc % dict
dict['name'] = 'isoline'
dict['cap'] = dict['name'].title()
isisoline_doc= queries_is_doc % dict
dict['name'] = dict['cap'] = '3d_scalar'
is3d_scalar_doc= queries_is_doc % dict
dict['name'] = dict['cap'] = '3d_dual_scalar'
is3d_dual_scalar_doc= queries_is_doc % dict
dict['name'] = dict['cap'] = '3d_vector'
is3d_vector_doc= queries_is_doc % dict
dict['name'] = 'xvsy'
dict['cap'] = dict['name'].title()
isxvsy_doc = queries_is_doc % dict
dict['name'] = 'yxvsx'
dict['cap'] = dict['name'].title()
isyxvsx_doc = queries_is_doc % dict
dict['name'] = dict['cap'] = '1d'
is1d_doc = queries_is_doc % dict

# special inheritance cases
dict['name'] = 'scatter'
dict['cap'] = dict['name'].title()
dict['parent'] = 'default_scatter_'
isscatter_doc = queries_is_doc % dict
dict['name'] = 'xyvsy'
dict['cap'] = dict['name'].title()
dict['parent'] = 'default_xyvsy_'
isxyvsy_doc = queries_is_doc % dict

# queries.is[SECONDARY_OBJECT]
dict['type'] = 'secondary'
dict['parent'] = 'default'

dict['name'] = 'line'
dict['cap'] = dict['name'].title()
isline_doc = queries_is_doc % dict
dict['name'] = 'marker'
dict['cap'] = dict['name'].title()
ismarker_doc = queries_is_doc % dict
dict['name'] = 'fillarea'
dict['cap'] = dict['name'].title()
isfillarea_doc = queries_is_doc % dict
dict['name'] = 'texttable'
dict['cap'] = dict['name'].title()
istexttable_doc = queries_is_doc % dict
dict['name'] = 'textorientation'
dict['cap'] = dict['name'].title()
istextorientation_doc = queries_is_doc % dict

# queries.is[SPECIAL_CASES]
dict['name'] = 'textcombined'
dict['cap'] = dict['name'].title()
dict['tc_example'] ="""
            >>> vcs.createtext('example_tt', 'std', 'example_to', '7left')
            <vcs.textcombined.Tc ...>
    """
dict['parent'] = 'example_tt'
dict['to'] = ", 'example_to'"
istextcombined_doc = queries_is_doc % dict
dict['tc_example'] = dict['to'] = ''
dict.clear()
# contains api implementation details used to build Example doctests and fill in docstring
obj_details={
    "graphics method": {
        "taylordiagram": {
            "callable": True,
            "parent": "default",
            "parent2": False,
            "rtype": "vcs.taylor.Gtd",
            "slabs": 1,
            "title": True,
        },
        "3d_scalar": {
            "callable": False,
            "parent": "default",
            "parent2": False,
            "rtype": "vcs.dv3d.Gf3Dscalar",
            "slabs": 1,
            "title": False,
        },
        "3d_dual_scalar": {
            "callable": False,
            "parent": "default",
            "parent2": False,
            "rtype": "vcs.dv3d.Gf3DDualScalar",
            "slabs": 2,
            "title": False,
        },
        "3d_vector":{
            "callable": False,
            "parent": "default",
            "parent2": False,
            "rtype": "vcs.dv3d.Gf3Dvector",
            "slabs": 2,
            "title": False,
        },
        "vector": {
            "callable": True,
            "parent": "default",
            "parent2": False,
            "rtype": "vcs.vector.Gv",
            "slabs": 2,
            "title": True,

        },
        "scatter": {
            "callable": True,
            "parent": "default_scatter_",
            "parent2": False,
            "rtype": "vcs.unified1D.G1d",
            "slabs": 2,
            "title": True,
        },
        "yxvsx": {
            "callable": True,
            "parent": "default_yxvsx_",
            "parent2": False,
            "rtype": "vcs.unified1D.G1d",
            "slabs": 1,
            "title": True,
        },
        "xyvsy": {
            "callable": True,
            "parent": "default_xyvsy_",
            "parent2": False,
            "rtype": "vcs.unified1D.G1d",
            "slabs": 1,
            "title": True,
        },
        "xvsy": {
            "callable": True,
            "parent": "default_xvsy_",
            "parent2": False,
            "rtype": "vcs.unified1D.G1d",
            "slabs": 2,
            "title": True,
        },
        "1d": {
            "callable": False,
            "parent": "default",
            "parent2": False,
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
            "parent2": "polar",
            "rtype": "vcs.projection.Proj",
            "slabs": 1,
            "title": True,
        },
        "meshfill": {
            "callable": True,
            "parent": "default",
            "parent2": "polar",
            "rtype": "vcs.meshfill.Gfm",
            "slabs": 1,
            "title": True,
        },
    },
    "secondary method":{
        "fillarea": {
            "callable": True,
            "parent": "default",
            "parent2": False,
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
            "callable": True,
            "parent": "default",
            "parent2": "rainbow",
            "rtype": "vcs.colormap.Cp",
            "slabs": 0,
            "title": True,
        },
        "textcombined": {
            "callable": True,
            "parent": "qa_tt:::left_tto",
            "parent2": False,
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

def cleanup(string):
    """
    Removes extraneous empty lines from a string.

    :param string: A string to strip of empty strings contained therein
    :return: A string with all the empty strings stripped out
    """
    raw = string.split('\n')
    for _ in raw:
        if _ == '':
            raw.remove(_)
    clean = '\n'.join(raw)
    return clean

def populate_docstrings(type_dict, target_dict, docstring, method):
    """
    A function to generate docstrings from a dictionary.
    Structure of the function is pretty specific to type_dicts shaped like xmldoc.obj_details.

    Indentation of the docstring snippets looks screwy because they need to maintain alignment
    with the original docstring entries for Sphinx to pick them up correctly.

    :param type_dict: The dictionary to parse for values used to fill in the docstring
    :param target_dict: An empty dictionary to be populated with docstrings
    :param docstring: The template docstring
    :param method: The method that the docstring is for
    """
    for obj_type in type_dict.keys():
        dict = {}
        # example entries should default to empty
        example1 = ''
        example2 = ''
        dict['type'] = obj_type
        for obj_name in type_dict[obj_type].keys():
            # default values. Change as necessary.
            dict['name'] = dict['sp_name'] = obj_name
            dict['parent'] = type_dict[obj_type][obj_name]['parent']
            dict['parent2'] = ''
            dict['sp_parent'] = ''
            dict['tc'] = ''
            dict['ex2'] = ''
            dict['rtype'] = type_dict[obj_type][obj_name]['rtype']
            if type_dict[obj_type][obj_name]['title']:
                dict['cap'] = dict['name'].title()
            else:
                dict['cap'] = dict['name']
            if method == 'get':
                example1 = """%(tc)s
            >>> ex=vcs.get%(name)s(%(sp_parent)s)  # instance of '%(parent)s' %(name)s %(type)s%(plot)s"""
                if obj_name in ['3d_vector', '3d_scalar', '3d_dual_scalar']:
                    dict['sp_name'] = 'dv3d'
                elif obj_name in ['1d','scatter','textcombined','xyvsy']:
                    if obj_name == 'textcombined':
                        dict['tc'] = """
            >>> vcs.createtext('qa_tt', 'qa', 'left_tto', '7left') # Create 'qa_tt' and 'left_tto'
            <vcs.textcombined.Tc object at ...>"""
                        dict['sp_parent'] = "'qa_tt', 'left_tto'"
                    else:
                        sp_parent = 'default_'+obj_name+'_'
                        dict['sp_parent'] = "'%s'" % sp_parent
                        dict['parent'] = dict['sp_parent']

                # set up dict['plot'] and dict['plot2']
                plot = ''
                plot2 = ''
                numslabs = type_dict[obj_type][obj_name]['slabs']
                dict['slabs'] = ''
                dict['args'] = ''
                if numslabs > 0:
                    dict['slabs'] = """
            >>> import cdms2 # Need cdms2 to create a slab
            >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # use cdms2 to open a data file
            >>> slab1 = f('u') # use the data file to create a cdms2 slab"""
                    dict['args'] = ", slab1"
                    if numslabs == 2:
                        slab2 = """
            >>> slab2 = f('v') # need 2 slabs, so get another"""
                        dict['slabs'] = dict['slabs'] + slab2
                        dict['args'] = dict['args'] + ", slab2"
                # for vcs objects that have a self-named function, i.e. fillarea()
                if type_dict[obj_type][obj_name]['callable']:
                    plot = """%(slabs)s
            >>> a.%(name)s(ex%(args)s) # plot using specified %(name)s object
            <vcs.displayplot.Dp ...>"""
                    # set up plot2
                    plot2 = """
            >>> a.%(name)s(ex2%(args)s) # plot using specified %(name)s object
            <vcs.displayplot.Dp ...>"""
                # for objects like template, where a call to plot() needs to be made
                elif obj_name not in ['textorientation', 'texttable']:
                    plot = """%(slabs)s
            >>> a.plot(ex%(args)s) # plot using specified %(name)s object
            <vcs.displayplot.Dp ...>"""
                    plot2 = """
            >>> a.plot(ex2%(args)s) # plot using specified %(name)s object
            <vcs.displayplot.Dp ...>"""
                dict['plot'] = plot % dict
                dict['ex1'] = example1 % dict
                if type_dict[obj_type][obj_name]['parent2']:
                    dict['parent2'] = type_dict[obj_type][obj_name]['parent2']
                    example2 = """
            >>> ex2=vcs.get%(name)s('%(parent2)s')  # instance of '%(parent2)s' %(name)s %(type)s%(plot2)s
                    """
                    dict['plot2'] = plot2 % dict
                    dict['ex2'] = example2 % dict
            elif method == 'create':
                example2 ="""
            >>> ex2=vcs.create%(name)s('example2','%(parent)s') # create 'example2' from '%(parent)s' template
            >>> vcs.show('%(name)s') # should now contain the 'example2' %(name)s
            *******************%(cap)s Names List**********************
            ...
            *******************End %(cap)s Names List**********************"""
                dict['plot'] = """
            >>> a.%(name)s(ex) # Plot using specified %(name)s object
            <vcs.displayplot.Dp ...>"""
                dict['plot2'] = """
            >>> a.plot(ex2) # Plot using specified %(name)s object
            <vcs.displayplot.Dp ...>"""
                dict['ex2'] = example2
            target_dict[obj_name] = docstring % dict

get_methods_doc = """
    VCS contains a list of %(type)ss. This function will create a
    %(sp_name)s class object from an existing VCS %(sp_name)s %(type)s. If
    no %(sp_name)s name is given, then %(sp_name)s '%(parent)s' will be used.

    .. note::

        VCS does not allow the modification of 'default' attribute sets.
        However, a 'default' attribute set that has been copied under a
        different name can be modified. (See the :py:func:`vcs.manageElements.create%(name)s` function.)

    :Example:

        .. doctest:: manageElements_get

            >>> a=vcs.init()
            >>> vcs.show('%(name)s') # Show all the existing %(name)s %(type)ss
            *******************%(cap)s Names List**********************
            ...
            *******************End %(cap)s Names List**********************%(ex1)s%(ex2)s"""
get_docs = {}
populate_docstrings(obj_details, get_docs, get_methods_doc, 'get')

create_methods_doc = """
    Create a new %(name)s %(type)s given the the name and the existing
    %(name)s %(type)s to copy the attributes from. If no existing
    %(name)s %(type)s is given, then the default %(name)s %(type)s will be used as the graphics method
    to which the attributes will be copied from.

    .. note::

        If the name provided already exists, then an error will be returned. %(type)s
        names must be unique.

    :Example:

        .. doctest:: manageElements_create

            >>> vcs.show('%(name)s') # show all available %(name)s
            *******************%(cap)s Names List**********************
            ...
            *******************End %(cap)s Names List**********************
            >>> ex=vcs.create%(call)s('example1') # Create %(name)s 'example1' that inherits from 'default'
            >>> vcs.show('%(name)s') # should now contain the 'example1' %(name)s
            *******************%(cap)s Names List**********************
            ...
            *******************End %(cap)s Names List**********************
            %(ex2)s

    :param name: The name of the created object
    :type name: str

    :param source: The object to inherit from
    :type source: a %(name)s or a string name of a %(name)s

    :returns: A %(name)s %(type)s object
    :rtype: %(rtype)s
    """
create_docs = {}
# Graphics method create methods
#   no second example
dict['type'] = 'graphics method'
dict['ex2'] = ''
dict['name'] = dict['call'] = 'taylordiagram'
dict['cap'] = dict['name'].title()

# No type create methods
dict['type'] = ''
dict['name'] = dict['call'] = 'template'
dict['parent'] = 'quick'
dict['ex2'] = """
            >>> ex2=vcs.create%(name)s('example2','%(parent)s') # create 'example2' from '%(parent)s' template
            >>> vcs.show('%(name)s') # should now contain the 'example2' %(name)s
            *******************%(cap)s Names List**********************
            ...
            *******************End %(cap)s Names List**********************
    """ % dict


exts_attrs= """
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
    """ % (levels_attr,fillarea_colors_attr, fillarea_attrs, legend_attr, exts_attrs, missing_attr)

isofill_doc = meshfill_doc

fillareadoc = """
    fillareacolor :: (int) (None) color to use for outfilling
    fillareastyle :: (str) ('solid') style to use for levels filling: solid/pattenr/hatch
    fillareaindex :: (int) (None) pattern to use when filling a level and using pattern/hatch
    """  # noqa

linesdoc = """    line :: ([str,...]/[vcs.line.Tl,...]/[int,...]) (['solid',]) line type to use for each isoline, can also pass a line object or line object name
    linecolors :: ([int,...]) ([241]) colors to use for each isoline
    linewidths :: ([float,...]) ([1.0]) list of width for each isoline
    """  # noqa
linedoc = """    line :: ([str,...]/[vcs.line.Tl,...]/[int,...]) (['solid',]) line type to use for each isoline, can also pass a line object or line object name
    linecolor :: (int) (241) colors to use for each isoline
    linewidth :: (float) (1.0) list of width for each isoline
    """  # noqa

textsdoc = """
    text :: (None/[vcs.textcombined.Tc,...]) (None) text objects or text objects names to use for each countour labels
    textcolors :: (None/[int,...]) (None) colors to use for each countour labels
    """  # noqa

markerdoc = """
    marker :: (None/int/str/vcs.marker.Tm) (None) markers type to use
    markercolor :: (None/int) (None) color to use for markers
    markersize :: (None/int) (None) size of markers
    """

#############################################################################
#                                                                           #
# Graphics Method input section.                                            #
#                                                                           #
#############################################################################

create_GM_input = """
    :param new_GM_name: (Ex: 'my_awesome_gm') name of the new graphics method object. If no name is given, then one will be created for use.
    :type new_GM_name: str
    :param source_GM_name: (Ex: 'default') copy the contents of the source object to the newly created one. If no name is given, then the 'default' graphics methond contents is copied over to the new object.
    :type source_GM_name: str
    """  # noqa

get_GM_input = """
    :param GM_name: (Ex: 'default') retrieve the graphics method object of the given name. If no name is given, then retrieve the 'default' graphics method.
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
    :param slab_or_primary_object: Data at least 1D, last dimension(s) will be plotted, or secondary vcs object
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
