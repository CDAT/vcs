from genutil.colors import rgb2str, str2rgb  # noqa

def matplotlib2vcs(cmap, vcs_name=None):
    """
    Convert a matplotlib colormap to a vcs colormap
    Input can be either the actual matplotlib colormap or its name
    Optional second argument: vcs_name, name of the resulting vcs colormap

    :param cmap: A matplotlib colormap or string name of a matplotlib colormap
    :type cmap: :py:class:`str` , matplotlib.cm

    :param vcs_name: String to set the name of the generated VCS colormap
    :type vcs_name: :py:class:`str`

    :returns: A VCS colormap object
    :rtype: vcs.colormap.Cp
    """
    import vcs
    import matplotlib.cm
    import warnings
    if isinstance(cmap, (str, unicode)):
        try:
            cmap = matplotlib.cm.get_cmap(cmap)
        except:
            raise RuntimeError("Could not retrieve matplotlib colormap: %s" % cmap)

    if vcs_name is None:
        vcs_name = cmap.name
    i = 0
    vcs_name_final = vcs_name
    while vcs_name_final in vcs.listelements("colormap"):
        vcs_name_final = vcs_name + "_mpl_%.3i" % i
        i += 1
    if vcs_name_final != vcs_name:
        warnings.warn(
            "%s colormap name was already existing, your colormap name will be: %s" %
            (vcs_name, vcs_name_final))
    vcs_cmap = vcs.createcolormap(vcs_name_final)
    cmap_rgbs = cmap(range(0, cmap.N))
    for i in range(0, min(cmap.N, 256)):
        vcs_cmap.setcolorcell(i, *([int(x * 100) for x in cmap_rgbs[i][:4]]))

    return vcs_cmap


def loadmatplotlibcolormaps():
    """
    Convert all matplotlib colormaps to vcs colormaps
    """
    import matplotlib.pyplot as plt
    mpl_cmaps = sorted(m for m in plt.cm.datad if not m.endswith("_r"))
    for cmap in mpl_cmaps:
        matplotlib2vcs(cmap)
