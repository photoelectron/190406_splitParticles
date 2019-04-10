fc = 2
wd = 1080/fc; ht = 1080/fc

probdel = 1/10.*0
probinv = 1/5.*0

inip = 4
splitp = inip
angle = TWO_PI/splitp
toff = angle/8
maxL = wd/4.
lifeDiv = 2
maxiters = 8
maxp = splitp**maxiters
hini = .275
hinc = 0.025
alp = 0.25

def settings():
    size(wd,ht)

def setup():
    global P
    colorMode(HSB,1.)
    background(0)
    P = syst(PVector(width/2,height/2),PVector(0,-1),
             inip,splitp,angle,maxL,lifeDiv)

def draw():
    P.update()
    # print len(P.p)

#######################
class particle():
    def __init__(self,pos,vel,h,life):
        self.pos = pos
        self.vel = vel
        self.h = h
        self.ltot = life
        self.life = life
        self.vis = 1
    
    def show(self):
        stroke(self.h,1,1,alp*self.vis)
        point(self.pos.x,self.pos.y)
    
    def update(self):
        self.pos.add(self.vel)
        self.life -= 1

class syst():
    def __init__(self,pos,vel,ip,np,theta,life,lsplit):
        self.theta = theta
        self.np = np
        self.lsplit = lsplit
        self.p = []
        for i in xrange(ip):
            po = particle(pos.copy(),vel.copy(),hini,life)
            po.vel.rotate(theta*i+toff)
            self.p.append(po)
    
    def update(self):
        newp = []
        for i in xrange(len(self.p)):
            self.p[i].update()
            self.p[i].show()
            if self.p[i].life <= 0:
                if self.p[i].ltot <= 1:
                    continue
                for j in xrange(self.np):
                    r = random(1.)
                    if r < probdel:
                        po = self.p[i]
                        po.ltot /= self.lsplit
                        po.life = po.ltot
                        newp.append(po)
                        continue
                    po = particle(self.p[i].pos.copy(),
                                  self.p[i].vel.copy(),
                                  self.p[i].h+hinc,
                                  self.p[i].ltot/self.lsplit)
                    po.vel.rotate(self.theta*j+toff)
                    r = random(1.)
                    if r < map(po.ltot,1,maxL,probinv,probinv*3):
                        po.vis = 0
                    newp.append(po)
            else:
                newp.append(self.p[i])
        if len(newp) >= maxp:
            print "Max particles; sim ended."
            self.p = []
            noLoop()
        elif len(newp) == 0:
            print "No more particles."
            self.p = []
            noLoop()
        self.p = newp[:]
