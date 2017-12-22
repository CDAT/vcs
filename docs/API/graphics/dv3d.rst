===================
3D Graphics Methods
===================

Deriving actionable information from climate simulations requires the capacity to detect, compare, and analyze features
spanning large heterogeneous, multi-variate, multi-dimensional datasets with spatial and temporal references. The
brain’s capacity to detect visual patterns is invaluable in this knowledge discovery process. Visual mapping techniques
are very effective in expressing the results of feature detection and analysis algorithms as they naturally employ the
visual information processing capacity of the cerebral cortex, which is extremely difficult to emulate using statistical
and machine learning approaches alone. Visual representations, which play an important role in addressing data
complexity, can be enhanced by an increase in the number of “degrees of freedom” in the visual mapping process.
Interactive three-dimensional views into complex high dimensional datasets can offer a widened perspective and a more
comprehensive gestalt facilitating the recognition of significant features and the discovery of important patterns and
relationships in the climate knowledge discovery process.


3D Plot Constituents
--------------------

In the VCS model 3D perspectives are provided by the 3d_scalar and 3d_vector graphics methods.

The 3d_scalar graphics method provides the :term:`Volume`, :term:`Surface`, and :term:`Slice` display
techniques (denoted henceforth as “plot constituents”). It can be used to display data in both the default (x-y-z) and
Hovmoller3D (x-y-t)geometries.

The 3d_vector graphics method provides the :term:`Vector` slice plot constituent.

.. glossary::

    Volume
        The Volume plot enables scientists to create an overview of the topology of the data, revealing complex 3D structures at
        a glance. It is generated using a “transfer function” to linearly map an adjustable range of variable values to an
        adjustable range of opacity values at each point of a 3D volume. Values of the variable that fall outside of the range
        are invisible (transparent). In addition, the rendered color is determined by mapping the variable’s value at each point
        of the volume to an adjustable range of colormap values. All three adjustable ranges can be configured either statically
        using a script or interactively using sliders in an active plot window.

    Surface
        The Surface plot can produce views similar to a volume rendering while facilitating the comparison of two variables. It
        is displayed as an isosurface (the higher dimensional analog of an isoline or contour line on a weather or terrain map),
        illustrating the surfaces of constant value for one variable and optionally colored by the spatially correspondent
        values of a second variable. The rendered color is determined by mapping the second variable’s value at each point of
        the surface to an adjustable range of colormap values. The isosurface value and the colormap range can be configured
        either statically using a script or interactively using sliders in an active plot window.

    Slice
        The Slice plot allows scientists to quickly and easily browse the 3D structure of a dataset, compare variables in 3D,
        and probe data values. It provides a set of three slice planes (perpendicular to the x, y, and z axes) that can be
        interactively dragged over the dataset. A slice through the data volume at the plane’s location is displayed by mapping
        the variable’s value at each point of the plane to an adjustable range of colormap values. A slice through a second data
        volume can also be overlaid as a contour map over the first. In an active plot window a shift-right-click on one of the
        planes will display the coordinates and value of the variable(s) at that point. The slice positions and the colormap
        range can be configured either statically using a script or interactively using sliders in an active plot window

    Vector
        The Vector slice plot allows scientists to browse the 3D structure of variables (such as wind velocity) that have both
        magnitude and direction. It provides a horizontal slice plane that can be interactively dragged over a vector field
        dataset (consisting of a pair of variables denoting the X and Y components of a vector at each point). A slice through
        the data volume at the plane’s location is displayed using a set of vector glyphs denoting the direction and magnitude
        of the field at a regularly spaced set of points on the plane. The slice position and the density and scaling of the
        vector glyphs can be configured either statically using a script or interactively using sliders in an active plot
        window.

        .. note::

            This display technique can be very computationally intensive so that the higher glyph densities may cause diminished
            interactivity.

.. automodule:: vcs.dv3d
   :members:

Jupyter Notebooks
^^^^^^^^^^^^^^^^^

.. include:: dv3d_notebooks.rst
