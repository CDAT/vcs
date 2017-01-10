import vcs, inspect

# VCS objects to generate function references for. Some are modules, some are classes.
# Probably will need to add to this later when there's more documentation
objects = [vcs.boxfill.Gfb, vcs.Canvas.Canvas, vcs.colormap.Cp, vcs.fillarea.Tf, vcs.isofill.Gfi, vcs.isoline.Gi,
           vcs.line.Tl, vcs.marker.Tm, vcs.meshfill.Gfm, vcs.projection.Proj, vcs.taylor.Gtd, vcs.template.P,
           vcs.textcombined.Tc,vcs.textorientation.To, vcs.texttable.Tt, vcs.unified1D.G1d, vcs.vector.Gv,
           vcs.manageElements, vcs.queries, vcs.utils, vcs.animate_helper, vcs.dv3d, vcs.colors, vcs.displayplot.Dp,
           vcs.vcshelp, ]

# iterate through objects to find the functions of each, and write RST links for those out to
# API/functions/$MODULE_NAME.rst
for obj in objects:
    if inspect.isclass(obj):
        key = obj.__module__ + '.' + obj.__name__
        pred = inspect.ismethod
    else:
        key = obj.__name__
        pred = inspect.isfunction
    funcs = []
    tup_l = inspect.getmembers(obj, predicate=pred)
    for tup in tup_l:
        if not tup[0][0] == '_':
            funcs.append(':func:`' + key + '.' + tup[0] + '`\n\n')
    fname = key.split('.')[1]
    with open('functions/' + fname + ".rst", "w+") as f:
        f.write(fname + "\n")
        map(lambda x: f.write('-'), range(len(fname)))
        f.write("\n\n")
        f.writelines(funcs)
