import vcs
import vtk
import numpy

## This module contains some convenience function from vcs2vtk

## Continents first
def continentsVCS2VTK(fnm):
  """ This converts vcs continents files to vtkpolydata
  Author: Charles Doutriaux
  Input: vcs continent file name
  """
  poly =vtk.vtkPolyData()
  cells = vtk.vtkCellArray()
  pts = vtk.vtkPoints()
  f=open(fnm)
  ln=f.readline()
  while ln.strip().split()!=["-99","-99"]:
    # Many lines, need to know number of points
    N = int(ln.split()[0])
    # Now create and store these points
    n=0
    npts = pts.GetNumberOfPoints()
    while n<N:
        ln=f.readline()
        while len(ln)>2:
          l,L=float(ln[:8]),float(ln[8:16])
          pts.InsertNextPoint(L,l,0.0001)
          ln=ln[16:]
          n+=2
    ln = vtk.vtkPolyLine()
    ln.GetPointIds().SetNumberOfIds(N/2)
    for i in range(N/2): ln.GetPointIds().SetId(i,i+npts)
    cells.InsertNextCell(ln)
    ln=f.readline()
  poly.SetPoints(pts)
  poly.SetLines(cells)
  return poly


#Geo projection
def project(pts,projection):
  if projection.type=="linear":
    return pts
  geo = vtk.vtkGeoTransform()
  ps = vtk.vtkGeoProjection()
  pd = vtk.vtkGeoProjection()
  projName = projection.type
  pd.SetName(projName)
  geo.SetSourceProjection(ps)
  geo.SetDestinationProjection(pd)
  geopts = vtk.vtkPoints()
  geo.TransformPoints(pts,geopts)
  return geopts


#Vtk dump
dumps=0
def dump2VTK(obj,fnm=None):
  global dumps
  if fnm is None:
    fnm="foo%.3i.vtk" % dumps
    dumps+=1
  dsw = vtk.vtkDataSetWriter()
  dsw.SetFileName(fnm)
  try:
    dsw.SetInputData(obj)
  except:
    dsw.SetInputConnection(obj.GetOutputPort())

  dsw.Write()


#Wrapping around
def doWrap(Act,gm,wrap=[0.,360]):
  Mapper = Act.GetMapper()
  data = Mapper.GetInput()
  xmn=min(gm.datawc_x1,gm.datawc_x2)
  xmx=max(gm.datawc_x1,gm.datawc_x2)
  if numpy.allclose(xmn,1.e20) or numpy.allclose(xmx,1.e20):
    xmx = abs(wrap[1])
    xmn = -wrap[1]
  ymn=min(gm.datawc_y1,gm.datawc_y2)
  ymx=max(gm.datawc_y1,gm.datawc_y2)
  if numpy.allclose(ymn,1.e20) or numpy.allclose(ymx,1.e20):
    ymx = abs(wrap[0])
    ymn = -wrap[0]
  
  ## Prepare MultiBlock and puts in oriinal data
  appendFilter =vtk.vtkAppendPolyData()
  appendFilter.AddInputData(data)
  ## X axis wrappping
  Amn,Amx = Act.GetXRange()
  if wrap[1]!=0.:
    i=0
    while Amn>xmn:
      i+=1
      Amn-=wrap[1]
      Tpf = vtk.vtkTransformPolyDataFilter()
      Tpf.SetInputData(data)
      T=vtk.vtkTransform()
      T.Translate(-i*wrap[1],0,0)
      Tpf.SetTransform(T)
      Tpf.Update()
      appendFilter.AddInputData(Tpf.GetOutput())
    i=0
    while Amx<xmx:
      i+=1
      Amx+=wrap[1]
      Tpf = vtk.vtkTransformPolyDataFilter()
      Tpf.SetInputData(data)
      T = vtk.vtkTransform()
      T.Translate(i*wrap[1],0,0)
      Tpf.SetTransform(T)
      Tpf.Update()
      appendFilter.AddInputData(Tpf.GetOutput())

  # Y axis wrapping
  Amn,Amx = Act.GetYRange()
  if wrap[0]!=0.:
    i=0
    while Amn>ymn:
      i+=1
      Amn-=wrap[0]
      Tpf = vtk.vtkTransformPolyDataFilter()
      Tpf.SetInputData(data)
      T = vtk.vtkTransform()
      T.Translate(0,i*wrap[0],0)
      Tpf.SetTransform(T)
      Tpf.Update()
      appendFilter.AddInputData(Tpf.GetOutput())
    i=0
    while Amx<ymx:
      i+=1
      Amx+=wrap[0]
      Tpf = vtk.vtkTransformPolyDataFilter()
      Tpf.SetInputData(data)
      T = vtk.vtkTransform()
      T.Translate(0,-i*wrap[0],0)
      Tpf.SetTransform(T)
      Tpf.Update()
      appendFilter.AddInputData(Tpf.GetOutput())
  appendFilter.Update()
  Actor = vtk.vtkActor()
  Actor.SetProperty(Act.GetProperty())
  #Mapper2 = vtk.vtkDataSetMapper()
  #Mapper2 = vtk.vtkCompositePolyDataMapper()
  Mapper2 = vtk.vtkPolyDataMapper()
  Mapper2.SetInputData(doClip(appendFilter.GetOutput(),xmn,xmx,ymn,ymx))
  Mapper2.SetLookupTable(Mapper.GetLookupTable())
  Mapper2.SetScalarRange(Mapper.GetScalarRange())
  Actor.SetMapper(Mapper2)
  return Actor

