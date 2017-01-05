import vcs, inspect

objects = [
    vcs.boxfill.Gfb,
    vcs.Canvas.Canvas,
    vcs.colormap.Cp,
    vcs.fillarea.Tf,
    vcs.isofill.Gfi,
    vcs.isoline.Gi,
    vcs.line.Tl,
    vcs.marker.Tm,
    vcs.meshfill.Gfm,
    vcs.projection.Proj,
    vcs.taylor.Gtd,
    vcs.template.P,
    vcs.textcombined.Tc,
    vcs.textorientation.To,
    vcs.texttable.Tt,
    vcs.unified1D.G1d,
    vcs.vector.Gv,
    vcs.manageElements,
    vcs.queries,
    vcs.utils
]

obj_d = {}
for obj in objects:
    if inspect.isclass(obj):
        key = obj.__module__ + '.' + obj.__name__
        pred = inspect.ismethod
    else:
        key = obj.__name__
        pred = inspect.isfunction
    obj_d[key] = []
    tup_l = inspect.getmembers(obj, predicate=pred)
    for tup in tup_l:
        if not tup[0][0] == '_':
            obj_d[key].append(':func:`' + key + '.' + tup[0] + '`\n\n')

mod_d = {}
for key in obj_d:
    fname = key.split('.')[1]
    with open('functions/' + fname + ".rst", "w+") as f:
        f.write(fname + "\n")
        map(lambda x: f.write('-'), range(len(fname)))
        f.write("\n\n")
        f.writelines(obj_d[key])
