vcs.queries.isplot
------------------
```python
Failed example:
    vcs.queries.isplot(dsp_plot)
Expected:
    1
Got:
    0
```

vcs.queries.istextcombined
--------------------------
```python
Failed example:
    try: # try to create a new textcombined, in case none exist
        vcs.createtextcombined('EXAMPLE_tt', 'qa', 'EXAMPLE_tto', '7left')
    except:
        pass
Expected nothing
Got:
    <vcs.textcombined.Tc object at 0x117fc1230>
```

Missing Doctests
----------------
:x:```    vcs.queries```

