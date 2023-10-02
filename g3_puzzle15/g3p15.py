import pygame as pg
import random as rdm
Blue=(50,50,200)
SQ=150
Border=SQ//10
W=3
H=4
class Piece():
  def __init__(self,screen,n=0,pos=[0,0],w=1,h=1):
    self.screen=screen
    self.n=n #number, only used here
    self.pos=pos
    self.w=w
    self.h=h
    self.t1=pg.font.SysFont('Arial',40).render(str(n),False,(200,200,200))
  def draw(self):
    ul=list(map(lambda x: x*SQ+Border,self.pos)) #upper left
    self.rect1=self.t1.get_rect(center=list(map(lambda x:x+SQ//2-Border//2,ul)))
    pg.draw.rect(self.screen,Blue, pg.Rect(ul[0],ul[1],self.w*SQ-Border, self.h*SQ-Border))
    screen.blit(self.t1,self.rect1) #text
class Empty(Piece):
  def __init__(self,screen,n=0,pos=[0,0],w=1,h=1):
    super().__init__(screen)
  def draw(self):
    pass #just do not draw the empty
class Board():
  def __init__(self,screen,w=W,h=H):
    self.w=w
    self.h=h
    self.screen=screen
    self.pl=[]
    poses=[]
    self.poses=[] #keep track of positions of the pieces, the index is the piece,
    for k1 in range(H):
      for k2 in range(W):
        poses.append([k2,k1])
    for k in range(H*W-1): #make the last piece Empty
      p1=poses.pop(rdm.randint(0,len(poses)-1))
      self.pl.append(Piece(screen,k,p1))
      self.poses.append(p1)
    p1=poses.pop()
    self.pl.append(Empty(screen,H*W-1,p1))
    self.poses.append(p1)
  def draw(self):
    for p in self.pl:
      p.draw()
  def move(self,d):
    if d==0: #go up, (empty goes down)
      if self.poses[-1][1]!=H-1: #the empty is not on the bottom
        self.poses[-1][1]+=1
        #find the piece which have the same pos as empty, make it go up
        #find the index of the piece, which have the same pos as the (changed) empty
        i=self.poses.index(self.poses[-1])
        self.poses[i][1]-=1
        # self.pl[-1].move(1)
        # self.pl[i].move(0)
    if d==1:
      if self.poses[-1][1]!=0:
        self.poses[-1][1]-=1
        i=self.poses.index(self.poses[-1])
        self.poses[i][1]+=1
    if d==2:
      if self.poses[-1][0]!=W-1:
        self.poses[-1][0]+=1
        i=self.poses.index(self.poses[-1])
        self.poses[i][0]-=1
    if d==3:
      if self.poses[-1][0]!=0:
        self.poses[-1][0]-=1
        i=self.poses.index(self.poses[-1])
        self.poses[i][0]+=1
go=True
clock = pg.time.Clock()
pg.init()
pg.display.set_caption('Puzzle 15')
screen = pg.display.set_mode((W*SQ+Border,H*SQ+Border))
b1=Board(screen)
while go:
  clock.tick(40)
  screen.fill('#ffcc00')
  for e in pg.event.get():
    if e.type == pg.QUIT: go = False
    if e.type == pg.KEYDOWN:
      if e.key== pg.K_UP: b1.move(0)
      elif e.key== pg.K_DOWN: b1.move(1)
      elif e.key== pg.K_LEFT: b1.move(2)
      elif e.key== pg.K_RIGHT: b1.move(3)
  b1.draw()
  pg.display.flip()