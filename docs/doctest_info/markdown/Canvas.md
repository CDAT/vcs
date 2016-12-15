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
    <vcs.textcombined.Tc object at 0x1186ab050>
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
    <vcs.displayplot.Dp object at 0x1354a87f8>
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
    <vcs.displayplot.Dp object at 0x127bde280>
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
    <vcs.displayplot.Dp object at 0x14f922280>
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
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 1320, in taylordiagram
        return self.__plot(arglist, parms)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 3700, in __plot
        t.plot(arglist[0], canvas=self, template=arglist[2], **keyargs)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/taylor.py", line 1967, in plot
        self.draw(canvas, data)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/taylor.py", line 1207, in draw
        d0 = float(data[i][0])
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/numpy/ma/core.py", line 4182, in __float__
        raise TypeError("Only length-1 arrays can be converted "
    TypeError: Only length-1 arrays can be converted to Python scalars
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

:x:```    vcs.Canvas.SIGNAL.__call__```

:x:```    vcs.Canvas.SIGNAL.__init__```

:x:```    vcs.Canvas.SIGNAL.clear```

:x:```    vcs.Canvas.SIGNAL.connect```

:x:```    vcs.Canvas.SIGNAL.disconnect```

:x:```    vcs.Canvas._determine_arg_list```

:x:```    vcs.Canvas._process_keyword```

:x:```    vcs.Canvas.change_date_time```

:x:```    vcs.Canvas.dictionarytovcslist```

