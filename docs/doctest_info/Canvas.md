vcs.Canvas.Canvas.canvasid
--------------------------
```python
Failed example:
    a.canvasid()
Expected nothing
Got:
    2
```

vcs.Canvas.Canvas.check_name_source
-----------------------------------
```python
Failed example:
    cns('polar','quick','boxfill') # is 'polar' boxfill taken?
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.Canvas.Canvas.check_name_source[2]>", line 1, in <module>
        cns('polar','quick','boxfill') # is 'polar' boxfill taken?
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 93, in check_name_source
        raise vcsError("Error %s object named %s already exists" % (typ, name))
    vcsError: Error boxfill object named polar already exists
```

vcs.Canvas.Canvas.clean_auto_generated_objects
----------------------------------------------
```python
Failed example:
    a.plot(array)
Expected nothing
Got:
    <vcs.displayplot.Dp object at 0x118580d70>
```

vcs.Canvas.Canvas.clean_auto_generated_objects
----------------------------------------------
```python
Failed example:
    boxes == new_boxes
Expected:
    True
Got:
    False
```

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
    <vcs.textcombined.Tc object at 0x118041b90>
```

vcs.Canvas.Canvas.drawtext
--------------------------
```python
Failed example:
    vcs.createtextcombined('draw_tt', 'qa', 'draw_tto', '7left')
Expected nothing
Got:
    <vcs.textcombined.Tc object at 0x1185be9b0>
```

vcs.Canvas.Canvas.drawtext
--------------------------
```python
Failed example:
    tc=a.drawtextcombined(Tt_name = 'draw_tt', To_name='draw_tto')
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.Canvas.Canvas.drawtext[3]>", line 1, in <module>
        tc=a.drawtextcombined(Tt_name = 'draw_tt', To_name='draw_tto')
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 2353, in drawtextcombined
        t.string = string
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/textcombined.py", line 286, in _setstring
        self.Tt.string = value
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/texttable.py", line 307, in _setstring
        raise ValueError('Must be a string or a list of strings.')
    ValueError: Must be a string or a list of strings.
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
    <vcs.displayplot.Dp object at 0x11838f050>
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
    <vcs.displayplot.Dp object at 0x151797168>
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
    <vcs.displayplot.Dp object at 0x1517b3910>
```

vcs.Canvas.Canvas.gettaylordiagram
----------------------------------
```python
Failed example:
    a.taylordiagram(ex) # plot using specified taylordiagram object
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.Canvas.Canvas.gettaylordiagram[6]>", line 1, in <module>
        a.taylordiagram(ex) # plot using specified taylordiagram object
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 1306, in taylordiagram
        arglist = _determine_arg_list('taylordiagram', args)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 272, in _determine_arg_list
        arglist[igraphics_method])
    vcsError: Graphics method taylordiagram requires 1 slab.
```

vcs.Canvas.Canvas.initLogoDrawing
---------------------------------
```python
Failed example:
    a.plot(array) # should have logo in lower right corner
Expected nothing
Got:
    <vcs.displayplot.Dp object at 0x157a49280>
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

vcs.Canvas.Canvas.isopened
--------------------------
```python
Failed example:
    a.plot(array)
Expected nothing
Got:
    <vcs.displayplot.Dp object at 0x15fc41c58>
```

vcs.Canvas.Canvas.return_display_names
--------------------------------------
```python
Failed example:
    a.plot(array)
Expected nothing
Got:
    <vcs.displayplot.Dp object at 0x189fdca28>
```

vcs.Canvas.Canvas.setdefaultfont
--------------------------------
```python
Failed example:
    a.setdefaultfont('Times')
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.Canvas.Canvas.setdefaultfont[2]>", line 1, in <module>
        a.setdefaultfont('Times')
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 5910, in setdefaultfont
        return self.copyfontto(font, 1)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 5890, in copyfontto
        return self.canvas.copyfontto(*(index1, index2))
    AttributeError: 'module' object has no attribute 'copyfontto'
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

:x:```    vcs.Canvas.Canvas.getfontname```

:x:```    vcs.Canvas.Canvas.getfontnumber```

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

