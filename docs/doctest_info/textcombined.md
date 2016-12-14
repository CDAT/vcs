vcs.textcombined.Tc.script
--------------------------
```python
Failed example:
    try: # try to create a new textcombined, in case none exist
        vcs.createtextcombined('EXAMPLE_tt', 'qa', 'EXAMPLE_tto', '7left')
    except:
        pass
Expected nothing
Got:
    <vcs.textcombined.Tc object at 0x117e87230>
```

vcs.textcombined.Tc.script
--------------------------
```python
Failed example:
    ex.script('filename.py') # Append to a Python script named 'filename.py'
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.textcombined.Tc.script[3]>", line 1, in <module>
        ex.script('filename.py') # Append to a Python script named 'filename.py'
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/textcombined.py", line 503, in script
        fp.write("%s.color = %g\n\n" % (unique_name, self.color))
    TypeError: float argument required, not list
```

Missing Doctests
----------------
:x:```    vcs.textcombined```

:x:```    vcs.textcombined.Tc```

:x:```    vcs.textcombined.Tc.To_name```

:x:```    vcs.textcombined.Tc.Tt_name```

:x:```    vcs.textcombined.Tc.__init__```

:x:```    vcs.textcombined.Tc._getToname```

:x:```    vcs.textcombined.Tc._getTtname```

:x:```    vcs.textcombined.Tc._getangle```

:x:```    vcs.textcombined.Tc._getcolor```

:x:```    vcs.textcombined.Tc._getcolormap```

:x:```    vcs.textcombined.Tc._getexpansion```

:x:```    vcs.textcombined.Tc._getfcolor```

:x:```    vcs.textcombined.Tc._getfont```

:x:```    vcs.textcombined.Tc._gethalign```

:x:```    vcs.textcombined.Tc._getheight```

:x:```    vcs.textcombined.Tc._getpath```

:x:```    vcs.textcombined.Tc._getpriority```

:x:```    vcs.textcombined.Tc._getprojection```

:x:```    vcs.textcombined.Tc._getspacing```

:x:```    vcs.textcombined.Tc._getstring```

:x:```    vcs.textcombined.Tc._getvalign```

:x:```    vcs.textcombined.Tc._getviewport```

:x:```    vcs.textcombined.Tc._getworldcoordinate```

:x:```    vcs.textcombined.Tc._getx```

:x:```    vcs.textcombined.Tc._gety```

:x:```    vcs.textcombined.Tc._setToname```

:x:```    vcs.textcombined.Tc._setTtname```

:x:```    vcs.textcombined.Tc._setangle```

:x:```    vcs.textcombined.Tc._setcolor```

:x:```    vcs.textcombined.Tc._setcolormap```

:x:```    vcs.textcombined.Tc._setexpansion```

:x:```    vcs.textcombined.Tc._setfcolor```

:x:```    vcs.textcombined.Tc._setfont```

:x:```    vcs.textcombined.Tc._sethalign```

:x:```    vcs.textcombined.Tc._setheight```

:x:```    vcs.textcombined.Tc._setpath```

:x:```    vcs.textcombined.Tc._setpriority```

:x:```    vcs.textcombined.Tc._setprojection```

:x:```    vcs.textcombined.Tc._setspacing```

:x:```    vcs.textcombined.Tc._setstring```

:x:```    vcs.textcombined.Tc._setvalign```

:x:```    vcs.textcombined.Tc._setviewport```

:x:```    vcs.textcombined.Tc._setworldcoordinate```

:x:```    vcs.textcombined.Tc._setx```

:x:```    vcs.textcombined.Tc._sety```

:x:```    vcs.textcombined.Tc.angle```

:x:```    vcs.textcombined.Tc.color```

:x:```    vcs.textcombined.Tc.colormap```

:x:```    vcs.textcombined.Tc.expansion```

:x:```    vcs.textcombined.Tc.fillincolor```

:x:```    vcs.textcombined.Tc.font```

:x:```    vcs.textcombined.Tc.halign```

:x:```    vcs.textcombined.Tc.height```

:x:```    vcs.textcombined.Tc.list```

:x:```    vcs.textcombined.Tc.path```

:x:```    vcs.textcombined.Tc.priority```

:x:```    vcs.textcombined.Tc.projection```

:x:```    vcs.textcombined.Tc.spacing```

:x:```    vcs.textcombined.Tc.string```

:x:```    vcs.textcombined.Tc.valign```

:x:```    vcs.textcombined.Tc.viewport```

:x:```    vcs.textcombined.Tc.worldcoordinate```

:x:```    vcs.textcombined.Tc.x```

:x:```    vcs.textcombined.Tc.y```

