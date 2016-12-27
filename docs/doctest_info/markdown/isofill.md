vcs.isofill.Gfi.list
--------------------
```python
Failed example:
    obj.list() # print isofill attributes
Expected nothing
Got:
     ----------Isofill (Gfi) member (attribute) listings ----------
    graphics method = Gfi
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
    datawc_y1 =  1e+20
    datawc_x2 =  1e+20
    datawc_y2 =  1e+20
    datawc_timeunits =  days since 2000
    datawc_calendar =  135441
    xaxisconvert =  linear
    yaxisconvert =  linear
    missing =  (0.0, 0.0, 0.0, 100.0)
    ext_1 =  False
    ext_2 =  False
    fillareastyle =  solid
    fillareaindices =  [1]
    fillareacolors =  [1]
    fillareaopacity =  []
    levels =  ([1.0000000200408773e+20, 1.0000000200408773e+20],)
    legend =  None
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

:x:```    vcs.isofill.Gfi.colors```

:x:```    vcs.isofill.Gfi.datawc```

:x:```    vcs.isofill.Gfi.datawc_calendar```

:x:```    vcs.isofill.Gfi.datawc_timeunits```

:x:```    vcs.isofill.Gfi.datawc_x1```

:x:```    vcs.isofill.Gfi.datawc_x2```

:x:```    vcs.isofill.Gfi.datawc_y1```

:x:```    vcs.isofill.Gfi.datawc_y2```

:x:```    vcs.isofill.Gfi.ext_1```

:x:```    vcs.isofill.Gfi.ext_2```

:x:```    vcs.isofill.Gfi.exts```

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

:x:```    vcs.isofill.Gfi.xmtics```

:x:```    vcs.isofill.Gfi.xmtics1```

:x:```    vcs.isofill.Gfi.xmtics2```

:x:```    vcs.isofill.Gfi.xticlabels```

:x:```    vcs.isofill.Gfi.xticlabels1```

:x:```    vcs.isofill.Gfi.xticlabels2```

:x:```    vcs.isofill.Gfi.yaxisconvert```

:x:```    vcs.isofill.Gfi.ymtics```

:x:```    vcs.isofill.Gfi.ymtics1```

:x:```    vcs.isofill.Gfi.ymtics2```

:x:```    vcs.isofill.Gfi.yticlabels```

:x:```    vcs.isofill.Gfi.yticlabels1```

:x:```    vcs.isofill.Gfi.yticlabels2```

:x:```    vcs.isofill.load```

:x:```    vcs.isofill.process_src```
