vcs.Canvas.Canvas.createprojection
----------------------------------
```python
Failed example:
    ex2=vcs.createprojection('projection_ex2','polar') # create 'projection_ex2' from 'polar' template
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.Canvas.Canvas.createprojection[3]>", line 1, in <module>
        ex2=vcs.createprojection('projection_ex2','polar') # create 'projection_ex2' from 'polar' template
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 120, in createprojection
        return projection.Proj(name, source)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/projection.py", line 434, in __init__
        self.type = src.type
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/projection.py", line 987, in _settype
        value = VCS_validation_functions.checkProjType(self, 'type', value)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/VCS_validation_functions.py", line 1440, in checkProjType
        checkedRaise(self, value, Exception, err)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/VCS_validation_functions.py", line 59, in checkedRaise
        raise ex(err)
    Exception: type can either be ('linear', 'utm', 'state plane', 'albers equal area', 'lambert', 'mercator', 'polar', 'polyconic', 'equid conic a', 'transverse mercator', 'stereographic', 'lambert azimuthal', 'azimuthal', 'gnomonic', 'orthographic', 'gen. vert. near per', 'sinusoidal', 'equirectangular', 'miller', 'van der grinten', 'hotin', 'robinson', 'space oblique', 'alaska', 'interrupted goode', 'mollweide', 'interrupted mollweide', 'hammer', 'wagner iv', 'wagner vii', 'oblated') or (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)
```

vcs.Canvas.Canvas.drawtext
--------------------------
```python
Failed example:
    vcs.createtextcombined('EXAMPLE_tt', 'qa', 'EXAMPLE_tto', '7left')
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.Canvas.Canvas.drawtext[2]>", line 1, in <module>
        vcs.createtextcombined('EXAMPLE_tt', 'qa', 'EXAMPLE_tto', '7left')
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 1390, in createtextcombined
        Tt_name, Tt_source = check_name_source(Tt_name, Tt_source, 'texttable')
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 57, in check_name_source
        raise vcsError("Error %s object named %s already exists" % (typ, name))
    vcsError: Error texttable object named EXAMPLE_tt already exists
```

vcs.Canvas.Canvas.ffmpeg
------------------------
```python
Failed example:
    for i in range(10): # create a number of pngs to use for an mpeg
        a.clear()
        if (i%2):
            a.plot(u,v)
        else:
            a.plot(v,u)
        a.png('my_png__%i' % i)
        png_files.append('my_png__%i.png' % i)
Expected nothing
Got:
    <vcs.displayplot.Dp object at 0x1186bca28>
    <vcs.displayplot.Dp object at 0x1186db7f8>
    <vcs.displayplot.Dp object at 0x11833b910>
    <vcs.displayplot.Dp object at 0x1186286e0>
    <vcs.displayplot.Dp object at 0x11861fa28>
    <vcs.displayplot.Dp object at 0x11835e910>
    <vcs.displayplot.Dp object at 0x130ab1398>
    <vcs.displayplot.Dp object at 0x118600168>
    <vcs.displayplot.Dp object at 0x1186d4050>
    <vcs.displayplot.Dp object at 0x11868ba28>
```

vcs.Canvas.Canvas.get3d_dual_scalar
-----------------------------------
```python
Failed example:
    a.plot(ex, slab1, slab2) # plot using specified 3d_dual_scalar object
Expected:
    <vcs.displayplot.Dp ...>
Got:
    initCamera: Camera => ((0.0, 0.0, 540.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)) 
    <vcs.displayplot.Dp object at 0x130ab6280>
```

vcs.Canvas.Canvas.get3d_scalar
------------------------------
```python
Failed example:
    a.plot(ex, slab1) # plot using specified 3d_scalar object
Expected:
    <vcs.displayplot.Dp ...>
Got:
    initCamera: Camera => ((0.0, 0.0, 540.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)) 
    <vcs.displayplot.Dp object at 0x118d305c8>
```