def doClip(data,xmin,xmax,ymin,ymax):
  if xmin!=xmax:
    xminClip = doClip1(data,xmin,1,0)
    xfullClip = doClip1(xminClip,xmax,-1,0)
  else:
    xfullClip = data
  if ymin!=ymax:
    yminClip  = doClip1(xfullClip,ymin,1,1)
    xyClip  = doClip1(yminClip,ymax,-1,1)
  else:
    xyClip = xfullClip
  return xyClip

def doClip1(data,value,normal,axis=0):
    # We have the actor, do clipping
    clpf = vtk.vtkPlane()
    if axis == 0:
      clpf.SetOrigin(value,0,0)
      clpf.SetNormal(normal,0,0)
    else:
      clpf.SetOrigin(0,value,0)
      clpf.SetNormal(0,normal,0)
    clp = vtk.vtkClipPolyData()
    clp.SetClipFunction(clpf)
    clp.SetInputData(data)
    clp.Update()
    return clp.GetOutput()

def prepTextProperty(p,to="default",tt="default",cmap="default"):
  if isinstance(to,str):
    to = vcs.elements["textorientation"][to]
  if isinstance(tt,str):
    tt = vcs.elements["texttable"][tt]

  if isinstance(cmap,str):
    cmap = vcs.elements["colormap"][cmap]
  c=cmap.index[tt.color]
  p.SetColor([C/100. for C in c])
  if to.halign=="left":
    p.SetJustificationToLeft()
  elif to.halign =="right":
    p.SetJustificationToRight()
  elif to.halign=="center":
    p.SetJustificationToCentered()

  if to.valign=='top':
    p.SetVerticalJustificationToTop()
  elif to.valign=='half':
    p.SetVerticalJustificationToCentered()
  elif to.valign=='bottom':
    p.SetVerticalJustificationToBottom()
  elif to.valign=='cap':
    warnings.warn("VTK does not support 'cap' align, using 'top'")
    p.SetVerticalJustificationToTop()
  elif to.valign=='base':
    warnings.warn("VTK does not support 'base' align, using 'bottom'")
    p.SetVerticalJustificationToBottom()
  p.SetOrientation(-to.angle)
  p.SetFontFamily(vtk.VTK_FONT_FILE)
  p.SetFontFile(vcs.elements["font"][vcs.elements["fontNumber"][tt.font]])

