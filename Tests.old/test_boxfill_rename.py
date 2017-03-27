import vcs
import cdms2

# download sample data, if it isn't already there
vcs.download_sample_data_files()

# make a slab, make a boxfill, get default boxfill
f = cdms2.open(vcs.sample_data + '/clt.nc')
u = f('u')
b = vcs.createboxfill()
a = vcs.init()
r = a.getboxfill()

# rename() should rename the created boxfill
b_name = b.name
b.rename('foo')
assert(b_name != b.name)

# rename() should not rename the default object
r.rename('bar')
assert(r.name == 'default')

# both 'foo' and 'bar' boxfills should be get-able
a.getboxfill('foo')
a.getboxfill('bar')

# both boxfills should be plot-able
a.boxfill(b,u)
a.boxfill(r,u)