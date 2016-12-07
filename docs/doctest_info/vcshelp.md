vcs.vcshelp.objecthelp
----------------------
```python
Failed example:
    vcs.objecthelp(fa)
Expected:
    <BLANKLINE>
    The Fillarea class object...
Got:
    <BLANKLINE>
        The Fillarea class object allows the user to edit fillarea attributes, including
        fillarea interior style, style index, and color index.
    <BLANKLINE>
        This class is used to define an fillarea table entry used in VCS, or it
        can be used to change some or all of the fillarea attributes in an
        existing fillarea table entry.
    <BLANKLINE>
    <BLANKLINE>
        .. describe:: Useful Functions:
    <BLANKLINE>
            .. code-block:: python
    <BLANKLINE>
                # VCS Canvas Constructor
                a=vcs.init()
                # Show predefined fillarea objects
                a.show('fillarea')
                # Updates the VCS Canvas at user's request
                a.update()
    <BLANKLINE>
        .. describe:: Create a fillarea object:
    <BLANKLINE>
            .. code-block:: python
    <BLANKLINE>
                #Create a VCS Canvas object
                a=vcs.init()
    <BLANKLINE>
                # Two ways to create a fillarea:
    <BLANKLINE>
                # Copies content of 'def37' to 'new'ea:
                fa=a.createfillarea('new','def37')
                # Copies content of 'default' to 'new'
                fa=a.createfillarea('new')
    <BLANKLINE>
        .. describe::  Modify an existing fillarea:
    <BLANKLINE>
            .. code-block:: python
    <BLANKLINE>
                fa=a.getfillarea('red')
    <BLANKLINE>
        * Overview of fillarea attributes:
    <BLANKLINE>
            * List all the fillarea attribute values
    <BLANKLINE>
                .. code-block:: python
    <BLANKLINE>
                    fa.list()
    <BLANKLINE>
            * There are three possibilities for setting the isofill style:
    <BLANKLINE>
                .. code-block:: python
    <BLANKLINE>
                    fa.style = 'solid'
                    fa.style = 'hatch'
                    fa.style = 'pattern'
    <BLANKLINE>
            * Setting index, color, opacity:
    <BLANKLINE>
                .. code-block:: python
    <BLANKLINE>
                    # Range from 1 to 20
                    fa.index=1
                    # Range from 1 to 256
                    fa.color=100
                    # Range from 0 to 100
                    fa.opacity=100
    <BLANKLINE>
            * Setting the graphics priority viewport, worldcoordinate:
    <BLANKLINE>
                .. code-block:: python
    <BLANKLINE>
                    fa.priority=1
                    # FloatType [0,1]x[0,1]
                    fa.viewport=[0, 1.0, 0,1.0]
                    # FloatType [#,#]x[#,#]
                    fa.worldcoordinate=[0,1.0,0,1.0]
    <BLANKLINE>
            * Setting x and y values:
    <BLANKLINE>
                .. code-block:: python
    <BLANKLINE>
                    #List of FloatTypes
                    fa.x=[[0,.1,.2], [.3,.4,.5]]
                    # List of FloatTypes
                    fa.y=[[.5,.4,.3], [.2,.1,0]]
    <BLANKLINE>
    <BLANKLINE>
```

