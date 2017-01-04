vcs.vcshelp.help
----------------
```python
Failed example:
    vcs.help('getboxfill')
Expected nothing
Got:
    VCS contains a list of graphics methods. This function
        will create a boxfill object from an existing
        VCS boxfill graphics method. If no boxfill name is given,
        then default boxfill will be used.
    <BLANKLINE>
        .. note::
    <BLANKLINE>
            VCS does not allow the modification of 'default' attribute sets.
            However, a 'default' attribute set that has been copied under a
            different name can be modified.
            (See the :py:func:`vcs.manageElements.createboxfill` function.)
    <BLANKLINE>
        :Example:
    <BLANKLINE>
            .. doctest:: manageElements_get
    <BLANKLINE>
                >>> a=vcs.init()
                >>> vcs.listelements('boxfill') # list all boxfills
                [...]
                >>> ex=vcs.getboxfill()  # 'default' boxfill
                >>> import cdms2 # Need cdms2 to create a slab
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # get data with cdms2
                >>> slab1 = f('u') # take a slab from the data
                >>> a.boxfill(ex, slab1) # plot boxfill
                <vcs.displayplot.Dp ...>
                >>> ex2=vcs.getboxfill('polar')  # boxfill #2
                >>> a.boxfill(ex2, slab1) # plot boxfill
                <vcs.displayplot.Dp ...>
    <BLANKLINE>
    <BLANKLINE>
        :param Gfb_name_src: String name of an existing boxfill VCS object
        :type Gfb_name_src: :py:class:`str`
    <BLANKLINE>
        :return: A pre-existing boxfill graphics method
        :rtype: vcs.boxfill.Gfb
    <BLANKLINE>
```

Missing Doctests
----------------
:x:```    vcs.vcshelp```

:x:```    vcs.vcshelp.help__doc__```

:x:```    vcs.vcshelp.mode__doc__```

