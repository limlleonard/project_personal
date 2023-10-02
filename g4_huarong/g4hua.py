import pygame as pg
import random as rdm
#from g2five import Button
Blue=(50,50,200)
SQ=100
Border=SQ//10
W=4
H=5
def swipe(p1,p2):
  if abs(p1[0]-p2[0])<abs(p1[1]-p2[1]): #up or down
    if p2[1]<p1[1]: return 0
    else: return 1
  else:
    if p2[0]<p1[0]: return 2
    else: return 3
class Piece():
  def __init__(self,screen,pos=[0,0],w=1,h=1,n=0):
    self.screen=screen
    self.n=n #number, only used here
    self.pos=pos
    self.w=w
    self.h=h
    self.t1=pg.font.SysFont('Arial',30).render('',False,(200,200,200))
  def draw(self):
    ul=list(map(lambda x: x*SQ+Border,self.pos)) #upper left
    self.rect1=self.t1.get_rect(center=list(map(lambda x:x+SQ//2-Border//2,ul)))
    pg.draw.rect(self.screen,Blue, pg.Rect(ul[0],ul[1],self.w*SQ-Border, self.h*SQ-Border),border_radius=15)
    screen.blit(self.t1,self.rect1) #text
  def inme(self,pos):
    if self.pos==pos: return True
    else:
      x,y=self.pos
      x1,y1=pos
      if self.w==2 and x+1==x1 and y==y1: return True
      if self.h==2 and y+1==y1 and x==x1: return True
      if self.w==self.h==2 and x+1==x1 and y+1==y1: return True
  def free(self,emp,d):
    x,y=self.pos
    if d==0 and [x,y-1] in emp:
      self.pos[1]-=1
      emp[emp.index([x,y-1])][1]+=1
    if d==1 and [x,y+1] in emp:
      self.pos[1]+=1
      emp[emp.index([x,y+1])][1]-=1
    if d==2 and [x-1,y] in emp:
      self.pos[0]-=1
      emp[emp.index([x-1,y])][0]+=1
    if d==3 and [x+1,y] in emp:
      self.pos[0]+=1
      emp[emp.index([x+1,y])][0]-=1
class Thin(Piece):
  def __init__(self,screen,pos=[0,0]):
    Piece.__init__(self,screen,pos,w=1,h=2)
  def free(self,emp,d):
    x,y=self.pos
    if d==0 and [x,y-1] in emp:
      self.pos[1]-=1
      emp[emp.index([x,y-1])][1]+=2
    if d==1 and [x,y+2] in emp:
      self.pos[1]+=1
      emp[emp.index([x,y+2])][1]-=2
    if d==2 and [x-1,y] in emp and [x-1,y+1] in emp:
      self.pos[0]-=1
      for p in emp: p[0]+=1
    if d==3 and [x+1,y] in emp and [x+1,y+1] in emp:
      self.pos[0]+=1
      for p in emp: p[0]-=1
class Fat(Piece):
  def __init__(self,screen,pos=[0,0]):
    Piece.__init__(self,screen,pos,w=2,h=1)
  def free(self,emp,d):
    x,y=self.pos
    if d==0 and [x,y-1] in emp and [x+1,y-1] in emp:
      self.pos[1]-=1 #both fields up are free
      for p in emp: p[1]+=1
    if d==1 and [x,y+1] in emp and [x+1,y+1] in emp:
      self.pos[1]+=1
      for p in emp: p[1]-=1
    if d==2 and [x-1,y] in emp:
      self.pos[0]-=1
      emp[emp.index([x-1,y])][0]+=2
    if d==3 and [x+2,y] in emp:
      self.pos[0]+=1
      emp[emp.index([x+2,y])][0]-=2
class Cc(Piece):
  def __init__(self,screen,pos=[0,0]):
    Piece.__init__(self,screen,pos,w=2,h=2)
  def draw(self):
    ul=list(map(lambda x: x*SQ+Border,self.pos)) #upper left
    pg.draw.rect(self.screen,(200,20,20), pg.Rect(ul[0],ul[1],self.w*SQ-Border, self.h*SQ-Border),border_radius=15)
  def free(self,emp,d):
    x,y=self.pos
    if d==0 and [x,y-1] in emp and [x+1,y-1] in emp:
      self.pos[1]-=1 #both fields up are free
      for p in emp: p[1]+=2
    if d==1 and [x,y+2] in emp and [x+1,y+2] in emp:
      self.pos[1]+=1
      for p in emp: p[1]-=2
    if d==2 and [x-1,y] in emp and [x-1,y+1] in emp:
      self.pos[0]-=1
      for p in emp: p[0]+=2
    if d==3 and [x+2,y] in emp and [x+2,y+1] in emp:
      self.pos[0]+=1
      for p in emp: p[0]-=2
class Board():
  def __init__(self,screen,w=W,h=H):
    self.w=w
    self.h=h
    self.screen=screen
  def start(self):
    dstart={'l':[[0,0],[3,0],[0,2],[3,2]], 'w':[[1,2]], 'cc':[1,0], 'zu':[[1,3],[2,3],[1,4],[2,4]]}
    lcc=[Cc(screen,dstart['cc'])]
    lthin=[Thin(screen,p) for p in dstart['l']]
    lfat=[Fat(screen,p) for p in dstart['w']]
    lzu=[Piece(screen,p) for p in dstart['zu']]
    self.lemp=[[0,4],[3,4]]
    self.ll=[lcc,lthin,lfat,lzu]
  def draw(self):
    for l in self.ll:
      for p in l:
        p.draw()
go=True
clock = pg.time.Clock()
pg.init()
pg.display.set_caption('Huarondao(Klotski)')
screen = pg.display.set_mode((W*SQ+Border,H*SQ+Border))
b1=Board(screen)
b1.start()
while go:
  clock.tick(40)
  screen.fill('#ffcc00')
  for e in pg.event.get():
    if e.type == pg.QUIT: go = False
    if e.type==pg.MOUSEBUTTONDOWN and e.button==1:
      posd=e.pos
    if e.type==pg.MOUSEBUTTONUP:
      pos=[p//(SQ+Border) for p in posd]
      for l in b1.ll:
        for p in l:
          if p.inme(pos):
            p.free(b1.lemp,swipe(posd,e.pos))
  if b1.ll[0][0].pos==[1,3]: #cc arrive
    pass
  b1.draw()
  pg.draw.rect(screen,(200,20,20), pg.Rect(SQ,5*SQ,2*SQ+Border, Border))
  pg.display.flip()