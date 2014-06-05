import vcs
import sys
import cdms2
import vtk
import os

interact = True
f=cdms2.open(os.path.join(sys.prefix,'sample_data','clt.nc'))
s=f("clt")
#f=cdms2.open(os.path.join(sys.prefix,"sample_data","sampleCurveGrid4.nc"))
#s=f("sample")
x=vcs.init()
tmpl = x.createtemplate()
#tmpl.data.x1=.001
#tmpl.data.x2=.5
#tmpl.data.y1=.0001
#tmpl.data.y2=.25
x.setcolormap("rainbow")
gm=x.createisoline()
gm=x.createboxfill()
gm=x.createisofill()
gm.datawc_x1=0
gm.datawc_x2=40
gm.datawc_y1=-40
gm.datawc_y2=40

gm.datawc_x1=-180.
gm.datawc_x2=180.
gm.datawc_y1=-90
gm.datawc_y2=90
bg = False
#bg = True
#levs = range(-20,135,10)
#gm.levels = levs
#gm.fillareacolors = vcs.getcolors(levs)
x.plot(s,tmpl,gm,bg=bg)
x.png("test")#,width=2000,height=1000)
if interact:
  try:
    x.interact()
  except: # ok using old vcs
    raw_input("Press enter")
else:
  raw_input("Press enter")
