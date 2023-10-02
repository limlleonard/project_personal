import pygame as pg
from math import *
import colorsys
class spiral:
  def __init__(self, teeth2, r_draw):
    self.breite=self.hohe = 600
    self.screen1=pg.display.set_mode([self.breite, self.hohe])
    self.screen2 = pg.Surface([self.breite, self.hohe])
    self.clock = pg.time.Clock()

    self.r1=round(self.hohe//2*0.9) # radius of big circle
    self.c1=(self.breite//2,self.hohe//2)
    self.a1=self.a2=pi/2 # angle circle 2 to 1, angle drawing point to c2
    # fix the number of teeth on circle 1 (100) -> distance between teeth (for c1 and c2) -> given a r2 find a closest r2, which have a whole number of teeth. Distance is calculate by the arc, not a straight line
    self.nr_teeth1=120
    self.dist1=self.r1*2*pi/self.nr_teeth1
    self.nr_teeth2=teeth2
    self.r2=self.nr_teeth2*self.dist1 / (2*pi)

    self.r_draw=r_draw
    self.r3=r_draw * self.dist1 # distance of the drawing point to the center of the moving circle
    self.r4=5 # radius drawing point
    self.drawn, self.drawn_color=[],[] # save drawn points
    self.pos()
    self.step=pi/360
    self.n_round1=self.n_round2=0
    self.full_round=self.full()

  def moon(self, c1, r1, a1): # input: center1, radius, angle, output: center2
    return (c1[0]+r1*sin(a1), c1[1]-r1*cos(a1))
  def angle_color(self, a1):
    rainbow1 = colorsys.hsv_to_rgb(a1/(2*pi), 1, 1)
    rainbow1=tuple([i*255 for i in rainbow1])
    return rainbow1
  def full(self): # a full round, the drawing point return to the original place
    lcm1=lcm(self.nr_teeth1, self.nr_teeth2)
    full_round=lcm1//self.nr_teeth2
    return full_round
  def move(self):
    self.a1+=self.step
    if self.a1>2*pi:
      self.a1-=2*pi
      self.n_round1+=1
    self.a2-=self.step*self.r1/self.r2-self.step # -step is tricky to understand, rolling a wheel in a bigger wheel is different from on a flat line
    if self.a2<0:
      self.a2+=2*pi
      self.n_round2+=1
    self.pos()
    self.drawn.append(self.c3)
    self.drawn_color.append(self.angle_color(self.a1))
    return self.n_round2>=self.full_round
  def pos(self):
    self.c2=(self.c1[0]+(self.r1-self.r2)*cos(self.a1), self.c1[1]-(self.r1-self.r2)*sin(self.a1))
    self.c3=(self.c2[0]+self.r3*cos(self.a2), self.c2[1]-self.r3*sin(self.a2)) # position of the drawing point
  def draw(self):
    str1=f'N1={self.nr_teeth1}, N2={round(self.nr_teeth2)}, N3={self.r_draw}' # text
    font1 = pg.font.SysFont('freesanbold.ttf', 30)
    text1 = font1.render(str1, True, (0, 255, 0))
    textRect1 = text1.get_rect()
    textRect1.topleft  = (10, 10)
    self.screen2.blit(text1, textRect1)

    pg.draw.circle(self.screen2, (128, 128, 128), self.c1,self.r1) # big circle
    pg.draw.circle(self.screen2, (255,255,255), self.c1,2)
    for i1 in range(self.nr_teeth1): # teeth
      pg.draw.circle(self.screen2, (128,128,128), self.moon(self.c1, self.r1, 2*pi*i1/self.nr_teeth1), self.dist1/2.2)

    for i in range(self.nr_teeth2): # running circle
      pg.draw.circle(self.screen2, (192,192,192), self.moon(self.c2, self.r2, 2*pi/self.nr_teeth2*i+pi/2-self.a2), self.dist1/2.2, 1) # +pi/2 so that the starting point is vertical top
    pg.draw.circle(self.screen2, (255,255,255), self.c2, 2) #c2
    pg.draw.circle(self.screen2, self.angle_color(self.a1), self.c3, self.r4) #drawing point
    for pt,cl in zip(self.drawn, self.drawn_color): # track
      pg.draw.circle(self.screen2, cl, pt, self.r4/5)

def get_input():
  while True:
    ip1=input('Give the number of the teeth (20-80): ')
    try:
      n_teeth=int(ip1)
      if n_teeth>19 and n_teeth<81: break
    except: pass
  while True:
    ip2=input(f'Give the relative radius of the drawing point (1-{n_teeth//6}): ')
    try:
      r3=int(ip2)
      if r3>0 and r3<=n_teeth: break
    except: pass
  return n_teeth, r3
n_teeth, r3=get_input()

s1=spiral(n_teeth, r3)
pg.init()
weitermachen = True
moving=False
while weitermachen:
  s1.clock.tick(60)
  for event in pg.event.get():
    if event.type == pg.QUIT or event.type == pg.KEYDOWN:
      if event.key == pg.K_ESCAPE:
        weitermachen = False
      if event.key==pg.K_SPACE:
        moving=not moving
  s1.screen1.blit(s1.screen2, (0, 0))
  s1.draw()
  if moving:
    full1=s1.move()
    # print(s1.n_round2, s1.a2)
    if full1:
      moving=False
  pg.display.flip()

pg.quit()
