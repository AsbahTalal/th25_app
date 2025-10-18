import pygame as pg
from sys import exit

#variables
width = 400
height = 500

pg.init()
window = pg.display.setmode((width,height))
pg.display.set_caption("Temp")

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