vcs.Canvas.Canvas.get3d_vector
------------------------------
```python
Failed example:
    a.plot(ex, slab1, slab2) # plot using specified 3d_vector object
Expected:
    <vcs.displayplot.Dp ...>
Got:
    Sample rate: 6 
    Sample rate: 6 
    initCamera: Camera => ((0.0, 0.0, 540.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)) 
    <vcs.displayplot.Dp object at 0x118d9dd70>
```

vcs.Canvas.Canvas.gettaylordiagram
----------------------------------
```python
Failed example:
    a.taylordiagram(ex, slab1) # plot using specified taylordiagram object
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.Canvas.Canvas.gettaylordiagram[6]>", line 1, in <module>
        a.taylordiagram(ex, slab1) # plot using specified taylordiagram object
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 1275, in taylordiagram
        return self.__plot(arglist, parms)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 3634, in __plot
        t.plot(arglist[0], canvas=self, template=arglist[2], **keyargs)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/taylor.py", line 1965, in plot
        self.draw(canvas, data)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/taylor.py", line 1205, in draw
        d0 = float(data[i][0])
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/numpy/ma/core.py", line 4182, in __float__
        raise TypeError("Only length-1 arrays can be converted "
    TypeError: Only length-1 arrays can be converted to Python scalars
```

vcs.Canvas.Canvas.gettextcombined
---------------------------------
```python
Failed example:
    vcs.createtextcombined('EXAMPLE_tt', 'qa', 'EXAMPLE_tto', '7left') # Create 'EXAMPLE_tt' and 'EXAMPLE_tto'
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.Canvas.Canvas.gettextcombined[2]>", line 1, in <module>
        vcs.createtextcombined('EXAMPLE_tt', 'qa', 'EXAMPLE_tto', '7left') # Create 'EXAMPLE_tt' and 'EXAMPLE_tto'
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 1390, in createtextcombined
        Tt_name, Tt_source = check_name_source(Tt_name, Tt_source, 'texttable')
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 57, in check_name_source
        raise vcsError("Error %s object named %s already exists" % (typ, name))
    vcsError: Error texttable object named EXAMPLE_tt already exists
```

vcs.Canvas.Canvas.objecthelp
----------------------------
```python
Failed example:
    a.objecthelp(ln) # This will print out information on how to use ln
Expected nothing
Got:
    <BLANKLINE>
        The Line object allows the manipulation of line type, width, color index,
        view port, world coordinates, and (x,y) points.
    <BLANKLINE>
        This class is used to define an line table entry used in VCS, or it
        can be used to change some or all of the line attributes in an
        existing line table entry.
    <BLANKLINE>
        .. describe:: Useful Functions:
    <BLANKLINE>
            .. code-block:: python
    <BLANKLINE>
                # VCS Canvas Constructor
                a=vcs.init()
                # Show predefined line objects
                a.show('line')
                # Will list all the line attribute values
                ln.list()
                # Updates the VCS Canvas at user's request
                a.update()
    <BLANKLINE>
        .. describe:: Create a new instance of line:
    <BLANKLINE>
            .. code-block:: python
    <BLANKLINE>
                # Copies content of 'red' to 'new'
                ln=a.createline('new','red')
                # Copies content of 'default' to 'new'
                ln=a.createline('new')
    <BLANKLINE>
        .. describe:: Modify an existing line:
    <BLANKLINE>
            * Get a line object 'ln' to manipulate:
    <BLANKLINE>
                .. code-block:: python
    <BLANKLINE>
                    ln=a.getline('red')
    <BLANKLINE>
            * Set line color:
    <BLANKLINE>
                .. code-block:: python
    <BLANKLINE>
                    # Range from 1 to 256
                    ln.color=100
    <BLANKLINE>
            * Set line width:
    <BLANKLINE>
                .. code-block:: python
    <BLANKLINE>
                    # Range from 1 to 300
                    ln.width=100
    <BLANKLINE>
            * Specify the line type:
    <BLANKLINE>
                .. code-block:: python
    <BLANKLINE>
                    # Same as ln.type=0
                     ln.type='solid'
                     # Same as ln.type=1
                     ln.type='dash'
                     # Same as ln.type=2
                     ln.type='dot'
                     # Same as ln.type=3
                     ln.type='dash-dot'
                     # Same as ln.type=4
                     ln.type='long-dash'
    <BLANKLINE>
            * Set the graphics priority on the canvas:
    <BLANKLINE>
                .. code-block:: python
    <BLANKLINE>
                    ln.priority=1
                    # FloatType [0,1]x[0,1]
                    ln.viewport=[0, 1.0, 0,1.0]
                    # FloatType [#,#]x[#,#]
                    ln.worldcoordinate=[0,1.0,0,1.0]
    <BLANKLINE>
            * Set line x and y values:
    <BLANKLINE>
                .. code-block:: python
    <BLANKLINE>
                    # List of FloatTypes
                    ln.x=[[0,.1,.2], [.3,.4,.5]]
                    # List of FloatTypes
                    ln.y=[[.5,.4,.3], [.2,.1,0]]
    <BLANKLINE>
```

