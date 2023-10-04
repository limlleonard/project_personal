import asyncio
import pygame as pg
from math import *
from spiral import spiral
from functions import get_input

def main():
  n_teeth, r3=get_input()
  # n_teeth, r3=32,4
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
    s1.draw(not moving)
    if moving:
      full1=s1.move()
      # print(s1.n_round2, s1.a2)
      if full1:
        moving=False
    pg.display.flip()
  # await asyncio.sleep(0)
  pg.quit()
main()
# asyncio.run(main())