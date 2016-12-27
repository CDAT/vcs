vcs.Canvas.Canvas.createtext
----------------------------
```python
Failed example:
    try: # try to create a new textcombined, in case none exist
        vcs.createtextcombined('EXAMPLE_tt', 'qa', 'EXAMPLE_tto', '7left')
    except:
        pass
Expected nothing
Got:
    <vcs.textcombined.Tc object at 0x1180eb320>
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
    <vcs.displayplot.Dp object at 0x11c7057f8>
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
    <vcs.displayplot.Dp object at 0x153eab5c8>
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
    <vcs.displayplot.Dp object at 0x153e695c8>
```

vcs.Canvas.Canvas.isinfile
--------------------------
```python
Failed example:
    a.isinfile(box, 'deft_box.py')
Expected:
    1
Got nothing
```

Missing Doctests
----------------
:x:```    vcs.Canvas```

:x:```    vcs.Canvas.Canvas```

:x:```    vcs.Canvas.Canvas.addfont```

:x:```    vcs.Canvas.Canvas.animate```

:x:```    vcs.Canvas.Canvas.animate_info```

:x:```    vcs.Canvas.Canvas.canvas```

:x:```    vcs.Canvas.Canvas.cgm```

:x:```    vcs.Canvas.Canvas.configure```

:x:```    vcs.Canvas.Canvas.copyfontto```

:x:```    vcs.Canvas.Canvas.dual_scalar3d```

:x:```    vcs.Canvas.Canvas.endconfigure```

:x:```    vcs.Canvas.Canvas.get1d```

:x:```    vcs.Canvas.Canvas.get_selected_display```

:x:```    vcs.Canvas.Canvas.getplot```

:x:```    vcs.Canvas.Canvas.gif```

:x:```    vcs.Canvas.Canvas.grid```

:x:```    vcs.Canvas.Canvas.gs```

:x:```    vcs.Canvas.Canvas.interact```

:x:```    vcs.Canvas.Canvas.isplottinggridded```

:x:```    vcs.Canvas.Canvas.mode```

:x:```    vcs.Canvas.Canvas.onClosing```

:x:```    vcs.Canvas.Canvas.pause_time```

:x:```    vcs.Canvas.Canvas.plot_annotation```

:x:```    vcs.Canvas.Canvas.plot_filledcontinents```

:x:```    vcs.Canvas.Canvas.processParameterChange```

:x:```    vcs.Canvas.Canvas.removeP```

:x:```    vcs.Canvas.Canvas.savecontinentstype```

:x:```    vcs.Canvas.Canvas.scalar3d```

:x:```    vcs.Canvas.Canvas.scriptrun```

:x:```    vcs.Canvas.Canvas.setAnimationStepper```

:x:```    vcs.Canvas.Canvas.setdefaultfont```

:x:```    vcs.Canvas.Canvas.start```

:x:```    vcs.Canvas.Canvas.updateorientation```

:x:```    vcs.Canvas.Canvas.user_actions```

:x:```    vcs.Canvas.Canvas.user_actions_names```

:x:```    vcs.Canvas.Canvas.varglist```

:x:```    vcs.Canvas.Canvas.vector3d```

:x:```    vcs.Canvas.Canvas.viewport```

:x:```    vcs.Canvas.Canvas.winfo_id```

:x:```    vcs.Canvas.Canvas.worldcoordinate```

:x:```    vcs.Canvas.SIGNAL```

:x:```    vcs.Canvas.SIGNAL.clear```

:x:```    vcs.Canvas.SIGNAL.connect```

:x:```    vcs.Canvas.SIGNAL.disconnect```

:x:```    vcs.Canvas.change_date_time```

:x:```    vcs.Canvas.dictionarytovcslist```