Missing Doctests
----------------
:x:```    vcs.Canvas```

:x:```    vcs.Canvas.Canvas```

:x:```    vcs.Canvas.Canvas._Canvas__new_elts```

:x:```    vcs.Canvas.Canvas._Canvas__plot```

:x:```    vcs.Canvas.Canvas.__init__```

:x:```    vcs.Canvas.Canvas._compute_margins```

:x:```    vcs.Canvas.Canvas._compute_width_height```

:x:```    vcs.Canvas.Canvas._continentspath```

:x:```    vcs.Canvas.Canvas._datawc_tv```

:x:```    vcs.Canvas.Canvas._get_user_actions```

:x:```    vcs.Canvas.Canvas._get_user_actions_names```

:x:```    vcs.Canvas.Canvas._getanimate```

:x:```    vcs.Canvas.Canvas._getanimate_info```

:x:```    vcs.Canvas.Canvas._getcanvas```

:x:```    vcs.Canvas.Canvas._getisplottinggridded```

:x:```    vcs.Canvas.Canvas._getmode```

:x:```    vcs.Canvas.Canvas._getpausetime```

:x:```    vcs.Canvas.Canvas._getvarglist```

:x:```    vcs.Canvas.Canvas._getviewport```

:x:```    vcs.Canvas.Canvas._getwinfo_id```

:x:```    vcs.Canvas.Canvas._getworldcoordinate```

:x:```    vcs.Canvas.Canvas._reconstruct_tv```

:x:```    vcs.Canvas.Canvas._scriptrun```

:x:```    vcs.Canvas.Canvas._set_user_actions```

:x:```    vcs.Canvas.Canvas._set_user_actions_names```

:x:```    vcs.Canvas.Canvas._setanimate```

:x:```    vcs.Canvas.Canvas._setanimate_info```

:x:```    vcs.Canvas.Canvas._setcanvas```

:x:```    vcs.Canvas.Canvas._setisplottinggridded```

:x:```    vcs.Canvas.Canvas._setmode```

:x:```    vcs.Canvas.Canvas._setpausetime```

:x:```    vcs.Canvas.Canvas._setvarglist```

:x:```    vcs.Canvas.Canvas._setviewport```

:x:```    vcs.Canvas.Canvas._setwinfo_id```

:x:```    vcs.Canvas.Canvas._setworldcoordinate```

:x:```    vcs.Canvas.Canvas.addfont```

:x:```    vcs.Canvas.Canvas.animate```

:x:```    vcs.Canvas.Canvas.animate_info```

:x:```    vcs.Canvas.Canvas.canvas```

:x:```    vcs.Canvas.Canvas.canvasid```

:x:```    vcs.Canvas.Canvas.canvasinfo```

:x:```    vcs.Canvas.Canvas.cgm```

:x:```    vcs.Canvas.Canvas.change_display_graphic_method```

:x:```    vcs.Canvas.Canvas.check_name_source```

