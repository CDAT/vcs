vcs.vcshelp.help
----------------
```python
Failed example:
    vcs.help('getboxfill')
Expected nothing
Got:
    VCS contains a list of graphics methods. This function will create a
        boxfill class object from an existing VCS boxfill graphics method. If
        no boxfill name is given, then default boxfill will be used.
    <BLANKLINE>
        .. note::
    <BLANKLINE>
            VCS does not allow the modification of 'default' attribute sets.
            However, a 'default' attribute set that has been copied under a
            different name can be modified. (See the :py:func:`vcs.manageElements.createboxfill` function.)
    <BLANKLINE>
        :Example:
    <BLANKLINE>
            .. doctest:: manageElements_get
    <BLANKLINE>
                >>> a=vcs.init()
                >>> vcs.listelements('boxfill') # Show all the existing boxfill graphics methods
                [...]
                >>> ex=vcs.getboxfill()  # instance of 'default' boxfill graphics method
                >>> import cdms2 # Need cdms2 to create a slab
                >>> f = cdms2.open(vcs.sample_data+'/clt.nc') # use cdms2 to open a data file
                >>> slab1 = f('u') # use the data file to create a cdms2 slab
                >>> a.boxfill(ex, slab1) # plot using specified boxfill object
                <vcs.displayplot.Dp ...>
                >>> ex2=vcs.getboxfill('polar')  # instance of 'polar' boxfill graphics method
                >>> a.boxfill(ex2, slab1) # plot using specified boxfill object
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

