vcs.meshfill.Gfm.colors
-----------------------
```python
Failed example:
    a.plot(ex, array, array)
Expected nothing
Got:
    <vcs.displayplot.Dp object at 0x118345398>
```

vcs.meshfill.Gfm.exts
---------------------
```python
Failed example:
    ex.exts(True, True) # arrows on both ends
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.meshfill.Gfm.exts[3]>", line 1, in <module>
        ex.exts(True, True) # arrows on both ends
    AttributeError: 'function' object has no attribute 'exts'
```

vcs.meshfill.Gfm.exts
---------------------
```python
Failed example:
    a.plot(ex, array, array)
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.meshfill.Gfm.exts[4]>", line 1, in <module>
        a.plot(ex, array, array)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 2570, in plot
        arglist = _determine_arg_list(None, actual_args)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 213, in _determine_arg_list
        type(args[i]))
    vcsError: Unknown type <type 'instancemethod'> of argument to plotting command.
```

vcs.meshfill.Gfm.list
---------------------
```python
Failed example:
    obj.list() # print meshfill attributes
Expected:
     ----------...----------
    ...
Got:
     ---------- Meshfill (Gmf) member (attribute) listings ---------
    graphics method = Gfm
    name = default
    projection = linear
    xticlabels1 = *
    xticlabels2 = *
    xmtics1 = 
    xmtics2 = 
    yticlabels1 = *
    yticlabels2 = *
    ymtics1 = 
    ymtics2 = 
    datawc_x1 = 1e+20
    datawc_y1 = 1e+20
    datawc_x2 = 1e+20
    datawc_y2 = 1e+20
    datawc_timeunits =  days since 2000
    datawc_calendar =  135441
    xaxisconvert = linear
    yaxisconvert = linear
    levels = ([1.0000000200408773e+20, 1.0000000200408773e+20],)
    fillareacolors = [1]
    fillareastyle = solid
    fillareaindices = None
    legend = None
    ext_1 = False
    ext_2 = False
    missing = (0.0, 0.0, 0.0, 100.0)
    mesh = 0
    wrap = [0.0, 0.0]
    colormap =  None
```

vcs.meshfill.Gfm.script
-----------------------
```python
Failed example:
    ex.script('filename.py') # Append to a Python script named 'filename.py'
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.meshfill.Gfm.script[2]>", line 1, in <module>
        ex.script('filename.py') # Append to a Python script named 'filename.py'
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/meshfill.py", line 900, in script
        fp.write("%s.missing = %g\n\n" % (unique_name, self.missing))
    TypeError: float argument required, not tuple
```

Missing Doctests
----------------
:x:```    vcs.meshfill```

:x:```    vcs.meshfill.Gfm```

:x:```    vcs.meshfill.Gfm.colormap```

:x:```    vcs.meshfill.Gfm.datawc_calendar```

:x:```    vcs.meshfill.Gfm.datawc_timeunits```

:x:```    vcs.meshfill.Gfm.datawc_x1```

:x:```    vcs.meshfill.Gfm.datawc_x2```

:x:```    vcs.meshfill.Gfm.datawc_y1```

:x:```    vcs.meshfill.Gfm.datawc_y2```

:x:```    vcs.meshfill.Gfm.ext_1```

:x:```    vcs.meshfill.Gfm.ext_2```

:x:```    vcs.meshfill.Gfm.fillareacolors```

:x:```    vcs.meshfill.Gfm.fillareaindices```

:x:```    vcs.meshfill.Gfm.fillareaopacity```

:x:```    vcs.meshfill.Gfm.fillareastyle```

:x:```    vcs.meshfill.Gfm.legend```

:x:```    vcs.meshfill.Gfm.levels```

:x:```    vcs.meshfill.Gfm.mesh```

:x:```    vcs.meshfill.Gfm.missing```

:x:```    vcs.meshfill.Gfm.name```

:x:```    vcs.meshfill.Gfm.projection```

:x:```    vcs.meshfill.Gfm.wrap```

:x:```    vcs.meshfill.Gfm.xaxisconvert```

:x:```    vcs.meshfill.Gfm.xmtics1```

:x:```    vcs.meshfill.Gfm.xmtics2```

:x:```    vcs.meshfill.Gfm.xticlabels1```

:x:```    vcs.meshfill.Gfm.xticlabels2```

:x:```    vcs.meshfill.Gfm.yaxisconvert```

:x:```    vcs.meshfill.Gfm.ymtics1```

:x:```    vcs.meshfill.Gfm.ymtics2```

:x:```    vcs.meshfill.Gfm.yticlabels1```

:x:```    vcs.meshfill.Gfm.yticlabels2```

:x:```    vcs.meshfill.load```

:x:```    vcs.meshfill.process_src```