def genTextActor(renderer,string=None,x=None,y=None,to='default',tt='default',cmap='default'):
  if isinstance(to,str):
    to = vcs.elements["textorientation"][to]
  if isinstance(tt,str):
    tt = vcs.elements["texttable"][tt]
  if string is None:
    string = tt.string
  print "STRING SHOULD BE:",string
  if x is None:
    x = tt.x
  if y is None:
    y = tt.y
  if x is None or y is None or string in [['',],[]]:
    return
  
  n = max(len(x),len(y),len(string))
  for a in [x,y,string]:
    while len(a)<n:
      a.append(a[-1])

  for i in range(n):
    t = vtk.vtkTextActor()
    p=t.GetTextProperty()
    prepTextProperty(p,to,tt,cmap)
    t.SetInput(string[i])
    X,Y = world2Renderer(renderer,x[i],y[i],tt.viewport,tt.worldcoordinate)
    t.SetPosition(X,Y)
    renderer.AddActor(t)
  return t

def getRendererCorners(Renderer,vp=[0.,1.,0.,1.]):
  sz = Renderer.GetSize()
  origin = Renderer.GetOrigin()
  opposite = origin[0]+sz[0]*vp[1],origin[1]+sz[1]*vp[3]
  origin2 = origin[0]+sz[0]*vp[0],origin[1]+sz[1]*vp[2]
  print "Render origin,opposite:",origin2,opposite
  return origin2,opposite

def world2Renderer(ren,x,y,vp=[0.,1.,0.,1.],wc=[0.,1.,0.,1.]):
  origin,opposite = getRendererCorners(ren,vp)
  X = origin[0]+ (opposite[0]-origin[0] )*(x-wc[0])/(wc[1]-wc[0])
  Y = origin[1]+ (opposite[1]-origin[1] )*(y-wc[2])/(wc[3]-wc[2])
  print "Accounting for vp/wc",x,y,"in Render are:",X,Y
  return X,Y

def R2World(ren,x,y):
  """Converts renderer's x/y to WorldCoordinate for a given Renderer"""
  #print "ok X and Y:",x,y
  ren.SetDisplayPoint(x,y,0)
  ren.DisplayToWorld()
  ren.ViewToWorld()
  wp = ren.GetWorldPoint()
  return wp

def vtkWorld2Renderer(ren,x,y):
  ren.SetWorldPoint(x,y,0,0)
  ren.WorldToDisplay()
  renpts = ren.GetDisplayPoint()
  print "World:",x,y,"is:",renpts
  return renpts

def fitToViewport(Actor,Renderer,vp):
  ## Data range in World Coordinates
  Xrg = Actor.GetXRange()
  Yrg = Actor.GetYRange()
  XcenterData = (Xrg[1]+Xrg[0])/2.
  YcenterData = (Yrg[1]+Yrg[0])/2.

  ## Where they are in term of pixels
  oll = vtkWorld2Renderer(Renderer,Xrg[0],Yrg[0])
  our = vtkWorld2Renderer(Renderer,Xrg[1],Yrg[1])

  # Where they should be in term of pixel
  ll = world2Renderer(Renderer,Xrg[0],Yrg[0],
      vp,
      [Xrg[0],Xrg[1],Yrg[0],Yrg[1]])
  ur = world2Renderer(Renderer,Xrg[1],Yrg[1],
      vp,
      [Xrg[0],Xrg[1],Yrg[0],Yrg[1]])
  
  # How much does it needs to be scaled by?
  xScale = (ur[0]-ll[0])/(our[0]-oll[0])
  yScale = (ur[1]-ll[1])/(our[1]-oll[1])

  #World coordinates of where they need to be
  LL = R2World(Renderer,*ll)
  UR = R2World(Renderer, *ur)
  print "LL,UR:",LL,UR
  #xScale = (ur[0]-ll[0])/(Xrg[1]-Xrg[0])
  #yScale = (ur[1]-ll[1])/(Yrg[1]-Yrg[0])
  dX = LL[0]-Xrg[0]
  dY = LL[1]-Yrg[0]
  T = vtk.vtkTransform()
  T.Translate(LL[0]*(1.-xScale),LL[1]*(1.-yScale),0)
  T.Scale(xScale,yScale,1)
  T.Translate(dX,dY,0)
  print "TRANSLATE:",-XcenterData,-YcenterData
  #T.Translate(-XcenterData,-YcenterData,0)
  Actor.SetUserTransform(T)
  return Actor