:x:```    vcs.Canvas.Canvas.clean_auto_generated_objects```

:x:```    vcs.Canvas.Canvas.configure```

:x:```    vcs.Canvas.Canvas.copyfontto```

:x:```    vcs.Canvas.Canvas.create1d```

:x:```    vcs.Canvas.Canvas.dual_scalar3d```

:x:```    vcs.Canvas.Canvas.dummy_user_action```

:x:```    vcs.Canvas.Canvas.endconfigure```

:x:```    vcs.Canvas.Canvas.get1d```

:x:```    vcs.Canvas.Canvas.get_selected_display```

:x:```    vcs.Canvas.Canvas.getantialiasing```

:x:```    vcs.Canvas.Canvas.getcolormapname```

:x:```    vcs.Canvas.Canvas.getcontinentsline```

:x:```    vcs.Canvas.Canvas.getfontname```

:x:```    vcs.Canvas.Canvas.getfontnumber```

:x:```    vcs.Canvas.Canvas.getplot```

:x:```    vcs.Canvas.Canvas.gif```

:x:```    vcs.Canvas.Canvas.grid```

:x:```    vcs.Canvas.Canvas.gs```

:x:```    vcs.Canvas.Canvas.initLogoDrawing```

:x:```    vcs.Canvas.Canvas.interact```

:x:```    vcs.Canvas.Canvas.isinfile```

:x:```    vcs.Canvas.Canvas.isopened```

:x:```    vcs.Canvas.Canvas.isplottinggridded```

:x:```    vcs.Canvas.Canvas.match_color```

:x:```    vcs.Canvas.Canvas.mode```

:x:```    vcs.Canvas.Canvas.onClosing```

:x:```    vcs.Canvas.Canvas.pause_time```

:x:```    vcs.Canvas.Canvas.plot_annotation```

:x:```    vcs.Canvas.Canvas.plot_filledcontinents```

:x:```    vcs.Canvas.Canvas.processParameterChange```

:x:```    vcs.Canvas.Canvas.put_png_on_canvas```

:x:```    vcs.Canvas.Canvas.raisecanvas```

:x:```    vcs.Canvas.Canvas.removeP```

:x:```    vcs.Canvas.Canvas.remove_display_name```

:x:```    vcs.Canvas.Canvas.return_display_names```

:x:```    vcs.Canvas.Canvas.savecontinentstype```

:x:```    vcs.Canvas.Canvas.scalar3d```

:x:```    vcs.Canvas.Canvas.scriptrun```

:x:```    vcs.Canvas.Canvas.setAnimationStepper```

:x:```    vcs.Canvas.Canvas.setantialiasing```

:x:```    vcs.Canvas.Canvas.setdefaultfont```

:x:```    vcs.Canvas.Canvas.show```

:x:```    vcs.Canvas.Canvas.start```

:x:```    vcs.Canvas.Canvas.switchfonts```

:x:```    vcs.Canvas.Canvas.updateorientation```

:x:```    vcs.Canvas.Canvas.user_actions```

:x:```    vcs.Canvas.Canvas.user_actions_names```

:x:```    vcs.Canvas.Canvas.varglist```

:x:```    vcs.Canvas.Canvas.vector3d```

:x:```    vcs.Canvas.Canvas.viewport```

:x:```    vcs.Canvas.Canvas.winfo_id```

:x:```    vcs.Canvas.Canvas.worldcoordinate```

:x:```    vcs.Canvas.SIGNAL```

:x:```    vcs.Canvas.SIGNAL.__call__```

:x:```    vcs.Canvas.SIGNAL.__init__```

:x:```    vcs.Canvas.SIGNAL.clear```

:x:```    vcs.Canvas.SIGNAL.connect```

:x:```    vcs.Canvas.SIGNAL.disconnect```

:x:```    vcs.Canvas._determine_arg_list```

:x:```    vcs.Canvas._process_keyword```

:x:```    vcs.Canvas.change_date_time```

:x:```    vcs.Canvas.dictionarytovcslist```

