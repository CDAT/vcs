import vcs


canvas = vcs.init(bg=True, geometry=(800,600))
canvas.drawlogooff()  # Turn off logo

# vp and wc definitions
vp = [.2,.8, .2, .8]  # 20 to 80% of canvas in both direction
wc = [-180,180,-90,90]  # Whole globe


def text(string, x=.5, y=.5, halign="center", valign="half", height=10, color="black"):
    # First plot coordinate of canvas
    txt = vcs.createtext()
    txt.string = string
    txt.halign = halign
    txt.valign = valign
    txt.x = x
    txt.y = y
    txt.height = height
    txt.color = color
    txt.priority = 2  # To ensure it shows on top of fillarea and line objects
    canvas.plot(txt)

def straightLine(coord, direction="horizontal", color="grey", type="dot"):
    ln = vcs.createline()
    if direction[0].lower() == "h":
        ln.x = [0.001, .999]
        ln.y = [coord, coord]
    else:
        ln.x = [coord, coord]
        ln.y = [0., 1.]
    ln.type= type
    ln.color = [color]
    canvas.plot(ln)

# draw line around the cnavas
ln = vcs.createline()
ln.width=6
ln.x=[0,1,1,0,0]
ln.y=[0,0,1,1,0]
canvas.plot(ln)


# Viewport coordinates
text("[0,0] [Canvas Bottom/Left Viewport Origin]",0.01,0.01,"left","bottom")
text("[Canvas Top/Right Viewport Origin] [1, 1]",0.99,.99,"right","top")

# create the "viewport" area section
fa = vcs.createfillarea()
fa.x = [vp[0], vp[1], vp[1], vp[0]]
fa.y = [vp[2], vp[2], vp[3], vp[3]]
fa.color= "lightgrey"
canvas.plot(fa)

# Viewport Coordinates
text("[.2,.2] [Object Bottom/Left Viewport]",0.2,0.2,"right","top")
text("[Object Top/Right Viewport] [.8, .8]",0.8,.8,"left","bottom")
# World Coordinates
text("(-180., -90.) [Object Bottom/Left World]",0.2,0.2,"left", "bottom", color="red")
text("[Object Top/Right World] (180., 90)",0.8,.8,"right","top", color="red")

# extends view port area
straightLine(.2,"horizontal")
straightLine(.8,"horizontal")
straightLine(.2,"vertical")
straightLine(.8,"vertical")

# Draw a fillarea that extends beyond the viewport
fa = vcs.createfillarea()
fa.viewport = vp
fa.worldcoordinate = wc
fa.x = [150., 200., 200., 150.]
fa.y = [20., 20., 50., 50.]
fa.color="blue"
canvas.plot(fa)

#Draw the part cropped
ln = vcs.createline()
ln.color = ["blue"]
ln.type = "dot"
x1 = vp[1]
x2 = vp[0] + (fa.x[0][1]-wc[0])/(wc[1]-wc[0])*(vp[1]-vp[0])
y1 = vp[2] + (fa.y[0][0]-wc[2])/(wc[3]-wc[2])*(vp[3]-vp[2])
y2 = vp[2] + (fa.y[0][3]-wc[2])/(wc[3]-wc[2])*(vp[3]-vp[2])
ln.y = [y1, y1, y2, y2]
ln.x = [x1, x2, x2, x1]
canvas.plot(ln)

text("Object (Visible) ",vp[1],y2,halign="right",valign="bottom",color="blue",height=13)
text(" Object (Cropped)",vp[1],y2,halign="left",valign="bottom",color="blue",height=13)
canvas.png("vp_and_wc")

