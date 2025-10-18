import pygame as pg
from sys import exit

#variables
width = 400
height = 500

#images
#bg image
bg_img = pg.image.load()


pg.init()
info = pg.display.Info()
window = pg.display.set_mode((info.current_w,info.current_h))
pg.display.set_caption("Temp")
clock = pg.time.Clock()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
    pg.display.update()
    clock.tick(60)
