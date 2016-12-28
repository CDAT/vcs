vcs.isofill.Gfi.colors
----------------------
```python
Failed example:
    a.plot(ex, array)
Expected nothing
Got:
    <vcs.displayplot.Dp object at 0x118352280>
```

vcs.isofill.Gfi.exts
--------------------
```python
Failed example:
    ex.exts(True, True) # arrows on both ends
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.isofill.Gfi.exts[3]>", line 1, in <module>
        ex.exts(True, True) # arrows on both ends
    AttributeError: 'function' object has no attribute 'exts'
```

vcs.isofill.Gfi.exts
--------------------
```python
Failed example:
    a.plot(ex, array)
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.isofill.Gfi.exts[4]>", line 1, in <module>
        a.plot(ex, array)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 2570, in plot
        arglist = _determine_arg_list(None, actual_args)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 213, in _determine_arg_list
        type(args[i]))
    vcsError: Unknown type <type 'instancemethod'> of argument to plotting command.
```

vcs.isofill.Gfi.script
----------------------
```python
Failed example:
    ex.script('filename.py') # Append to a Python script named 'filename.py'
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.isofill.Gfi.script[2]>", line 1, in <module>
        ex.script('filename.py') # Append to a Python script named 'filename.py'
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/isofill.py", line 856, in script
        fp.write("%s.missing = %g\n" % (unique_name, self.missing))
    TypeError: float argument required, not tuple
```

Missing Doctests
----------------
:x:```    vcs.isofill```

:x:```    vcs.isofill.Gfi```

:x:```    vcs.isofill.Gfi.colormap```

:x:```    vcs.isofill.Gfi.datawc_calendar```

:x:```    vcs.isofill.Gfi.datawc_timeunits```

:x:```    vcs.isofill.Gfi.datawc_x1```

:x:```    vcs.isofill.Gfi.datawc_x2```

:x:```    vcs.isofill.Gfi.datawc_y1```

:x:```    vcs.isofill.Gfi.datawc_y2```

:x:```    vcs.isofill.Gfi.ext_1```

:x:```    vcs.isofill.Gfi.ext_2```

:x:```    vcs.isofill.Gfi.fillareacolors```

:x:```    vcs.isofill.Gfi.fillareaindices```

:x:```    vcs.isofill.Gfi.fillareaopacity```

:x:```    vcs.isofill.Gfi.fillareastyle```

:x:```    vcs.isofill.Gfi.legend```

:x:```    vcs.isofill.Gfi.levels```

:x:```    vcs.isofill.Gfi.missing```

:x:```    vcs.isofill.Gfi.name```

:x:```    vcs.isofill.Gfi.projection```

:x:```    vcs.isofill.Gfi.xaxisconvert```

:x:```    vcs.isofill.Gfi.xmtics1```

:x:```    vcs.isofill.Gfi.xmtics2```

:x:```    vcs.isofill.Gfi.xticlabels1```

:x:```    vcs.isofill.Gfi.xticlabels2```

:x:```    vcs.isofill.Gfi.yaxisconvert```

:x:```    vcs.isofill.Gfi.ymtics1```

:x:```    vcs.isofill.Gfi.ymtics2```

:x:```    vcs.isofill.Gfi.yticlabels1```

:x:```    vcs.isofill.Gfi.yticlabels2```

:x:```    vcs.isofill.load```

:x:```    vcs.isofill.process_src```

