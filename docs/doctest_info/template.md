vcs.template.P.drawLinesAndMarkersLegend
----------------------------------------
```python
Failed example:
    t.drawLinesAndMarkersLegend(x,
        ["red","blue","green"], ["solid","dash","dot"],[1,4,8],
        ["blue","green","red"], ["cross","square","dot"],[3,4,5],
        ["sample A","type B","thing C"],True)
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.template.P.drawLinesAndMarkersLegend[3]>", line 4, in <module>
        ["sample A","type B","thing C"],True)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/template.py", line 1522, in drawLinesAndMarkersLegend
        strings, scratched, bg, render)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/utils.py", line 2400, in drawLinesAndMarkersLegend
        if scratched is not None and scratched[i] is not False:
    TypeError: 'bool' object has no attribute '__getitem__'
```

vcs.template.P.moveto
---------------------
```python
Failed example:
    t = vcs.createtemplate('example1', 'default') # Create template 'example1', inherits from 'default'
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.template.P.moveto[0]>", line 1, in <module>
        t = vcs.createtemplate('example1', 'default') # Create template 'example1', inherits from 'default'
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 116, in createtemplate
        name, source = check_name_source(name, source, 'template')
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 93, in check_name_source
        raise vcsError("Error %s object named %s already exists" % (typ, name))
    vcsError: Error template object named example1 already exists
```

vcs.template.P.moveto
---------------------
```python
Failed example:
    t.moveto(0.2, 0.2) # Move everything so that data.x1= 0.2 and data.y1= 0.2
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.template.P.moveto[1]>", line 1, in <module>
        t.moveto(0.2, 0.2) # Move everything so that data.x1= 0.2 and data.y1= 0.2
    NameError: name 't' is not defined
```

vcs.template.P.reset
--------------------
```python
Failed example:
    t = vcs.createtemplate('example1', 'default') # template 'example1' inherits from 'default'
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.template.P.reset[0]>", line 1, in <module>
        t = vcs.createtemplate('example1', 'default') # template 'example1' inherits from 'default'
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 116, in createtemplate
        name, source = check_name_source(name, source, 'template')
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 93, in check_name_source
        raise vcsError("Error %s object named %s already exists" % (typ, name))
    vcsError: Error template object named example1 already exists
```

vcs.template.P.reset
--------------------
```python
Failed example:
    t.reset('x',0.15,0.5,t.data.x1,t.data.x2) # Set x1 value to 0.15 and x2 value to 0.5
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.template.P.reset[1]>", line 1, in <module>
        t.reset('x',0.15,0.5,t.data.x1,t.data.x2) # Set x1 value to 0.15 and x2 value to 0.5
    NameError: name 't' is not defined
```

vcs.template.P.scale
--------------------
```python
Failed example:
    t = vcs.createtemplate('example1', 'default') # Create template 'example1', inherits from 'default'
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.template.P.scale[0]>", line 1, in <module>
        t = vcs.createtemplate('example1', 'default') # Create template 'example1', inherits from 'default'
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 116, in createtemplate
        name, source = check_name_source(name, source, 'template')
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 93, in check_name_source
        raise vcsError("Error %s object named %s already exists" % (typ, name))
    vcsError: Error template object named example1 already exists
```

vcs.template.P.scale
--------------------
```python
Failed example:
    t.scale(0.5) # Halves the template size
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.template.P.scale[1]>", line 1, in <module>
        t.scale(0.5) # Halves the template size
    NameError: name 't' is not defined
```

vcs.template.P.scale
--------------------
```python
Failed example:
    t.scale(1.2) # Upsize everything to 20% more than the original size
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.template.P.scale[2]>", line 1, in <module>
        t.scale(1.2) # Upsize everything to 20% more than the original size
    NameError: name 't' is not defined
```

vcs.template.P.scale
--------------------
```python
Failed example:
    t.scale(2,'x') # Double the x axis
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.template.P.scale[3]>", line 1, in <module>
        t.scale(2,'x') # Double the x axis
    NameError: name 't' is not defined
```

Missing Doctests
----------------
:x:```    vcs.template```

:x:```    vcs.template.P```

:x:```    vcs.template.P.__init__```

:x:```    vcs.template.P._getName```

:x:```    vcs.template.P._getOrientation```

:x:```    vcs.template.P._setOrientation```

:x:```    vcs.template.P.blank```

:x:```    vcs.template.P.box1```

:x:```    vcs.template.P.box2```

:x:```    vcs.template.P.box3```

:x:```    vcs.template.P.box4```

:x:```    vcs.template.P.comment1```

:x:```    vcs.template.P.comment2```

:x:```    vcs.template.P.comment3```

:x:```    vcs.template.P.comment4```

:x:```    vcs.template.P.crdate```

:x:```    vcs.template.P.crtime```

:x:```    vcs.template.P.data```

:x:```    vcs.template.P.dataname```

:x:```    vcs.template.P.drawAttributes```

:x:```    vcs.template.P.drawColorBar```

:x:```    vcs.template.P.drawTicks```

:x:```    vcs.template.P.file```

:x:```    vcs.template.P.function```

:x:```    vcs.template.P.legend```

:x:```    vcs.template.P.line1```

:x:```    vcs.template.P.line2```

:x:```    vcs.template.P.line3```

:x:```    vcs.template.P.line4```

:x:```    vcs.template.P.list```

:x:```    vcs.template.P.logicalmask```

:x:```    vcs.template.P.max```

:x:```    vcs.template.P.mean```

:x:```    vcs.template.P.min```

:x:```    vcs.template.P.name```

:x:```    vcs.template.P.orientation```

:x:```    vcs.template.P.plot```

:x:```    vcs.template.P.scalefont```

:x:```    vcs.template.P.source```

:x:```    vcs.template.P.title```

:x:```    vcs.template.P.tname```

:x:```    vcs.template.P.transformation```

:x:```    vcs.template.P.tunits```

:x:```    vcs.template.P.tvalue```

:x:```    vcs.template.P.units```

:x:```    vcs.template.P.xlabel1```

:x:```    vcs.template.P.xlabel2```

:x:```    vcs.template.P.xmintic1```

:x:```    vcs.template.P.xmintic2```

:x:```    vcs.template.P.xname```

:x:```    vcs.template.P.xtic1```

:x:```    vcs.template.P.xtic2```

:x:```    vcs.template.P.xunits```

:x:```    vcs.template.P.xvalue```

:x:```    vcs.template.P.ylabel1```

:x:```    vcs.template.P.ylabel2```

:x:```    vcs.template.P.ymintic1```

:x:```    vcs.template.P.ymintic2```

:x:```    vcs.template.P.yname```

:x:```    vcs.template.P.ytic1```

:x:```    vcs.template.P.ytic2```

:x:```    vcs.template.P.yunits```

:x:```    vcs.template.P.yvalue```

:x:```    vcs.template.P.zname```

:x:```    vcs.template.P.zunits```

:x:```    vcs.template.P.zvalue```

:x:```    vcs.template._getgen```

:x:```    vcs.template._setgen```

:x:```    vcs.template.epsilon_gte```

:x:```    vcs.template.epsilon_lte```

:x:```    vcs.template.process_src```

