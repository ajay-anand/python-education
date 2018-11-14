import pygame as pg
import random as rn

def overlap(x1,y1,x2,y2):
  return x1 >= x2 and x1 <= x2 + 0.9 and y1 >= y2 and y1 <= y2 + 0.9

#game board
pg.init()
screen = pg.display.set_mode((800,600), pg.HWSURFACE)
pg.font.init()
text = pg.font.SysFont('Liberation Mono', 28, bold=True)
im = pg.image.load("game.png").convert_alpha()
bg = pg.image.load("bg.png").convert()

#apple
ax = 5
ay = 5

#worm
wx = [0, -1, -2]
wy = [0, 0, 0]
wl = 3
wd = (1, 0)
for i in range(0, 1000):
  wx.append(-1)
  wy.append(-1)

def setBit(i, j):
  if (wx[j]-wx[i]+25)%25==1:
    return 2
  if (wx[j]-wx[i]+25)%25==24:
    return 4
  if (wy[j]-wy[i]+19)%19==1:
    return 8
  if (wy[j]-wy[i]+19)%19==18:
    return 1
  return 0

Part = { 10: 0, 6: 1, 12: 2, 8: 3, 4: 4, 3: 5, 9: 7, 2: 8, 1: 9, 5: 12, 17: 13, 18: 14, 20: 18, 24: 19 }

def part(n):
  if n == 0:
    code = setBit(n, n+1)
  elif n == wl-1:
    code = setBit(n, n-1) + 16
  else:
    code = setBit(n, n-1) + setBit(n,n+1)
  return (Part[code]%5*32, Part[code]//5*32, 32, 32)

active = True
while active:

  #game controls
  for i in range(3):
    pg.event.pump()
    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE]:
      active = False
    elif keys[pg.K_RIGHT]:
      wd = (1,0)
    elif keys[pg.K_LEFT]:
      wd = (-1,0)
    elif keys[pg.K_UP]:
      wd = (0,-1)
    elif keys[pg.K_DOWN]:
      wd = (0,1)
    pg.time.Clock().tick(18)

  #update worm position
  for i in range(wl-1, 0, -1):
    wx[i] = wx[i-1]
    wy[i] = wy[i-1]
  wx[0] = (wx[0] + wd[0] + 25)%25
  wy[0] = (wy[0] + wd[1] + 19)%19

  #check overlap with apple
  for i in range(0, wl):
    if overlap(ax, ay, wx[i], wy[i]):
      ax = rn.randint(2,24)
      ay = rn.randint(2,17)
      wx[wl]=2*wx[wl-1]-wx[wl-2]
      wy[wl]=2*wy[wl-1]-wy[wl-2]
      wl = wl + 1

  #check self overlap
  for i in range(2, wl):
    if overlap(wx[0], wy[0], wx[i], wy[i]):
      print("Worm hits itself!")
      active = False

  #drawing and animation
  screen.blit(bg, (0,0) )
  scale = 32
  for i in range(0, wl):
    screen.blit(im, (wx[i]*scale, wy[i]*scale), part(i))
  screen.blit(im, (ax*scale, ay*scale), (0, 96, 32, 32))
  screen.blit(text.render('Score: '+str(wl-3), False, (250, 60, 6)), (600,560))
  pg.display.flip()

print('Score: ', wl-3)
pg.quit()
