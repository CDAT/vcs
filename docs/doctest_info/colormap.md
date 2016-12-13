vcs.colormap.Cp.setcolorcell
----------------------------
```python
Failed example:
    cmap = a.createcolormap('example', 'default') # Create a colormap
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.colormap.Cp.setcolorcell[1]>", line 1, in <module>
        cmap = a.createcolormap('example', 'default') # Create a colormap
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/Canvas.py", line 5721, in createcolormap
        return vcs.createcolormap(Cp_name, Cp_name_src)
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 1785, in createcolormap
        Cp_name, Cp_name_src = check_name_source(Cp_name, Cp_name_src, 'colormap')
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/site-packages/vcs/manageElements.py", line 93, in check_name_source
        raise vcsError("Error %s object named %s already exists" % (typ, name))
    vcsError: Error colormap object named example already exists
```

vcs.colormap.Cp.setcolorcell
----------------------------
```python
Failed example:
    cmap.setcolorcell(40,80,95,1.0) # Set RGBA values
Exception raised:
    Traceback (most recent call last):
      File "/Users/brown308/anaconda/envs/2.8/lib/python2.7/doctest.py", line 1315, in __run
        compileflags, 1) in test.globs
      File "<doctest vcs.colormap.Cp.setcolorcell[2]>", line 1, in <module>
        cmap.setcolorcell(40,80,95,1.0) # Set RGBA values
    NameError: name 'cmap' is not defined
```

