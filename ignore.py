import pygame as pg
import sys
pg.init()

class Game:
    def __init__(self):
        self.width = 1920
        self.height = 1080
        self.win=pg.display.set_mode((self.width, self.height))
        self.bg_img=pg.image.load("1.png").convert()
        self.gameLoop()

    def gameLoop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.win.blit(self.bg_img,(0,0))
            pg.display.update()

game = Game()