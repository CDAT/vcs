vcs.manageElements.createtext
-----------------------------
```python
Failed example:
    vcs.show('textcombined') # show all available textcombined
Expected:
    *******************Textcombined Names List**********************
    ...
    *******************End Textcombined Names List**********************
Got:
    *******************Textcombined Names List**********************
    *******************End Textcombined Names List**********************
```

vcs.manageElements.get3d_dual_scalar
------------------------------------
```python
Failed example:
    a.plot(ex, slab1, slab2) # plot using specified 3d_dual_scalar object
Expected:
    <vcs.displayplot.Dp ...>
Got:
    initCamera: Camera => ((0.0, 0.0, 540.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)) 
    <vcs.displayplot.Dp object at 0x124057d70>
```

vcs.manageElements.get3d_scalar
-------------------------------
```python
Failed example:
    a.plot(ex, slab1) # plot using specified 3d_scalar object
Expected:
    <vcs.displayplot.Dp ...>
Got:
    initCamera: Camera => ((0.0, 0.0, 540.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)) 
    <vcs.displayplot.Dp object at 0x1187704b0>
```

vcs.manageElements.get3d_vector
-------------------------------
```python
Failed example:
    a.plot(ex, slab1, slab2) # plot using specified 3d_vector object
Expected:
    <vcs.displayplot.Dp ...>
Got:
    Sample rate: 6 
    Sample rate: 6 
    initCamera: Camera => ((0.0, 0.0, 540.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)) 
    <vcs.displayplot.Dp object at 0x1180be398>
```

vcs.manageElements.gettaylordiagram
-----------------------------------
```python
Failed example:
    a.taylordiagram(ex, slab1) # plot using specified taylordiagram object
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.manageElements.gettaylordiagram[6]>", line 1, in <module>
        a.taylordiagram(ex, slab1) # plot using specified taylordiagram object
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 1275, in taylordiagram
        return self.__plot(arglist, parms)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 3634, in __plot
        t.plot(arglist[0], canvas=self, template=arglist[2], **keyargs)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/taylor.py", line 1967, in plot
        self.draw(canvas, data)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/taylor.py", line 1207, in draw
        d0 = float(data[i][0])
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/numpy/ma/core.py", line 4182, in __float__
        raise TypeError("Only length-1 arrays can be converted "
    TypeError: Only length-1 arrays can be converted to Python scalars
```

vcs.manageElements.gettextcombined
----------------------------------
```python
Failed example:
    vcs.createtextcombined('EXAMPLE_tt', 'qa', 'EXAMPLE_tto', '7left') # Create 'EXAMPLE_tt' and 'EXAMPLE_tto'
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.manageElements.gettextcombined[2]>", line 1, in <module>
        vcs.createtextcombined('EXAMPLE_tt', 'qa', 'EXAMPLE_tto', '7left') # Create 'EXAMPLE_tt' and 'EXAMPLE_tto'
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 1435, in createtextcombined
        Tt_name, Tt_source = check_name_source(Tt_name, Tt_source, 'texttable')
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 57, in check_name_source
        raise vcsError("Error %s object named %s already exists" % (typ, name))
    vcsError: Error texttable object named EXAMPLE_tt already exists
```

Missing Doctests
----------------
:x:```    vcs.manageElements```

:x:```    vcs.manageElements.check_name_source```

:x:```    vcs.manageElements.removeCp```

:x:```    vcs.manageElements.removeG```

:x:```    vcs.manageElements.removeG1d```

:x:```    vcs.manageElements.removeGSp```

:x:```    vcs.manageElements.removeGXY```

:x:```    vcs.manageElements.removeGXy```

:x:```    vcs.manageElements.removeGYx```

:x:```    vcs.manageElements.removeGfb```

:x:```    vcs.manageElements.removeGfi```

:x:```    vcs.manageElements.removeGfm```

:x:```    vcs.manageElements.removeGi```

:x:```    vcs.manageElements.removeGtd```

:x:```    vcs.manageElements.removeGv```

:x:```    vcs.manageElements.removeP```

:x:```    vcs.manageElements.removeProj```

:x:```    vcs.manageElements.removeTc```

:x:```    vcs.manageElements.removeTf```

:x:```    vcs.manageElements.removeTl```

:x:```    vcs.manageElements.removeTm```

:x:```    vcs.manageElements.removeTo```

:x:```    vcs.manageElements.removeTt```

