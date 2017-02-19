import vcs
print "imported"
x=vcs.init(bg=True)
print "init pass"
x.open()
print "open ok"
x.plot([1,2,3,4],bg=True)
