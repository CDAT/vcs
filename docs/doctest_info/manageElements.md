vcs.manageElements.check_name_source
------------------------------------
```python
Failed example:
    cns('polar','quick','boxfill') # is 'polar' boxfill taken?
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.manageElements.check_name_source[2]>", line 1, in <module>
        cns('polar','quick','boxfill') # is 'polar' boxfill taken?
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 93, in check_name_source
        raise vcsError("Error %s object named %s already exists" % (typ, name))
    vcsError: Error boxfill object named polar already exists
```

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

vcs.manageElements.createtext
-----------------------------
```python
Failed example:
    try: # try to create a new textcombined, in case none exist
        vcs.createtextcombined('EXAMPLE_tt', 'qa', 'EXAMPLE_tto', '7left')
    except:
        pass
Expected nothing
Got:
    <vcs.textcombined.Tc object at 0x118041230>
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
    <vcs.displayplot.Dp object at 0x122e4e168>
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
    <vcs.displayplot.Dp object at 0x1187476e0>
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
    <vcs.displayplot.Dp object at 0x11806e7f8>
```

vcs.manageElements.gettaylordiagram
-----------------------------------
```python
Failed example:
    a.taylordiagram(ex) # plot using specified taylordiagram object
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.manageElements.gettaylordiagram[6]>", line 1, in <module>
        a.taylordiagram(ex) # plot using specified taylordiagram object
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 1306, in taylordiagram
        arglist = _determine_arg_list('taylordiagram', args)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 272, in _determine_arg_list
        arglist[igraphics_method])
    vcsError: Graphics method taylordiagram requires 1 slab.
```

Missing Doctests
----------------
:x:```    vcs.manageElements```

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

