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
    <vcs.textcombined.Tc object at 0x118015410>
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
    <vcs.displayplot.Dp object at 0x118568050>
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
    <vcs.displayplot.Dp object at 0x1189005c8>
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
    <vcs.displayplot.Dp object at 0x11a097b40>
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

