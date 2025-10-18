import pygame as pg
from sys import exit
import math

#initiates app window
pg.init()
info = pg.display.Info()
window = pg.display.set_mode((info.current_w,info.current_h))

#start screen
def startScreen():
    #creates window and background
    pg.display.set_caption("Start Menu")
    bg_img = pg.image.load("startScreen.png").convert()
    bg_img = pg.transform.scale(bg_img, (info.current_w, info.current_h))

    while True:
        window.blit(bg_img, (0,0))

        mouse_x, mouse_y = pg.mouse.get_pos()

  

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return
        pg.display.update()


#game screen
def game():
    #name of window
    pg.display.set_caption("Rev Run")
    #framerate
    clock = pg.time.Clock()

    #images
    #bg image
    bg_img = pg.image.load("gameBackground.png").convert()
    scroll = 0
    tiles = math.ceil(info.current_w / bg_img.get_width())+1

    #fonts for stopwatch
    font = pg.font.SysFont("Consolas", 60)
    start_time = pg.time.get_ticks()

    #reveille class
    rev_img = pg.image.load("dog.png")
    rev_image = pg.transform.scale(rev_img, (100,100))
    rev_img_jump = pg.image.load("suprise.png")
    rev_img_jump = pg.transform.scale(rev_img_jump, (400,400))
    jump_height = 100
    disp_PopUp = False
    popUp_start = 0
    popUp_dur = 700
    rev_rect = rev_img.get_rect()
    rev_rect.center = (600,800)
    original_Y = rev_rect.centery
    start = False
    while True:

        #create background
        #if not jump to start
        if not start:
            window.blit(bg_img, (0, 0))
        #if starting
        #scrolling
        else:
            i = 0
            while(i < tiles):
                window.blit(bg_img, (bg_img.get_width()*i + scroll,0))
                i+= 1
            scroll -= 6
            if abs(scroll) > bg_img.get_width():
                scroll = 0

        # --- Stopwatch calculation ---
        elapsed_time = (pg.time.get_ticks() - start_time) // 1000  # seconds
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        stopwatch_text = f"{minutes:02}:{seconds:02}"

        # render text
        timer = font.render(stopwatch_text, True, (0,0,0))
        window.blit(timer, (50, 50))


        #closing game
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            #if keyboard
            if event.type == pg.KEYDOWN:
                #if spacebar
                if event.key == pg.K_SPACE:
                    disp_PopUp = True
                    popUp_start = pg.time.get_ticks()

        if disp_PopUp:
            elapsed_time = pg.time.get_ticks() - popUp_start
            if elapsed_time > popUp_dur:
                disp_PopUp = False
                rev_rect.centery = original_Y
            else:
                half = popUp_dur/2
                if elapsed_time < half:
                # going up
                    rev_rect.centery = original_Y - int(jump_height * (elapsed_time / half))
                else:
                # coming down
                    rev_rect.centery = original_Y - int(jump_height * (1 - (elapsed_time - half) / half))

        window.blit(rev_img_jump if disp_PopUp else rev_img, rev_rect)
        pg.display.update()
        clock.tick(60)
#call
startScreen()
game()