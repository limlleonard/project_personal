import pygame as pg
import random
import numpy as np
import time
R=13 #row
r=20 #radius
F=5
B=(0,0,0)
W=(255,255,255)
G=(120,120,120,120)
Trans=(120,120,120,10)
SQ=70
inf=10**6
def dicts():
#make a dictionary of all quads, in which order or which pos are in the quad, doesn't matter, just save how many red or yellow are in it
#a pos dictionary, the value is a tuple, which shows this pos is in which quads
  dictq={}
  dictp={}
  c1=0
  for y in range(R): #horizontal
    for x in range(R-F+1):
      for i in range(F):
        if not (x+i,y) in dictp: dictp[(x+i,y)]=(c1,)
        else: dictp[(x+i,y)]+=(c1,)
      dictq[c1]=[0,0]
      c1+=1
  for y in range(R-F+1):
    for x in range(R):
      for i in range(F): dictp[(x,y+i)]+=(c1,)
    #after horizontal, all pos should be already in dictp, so you don't need to check, if it exist
      dictq[c1]=[0,0]
      c1+=1
  for y in range(R-F+1):
    for x in range(R-F+1):
      for i in range(F): dictp[(x+i,y+i)]+=(c1,)
      dictq[c1]=[0,0]
      c1+=1
  for y in range(R-F+1):
    for x in range(F-1,R):
      for i in range(F): dictp[(x-i,y+i)]+=(c1,)
      dictq[c1]=[0,0]
      c1+=1
  return dictp, dictq
