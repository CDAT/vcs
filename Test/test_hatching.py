# Adapted for numpy/ma/cdms2 by convertcdms.py
import vcs
import support
bg = support.bg
x = vcs.init()

f = x.createfillarea('test')
f.x = [.2, .2, .8, .8]
f.y = [.2, .8, .8, .2]
f.color = 243
f.style = 'hatch'

x.plot(f, bg=bg)
support.check_plot(x)
