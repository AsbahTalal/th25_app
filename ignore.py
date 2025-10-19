import pygame as pg
from sys import exit
import math

#initiates app window
pg.init()
pg.mixer.init()

#initiates background music, paused until game starts
pg.mixer.music.load("kahoot.mp3")
pg.mixer.music.play(-1)
pg.mixer.music.pause()

#size of display
info = pg.display.Info()
window = pg.display.set_mode((info.current_w,info.current_h))

#start screen
def startScreen():
    #creates start window 
    pg.display.set_caption("Start Menu")
    #creates background to display screen
    bg_img = pg.image.load("start.png").convert()
    bg_img = pg.transform.scale(bg_img, (info.current_w, info.current_h))

    #while start screen
    while True:
        window.blit(bg_img, (0,0))

        #events
        for event in pg.event.get():
            #if close screen
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            #if key pressed 
            elif event.type == pg.KEYDOWN:
                #if enter pressed
                if event.key == pg.K_RETURN:
                    #ends start screen
                    return
        #continously updates screen
        pg.display.update()

#game screen
def game():
    #creates game window 
    pg.display.set_caption("Rev Run")
    #Clock - controls framerate 
    clock = pg.time.Clock()

    #images
    #bg image
    bg_img = pg.image.load("background.jpg").convert()
    bg_img = pg.transform.scale(bg_img, (bg_img.get_width(), info.current_h))
    scroll = 0
    tiles = math.ceil(info.current_w / bg_img.get_width())+1

    #clock
    clock_img = pg.image.load("clock.png").convert_alpha()
    clock_img = pg.transform.scale(clock_img, (406.2, 221.4))

    #start button
    startButton = pg.image.load("startButton.png").convert_alpha()
    startButton = pg.transform.scale(startButton, (990,342))

    #font for stopwatch
    font = pg.font.SysFont("Consolas", 60)

    #reveille variables
    #rev image
    rev_img = pg.image.load("dog2.png")
    rev_img = pg.transform.scale(rev_img, (495,270))
    #rev jump image
    rev_img_jump = pg.image.load("dog1.png")
    rev_img_jump = pg.transform.scale(rev_img_jump, (495,270))
    #other variables for jumping rev
    #jumps remaining, so she can double jump
    jumps_left = 2
    #how high
    jump_height = 300
    #if change to jumping rev image
    disp_PopUp = False
    #jumping duration
    popUp_start = 0
    popUp_dur = 700
    #position variables
    rev_rect = rev_img.get_rect()
    rev_rect.center = (info.current_w*0.25,info.current_h*0.87)
    original_Y = rev_rect.centery

    #jump and alarm 
    alarm = pg.mixer.Sound("alarmBeep.mp3")
    jumpSound = pg.mixer.Sound("jump.mp3")
    pg.mixer.Sound.set_volume(alarm,1)
    pg.mixer.Sound.set_volume(jumpSound,0.2)
    #continously play alarm until game starts
    alarm.play(-1)
    gameStarted = False
    gameEnded = False
    #while game screen
    while True:
        
        #area of start button
        start_Button = pg.Rect(682,573,990, 342)

        #events
        for event in pg.event.get():
            #close screen
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            #if key pressed
            if event.type == pg.KEYDOWN:
                #if spacebar
                if event.key == pg.K_SPACE and gameStarted:
                    if jumps_left > 0:
                        disp_PopUp = True
                        popUp_start = pg.time.get_ticks()
                        jumpSound.play()
                        jumps_left -= 1
            #if mouse pressed
            elif event.type == pg.MOUSEBUTTONDOWN:
                #if left click
                if event.button == 1:
                    #if area of start button was pressed 
                    if start_Button.collidepoint(event.pos) and not gameStarted:
                        gameStarted=True
                        #starts countdown
                        start_time = pg.time.get_ticks()
                        alarm.stop()

                
        #when game hasnt started, display background, rev, start button, alarm clock
        if not gameStarted:
            window.blit(bg_img, (0,0))
            window.blit(rev_img, rev_rect)
            window.blit(startButton, (323,340.5))
            window.blit(clock_img, (960,450))
        
        #when game starts, scrolling
        else:
            #music plays
            pg.mixer.music.unpause()
            #scroll
            i = 0
            while i < tiles:
                window.blit(bg_img, (bg_img.get_width() * i + scroll, 0))
                i += 1
            scroll -= 150  # scroll speed

            # check if reached end
            total_bg_width = bg_img.get_width() * tiles
            if abs(scroll) > total_bg_width - info.current_w:
                scroll = -(total_bg_width - info.current_w)
                gameEnded = True

            #stopwatch stuff
            #math
            if not gameEnded:
                elapsed_time = (pg.time.get_ticks() - start_time) // 1000  # seconds
                minutes = elapsed_time // 60
                seconds = elapsed_time % 60
                stopwatch_text = f"{minutes:02}:{seconds:02}"
                #displays stop watch
                timer = font.render(stopwatch_text, True, (0,0,0))
            window.blit(timer, (50, 50))

        # if rev is jumping
        if disp_PopUp:
            elapsed_time = pg.time.get_ticks() - popUp_start
            #if jump completed, reset y position of rev
            if elapsed_time > popUp_dur:
                disp_PopUp = False
                rev_rect.centery = original_Y
                jumps_left = 2
            #if jumping
            else:
                half = popUp_dur/2
                #going up
                if elapsed_time < half:
                    rev_rect.centery = original_Y - int(jump_height * (elapsed_time / half))
                #going down
                else:
                    rev_rect.centery = original_Y - int(jump_height * (1 - (elapsed_time - half) / half))
        #if game has started, update rev if jumping
        if gameStarted:
            window.blit(rev_img_jump if disp_PopUp else rev_img, rev_rect)

        #continously update window
        pg.display.update()
        clock.tick(60)

#calling both screens to run
startScreen()
game()