class Board():
  def __init__(self,screen):
    self.l1=np.zeros((R,R),dtype=int)
    self.dictp,self.dictq=dicts()
    self.vm=set() #valid moves
    self.counter=1
    for k1 in range(R):
      for k2 in range(R): self.vm.add((k1,k2))
    self.pl=[] #piece list
    for k1 in range(R):
      for k2 in range(R):
        self.pl.append(Piece(screen,(k1*SQ+SQ//2,k2*SQ+SQ//2)))
  def move(self,pos,p):
    win=False
    c=1 if p else 2
    self.l1[pos[0]][pos[1]]=c
    self.vm.remove(pos) #the change of valid move should be inside of move and back, because when minimax is calculated, the 2. fantacy move should not be in the same place. Piece should only be played, when it really make the move
    for q in self.dictp[pos]:
      self.dictq[q][c-1]+=1
      if self.dictq[q][c-1]==5: win=True
    return win
  def back(self,pos,p):
    c=1 if p else 2
    self.l1[pos[0]][pos[1]]=0
    self.vm.add(pos)
    for q in self.dictp[pos]:
      self.dictq[q][c-1]-=1
  def score(self):
    s=0
    for v in self.dictq.values():
      if v[0]>0 and v[1]>0: continue #if there are two colors, this quad is not useful anyway
      s+=10**v[0]-10**v[1] # calculate the current score of the field
    return s
  def reset(self):
    self.l1=np.zeros((R,R),dtype=int)
    for q in self.dictq:
      self.dictq[q]=[0,0]
  def winc(self):
    tie=True
    for v in self.dictq.values():
      if v[0]==F: return 1
      elif v[1]==F: return 2
      if v[0]==0 or v[1]==0: tie=False
    if tie: return 3
    return 0
class Robot():
  def __init__(self,b,p,d=1):
    self.b=b
    self.p=p # player
    self.d=d
    self.mmc=np.zeros(d+1, dtype = int)
  def minimax1(self,p,d=5,sub=False):
    scores=[] #tuple, 1 score, 2 where put the piece
    for pos in self.b.vm:
      self.b.move(pos,p)
      if d==0:
        scores.append((self.b.score(),pos))
      else:
        scores.append((self.minimax(not p, d-1)[0],pos))
      self.b.back(pos,p)
    scores.sort(reverse=p)
    return scores[0]
  def minimax(self,p,d,win,alpha=-inf,beta=inf):
    self.mmc[d]+=1
    #scores=[] #tuple, 1 score, 2 where put the piece
    if win: return -inf*2-d*100 if p else inf*2+d*100 #the move was made by the last player, in the minimax, the player color was reversed, so this reverse it back
    if d==0: return self.b.score()
    value = -inf if p else inf
    for pos in self.b.vm:
      if self.b.counter<8 and abs(pos[0]-R//2)+abs(pos[1]-R//2)>5:
        continue #the first 10 move only consider the area of square 10
      win=self.b.move(pos,p)
      score=self.minimax(not p, d-1,win,alpha,beta)
      self.b.back(pos,p)
      if p:
        value = max(value, score)
        alpha = max(value, alpha)  
      else:
        value = min(value, score)
        beta = min(value, beta)
      if alpha >= beta:
        break
    return value
  def move(self):
    scores=[] #tuple, 1 score, 2 where put the piece
    for pos in self.b.vm:
      if self.b.counter<8 and abs(pos[0]-R//2)+abs(pos[1]-R//2)>5:
        continue #the first 10 move only consider the area of square 10
      win=self.b.move(pos,self.p)
      # with concurrent.futures.ProcessPoolExecutor() as executor:
      #   f1=executor.submit(self.minimax, not self.p,0)
      # score=f1.result()
      score=self.minimax(not self.p,self.d,win,-inf,inf)
      scores.append((score,pos))
      self.b.back(pos,self.p)
    scores.sort(reverse=self.p)
    print(self.mmc)
    self.mmc=np.zeros(self.d+1,dtype=int)
    return scores
class Game():
  def __init__(self,screen):
    #buttons are needed anyway, pieces should be created each time start
    self.stage=1
    self.bl=[]
    self.screen=screen
    self.scores=[]
    tl=['human vs human','human vs robot','robot vs human','robot vs robot']
    for k1 in range(1,5):
      self.bl.append(Button(screen,k1,(SQ*R//2, SQ*R*k1//5),tl[k1-1]))
    b1=Button(screen,1,(SQ*R//4, SQ*R-SQ),'Again')
    b2=Button(screen,2,(SQ*R*3//4, SQ*R-SQ),'Quit')
    self.bl2=[b1,b2]
    #pl[3*R+4].play(True,4)
    self.p1v=self.p2v=self.turn=True #valid move
    m=R//2
    self.open1=set() #all possible opening 
    self.open2=set()
    for x in range(3):
      for y in range(-2,3): self.open1.add((R//2+x,R//2+y))
    self.open1.remove((R//2,R//2))
    self.open1.remove((R//2,R//2-1))
    for x in range(-2,3): 
      for y in range(-2,x+1): self.open2.add((R//2+x,R//2+y))
    self.open2.remove((R//2,R//2))
    self.open2.remove((R//2+1,R//2-1))
  def start(self,a1):
    self.b=Board(self.screen)
    self.turn=True
    pd=[(False,False),(False,True),(True,False),(True,True)]
    self.ps=pd[a1-1] #players if it is robot
    if a1==2:
      self.p1=Robot(self.b,False)
    elif a1==3:
      self.p1=Robot(self.b,True)
    elif a1==4:
      self.p1=Robot(self.b,True)
      self.p2=Robot(self.b,False)
    self.move((R//2,R//2))
    if bool(random.getrandbits(1)):
      self.move((R//2,R//2-1))
      self.move(random.sample(self.open1,1)[0])
    else:
      self.move((R//2+1,R//2-1))
      self.move(random.sample(self.open2,1)[0])
    if a1==2: self.move() 
    # if robot plays the 4. move
  def move(self,pos=False):
    #robot can only move if nothing is passed
    if not pos:
      if self.turn and self.ps[0] or not self.turn and self.ps[1]:
        #if p1 is in turn and it is a robot or
        t1=time.time()
        self.scores=self.p1.move()
        t2=time.time()
        print(round(t2-t1))
        pos=self.scores[0][1]
    if pos:
      if self.b.l1[pos]!=0: self.p1v=False
      else:
        self.b.move(pos,self.turn)
        self.b.pl[pos[0]*R+pos[1]].play(self.turn,self.b.counter)
        #piece list play, this should not be in move, because it could be moved back
        self.b.counter+=1
        self.turn=not self.turn # only switch, if make a valid move
      wc1=self.b.winc()
      if wc1:
        print(wc1)
        self.stage=3
  def draw(self):
    bspot=[(R*SQ//2, R*SQ//2),(3*SQ+SQ//2, 3*SQ+SQ//2),((R-3)*SQ-SQ//2,(R-3)*SQ-SQ//2), (3*SQ+SQ//2, (R-3)*SQ-SQ//2),((R-3)*SQ-SQ//2,3*SQ+SQ//2)]
    if self.stage==1:
      for b1 in self.bl:
        b1.draw()
    if self.stage>1:
      for k in range(R):
        guide1=pg.font.SysFont('Arial',22).render(str(k),False,(0,0,0))
        rect1=guide1.get_rect(center=(SQ//4,SQ*k+SQ//2))
        rect2=guide1.get_rect(center=(SQ*k+SQ//2,SQ//4))
        self.screen.blit(guide1,rect1)
        self.screen.blit(guide1,rect2)
      for bs in bspot:
        pg.draw.circle(self.screen,B, bs,5)
      for x in range(R): #Brett
        for y in range(R):
          pg.draw.line(self.screen,(0,0,0),(x*SQ+SQ//2,y*SQ+SQ//2),(R*SQ-SQ//2,y*SQ+SQ//2))
          pg.draw.line(self.screen,(0,0,0),(x*SQ+SQ//2,y*SQ+SQ//2),(x*SQ+SQ//2,R*SQ-SQ//2))
      for p in self.b.pl: p.draw() #piece list
      for s in self.scores:
        t1=pg.font.SysFont('Arial',18).render(str(s[0]),False,pg.Color('red'))
        rect1=t1.get_rect(center=(s[1][0]*SQ+SQ//2,s[1][1]*SQ+SQ//2-5))
        self.screen.blit(t1,rect1)
    if self.stage==3:
      for b1 in self.bl2:
        b1.draw()
class Button():
  def __init__(self,screen,n,center=(0,0),text='test1',size=(300, 100),font=30):
    self.screen=screen
    self.n=n # it doesn't have to be a function, return a number is enough
    #self.rect=pg.Rect(size)
    #self.rect.center = center
    self.color=(25,25,25,200)
    self.t1=pg.font.SysFont('Arial',30).render(text,False,(200,200,200))
    self.rect1=self.t1.get_rect(center=center)
    self.surf = pg.Surface(size,pg.SRCALPHA)
    self.rect2=self.surf.get_rect(center=center)
  def draw(self):
    #pg.draw.rect(self.screen,self.color,self.rect,border_radius=20)
    pg.draw.rect(self.surf,self.color,self.surf.get_rect(),border_radius=20)
    self.screen.blit(self.surf,self.rect2)
    self.screen.blit(self.t1,self.rect1) #text
  def check(self,e):
    if self.rect2.collidepoint(pg.mouse.get_pos()): #e.pos not exist
      self.color=(255,0,100)
      if e.type==pg.MOUSEBUTTONDOWN and e.button==1:
        return self.n
    else:self.color=(25,25,25,200)
class Piece():
  def __init__(self,screen,center,c=True,n=0):
    self.screen=screen
    self.c3=Trans
    self.center=center
    self.surf=pg.Surface((r*2,r*2),pg.SRCALPHA)
    self.rect2=self.surf.get_rect(center=center)
    self.vir=True
  def draw(self):
    if self.vir:
      pg.draw.circle(self.surf,self.c3,(r,r),r) #relative position on surf
      self.screen.blit(self.surf,self.rect2)
    else:
      self.t1=pg.font.SysFont('Arial',24).render(str(self.n),False,self.c2)
      self.rect1=self.t1.get_rect(center=self.center)
      pg.draw.circle(self.surf,self.c1,(r,r),r)
      self.screen.blit(self.surf,self.rect2)
      self.screen.blit(self.t1,self.rect1)
  def play(self,c,n):
    self.vir=False
    self.n=n
    if c:
      self.c1=B
      self.c2=W
    else:
      self.c1=W
      self.c2=B
    return tuple([a//SQ for a in pg.mouse.get_pos()])
  def check(self,e,c=True,n=0):
    if self.rect2.collidepoint(pg.mouse.get_pos()):
      self.c3=G
      if e.type==pg.MOUSEBUTTONDOWN and e.button==1:
        return tuple([a//SQ for a in pg.mouse.get_pos()])
        # return self.play(c,n) # it's played by Game anyway
    else: self.c3=Trans
def mainloop():
  go=True
  clock = pg.time.Clock()
  pg.init()
  pg.display.set_caption('Five in a row')
  screen = pg.display.set_mode((SQ*R, SQ*R))
  g1=Game(screen)
  while go:
    clock.tick(40)
    screen.fill('#ffcc00')
    for e in pg.event.get():
      if e.type == pg.QUIT: go = False
      if g1.stage==1:
        for b in g1.bl:
          n=b.check(e)
          if n:
            g1.start(n)
            g1.stage=2
      elif g1.stage==2:
        for p in g1.b.pl:
          cord=p.check(e,g1.turn,g1.b.counter)
          if cord:
            g1.move(cord)
        g1.move()
      elif g1.stage==3:
        for b in g1.bl2:
          n=b.check(e)
          if n==1: g1.stage=1
          elif n==2: go=False
    g1.draw()
    pg.display.flip()
if __name__ == "__main__":
  mainloop()