import pygame as pg
import sys, time
pg.init()

class Game:
    def __init__(self):
        #window config
        self.width = 1920
        self.height = 1080
        self.scale_factor = 1.5
        self.win=pg.display.set_mode((self.width, self.height))
        self.clock=pg.time.Clock()
        self.setUpBgAndGround()
        self.gameLoop()

    def gameLoop(self):
        last_time=time.time()
        while True:
            new_time = time.time()
            diff = new_time - last_time
            last_time = new_time
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)

game = Game()