import pygame as pg
from sys import exit
import math,random

#initiates app window
pg.init()
#continously updating objects
CREATE_OBSTACLE_EVENT = pg.USEREVENT + 1
#initiates sounds mixer
pg.mixer.init()
#initiates background music, paused until game starts
pg.mixer.music.load("kahoot.mp3")
pg.mixer.music.play(-1)
pg.mixer.music.pause()

#size of display
info = pg.display.Info()
window = pg.display.set_mode((info.current_w,info.current_h))

#Obstacle class
obstacle_y = info.current_h*0.85 +135
obstacle_height = 200
class Obstacle(pg.Rect):
        def __init__(self, img, obstacle_x, width):
            top = int(obstacle_y - obstacle_height)
            super().__init__(int(obstacle_x), top, int(width), obstacle_height)
            self.img = img
            self.passed = False

#quiz   
#x coordinates for quiz questions
CHECKPOINT_XS = [1680, 3680, 6680, 9880, 16480, 18580, 23980, 29580, 32330, 34480]
#answers for questions
QUIZ_ANSWERS  = ['D','B','C','C','A','A','D','D','A', 'A']  
#length to flash timer for wrong guess
WRONG_FLASH_MS = 700
#import quiz images
QUIZ_IMAGES = []
for i in range(len(CHECKPOINT_XS)):
    qimg = pg.image.load(f"q{i+1}.png").convert_alpha()
    target_h = int(info.current_h * 0.7)
    target_w = int(qimg.get_width() * (target_h / qimg.get_height()))
    qimg = pg.transform.smoothscale(qimg, (target_w, target_h))
    QUIZ_IMAGES.append(qimg)
#visual dimming effect
_OVERLAY = pg.Surface((info.current_w, info.current_h), pg.SRCALPHA)
_OVERLAY.fill((0, 0, 0, 140))
#center of sdisplay
def _center_xy(surf):
    r = surf.get_rect()
    return (info.current_w - r.width)//2, (info.current_h - r.height)//2
# map keys to letters for the quiz
_KEY2LETTER = {pg.K_a: 'A', pg.K_b: 'B', pg.K_c: 'C', pg.K_d: 'D'}


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
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    #ends start screen
                    return
        #continously updates screen
        pg.display.update()

#game screen
def game():
    #creates game window 
    pg.display.set_caption("Campus Chaos")
    #Clock - controls framerate 
    clock = pg.time.Clock()
    pg.time.set_timer(CREATE_OBSTACLE_EVENT, 3000)

    #images
    #bg image
    bg_img = pg.image.load("background.jpg").convert()
    bg_img = pg.transform.scale(bg_img, (bg_img.get_width(), info.current_h))
    scroll = 0
    tiles = math.ceil(info.current_w / bg_img.get_width())+1

    #end background image
    ebg_img = pg.image.load("endScreen.png").convert()
    ebg_img = pg.transform.scale(ebg_img, (info.current_w, info.current_h))

    #clock image
    clock_img = pg.image.load("clock.png").convert_alpha()
    clock_img = pg.transform.scale(clock_img, (406, 221))

    #start button image
    startButton = pg.image.load("startButton.png").convert_alpha()
    startButton = pg.transform.scale(startButton, (990,342))

    #quit button image
    quitButton = pg.image.load("quitButton.png").convert_alpha()

    #font for stopwatch
    font = pg.font.SysFont("Consolas", 60)


    #quiz variables
    #scroll speed
    SPEED = 10     
    #x distance
    distance = 0      
    #if quiz happening
    quiz_active = False
    quiz_index = -1    
    next_checkpoint_idx = 0
    wrong_flash_until = 0

    #reveille variables
    #rev image
    rev_img = pg.image.load("dog2.png")
    rev_img = pg.transform.scale(rev_img, (259,270))
    #rev jump image
    rev_img_jump = pg.image.load("dog1.png")
    rev_img_jump = pg.transform.scale(rev_img_jump, (259,270))
    #rev jumping variables
    #make rectangle of rev image
    rev_rect = rev_img.get_rect()
    #make center a certain percentage based on display screen
    rev_rect.center = (info.current_w * 0.25, info.current_h * 0.85)
    #original, fixed point
    original_Y = rev_rect.centery
    #jumping concept - 
    #default vertical speed 0, because begin without jumping
    velocity_y = 0
    #speed downwards
    gravity = 0.8
    #speed upwards
    jump_power = 24
    #amount of jumps, double jump
    jumps_left = 2
    #if jump, will change image of rev
    disp_PopUp = False

    #obstacles
    #coords
    obstacle_x = info.current_w 
    obstacle_y = info.current_h*0.85 + 100
    #height
    obstacle_height = 200
    #possible obstacle images
    possObstacles = []
    
    #import obstacle images, scaling 
    def load_scaled_obstacles(path):
        img = pg.image.load(path)
        ogW,ogH = img.get_size()
        newW = int(ogW*(obstacle_height/ogH))
        return pg.transform.scale(img, (newW,obstacle_height))
    possObstacles.append(load_scaled_obstacles("bench.png"))
    possObstacles.append(load_scaled_obstacles("duck.png"))
    possObstacles.append(load_scaled_obstacles("bus.png"))
    possObstacles.append(load_scaled_obstacles("person1.png"))
    possObstacles.append(load_scaled_obstacles("person2.png"))
    possObstacles.append(load_scaled_obstacles("person3.png"))
    possObstacles.append(load_scaled_obstacles("person4.png"))
    possObstacles.append(load_scaled_obstacles("person5.png"))
    possObstacles.append(load_scaled_obstacles("person6.png"))
    possObstacles.append(load_scaled_obstacles("person7.png"))
    possObstacles.append(load_scaled_obstacles("person8.png"))

    #obstacle creations
    obstacles = []
    collisionCount = 0
    winner = True
    quiz = False
    
    #obstacle move function
    def move():
        for obstacle in obstacles:
            obstacle.x += obs_speed
            
            if obstacle.right < 0:
                obstacles.remove(obstacle)
            
    #create obstacle function
    def create_obstacles():
        imageSurf = (random.choice(possObstacles))
        spawning = info.current_w
        imageWidth = imageSurf.get_width()
        specific_obs = Obstacle(imageSurf,spawning,imageWidth)
        obstacles.append(specific_obs)
    
    #lives display function
    def displayHearts(lives,rightHeartX):
        heart = pg.image.load('heart1.png')
        heart = pg.transform.scale(heart,(70,70))
        heartX = rightHeartX
        for i in range(lives):
            window.blit(heart,(heartX,50))
            heartX -= 100
           
    #jump and alarm sound
    alarm = pg.mixer.Sound("alarmBeep.mp3")
    jumpSound = pg.mixer.Sound("jump.mp3")
    pg.mixer.Sound.set_volume(alarm,1)
    pg.mixer.Sound.set_volume(jumpSound,0.2)
    #continously play alarm until game starts
    alarm.play(-1)

    #game started/ended variables
    gameStarted = False
    gameEnded = False

    #while game screen
    while True:
        #area of start button, quit button
        start_Button = pg.Rect(682,573,990, 342)
        quit_Button = pg.Rect(200,100,quitButton.get_width(), quitButton.get_height())

        #events
        for event in pg.event.get():
            #close screen
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            #if create obstacle
            if event.type == CREATE_OBSTACLE_EVENT:
                if gameStarted and (not quiz_active) and (not gameEnded):
                    create_obstacles()
            #quiz, check user input
            if quiz_active:
                if event.type == pg.KEYDOWN and event.key in _KEY2LETTER:
                    choice = _KEY2LETTER[event.key].upper()
                    correct = QUIZ_ANSWERS[quiz_index]
                    if choice == correct:
                        #correct, resets variables
                        quiz_active = False
                        quiz_index = -1
                        jumps_left = 2             
                        wrong_flash_until = 0      
                    else:
                        #wrong, stopwatch flash red
                        wrong_flash_until = pg.time.get_ticks() + WRONG_FLASH_MS
                #ignore all other input while quiz is up
                continue
            #if key pressed
            if event.type == pg.KEYDOWN:
                #if spacebar
                #not active while quiz is up and have jumps remaining
                if event.key == pg.K_SPACE and gameStarted and jumps_left > 0 and not quiz:
                    velocity_y = -jump_power
                    jumps_left -= 1
                    jumpSound.play()
            #if mouse left clicked
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                #if game successfully ended, allow user to quiz 
                if gameEnded:
                    if quit_Button.collidepoint(event.pos):
                        pg.quit()
                        exit()
                #to start beginning of game w/ start button
                elif start_Button.collidepoint(event.pos) and not gameStarted:
                    gameStarted=True
                    #starts countdown
                    start_time = pg.time.get_ticks()
                    alarm.stop()

        #when game hasnt started, display background, rev, start button, alarm clock
        if not gameStarted:
            window.blit(bg_img, (0,0))
            window.blit(rev_img, rev_rect)
            window.blit(startButton, (323,340))
            window.blit(clock_img, (960,450))
        
        #when game active
        else:

            #if there is no quiz
            if not quiz_active and not gameEnded:
                #music plays
                pg.mixer.music.unpause()

                #scrolling stuff
                i = 0
                while(i < tiles):
                    window.blit(bg_img, (bg_img.get_width()*i + scroll,0))
                    i+= 1
                scroll -= 9
                #object speed and distance 
                obs_speed = -12
                distance += 9

                #if reaches zach, ends game
                if abs(scroll) > bg_img.get_width() - 1800:
                    scroll = -(bg_img.get_width() - 1800)
                    gameEnded = True
                    obstacles.clear()

                #rev updates
                velocity_y += gravity
                rev_rect.centery += velocity_y

                #landing, resest values
                if rev_rect.centery >= original_Y:
                    rev_rect.centery = original_Y
                    velocity_y = 0
                    jumps_left = 2

                #update jump image
                disp_PopUp = rev_rect.centery < original_Y
                window.blit(rev_img_jump if disp_PopUp else rev_img, rev_rect)
            #if quiz active
            else:
                # Frozen background
                i = 0
                while i < tiles:
                    window.blit(bg_img, (bg_img.get_width()*i + scroll, 0))
                    i += 1
                #frozen object
                obs_speed = 0
                #frozen rev
                velocity_y = 0
                if disp_PopUp:
                    window.blit(rev_img_jump, rev_rect)
                else:
                    window.blit(rev_img, rev_rect)
                

            elapsed_time = (pg.time.get_ticks() - start_time) // 1000  # seconds
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            timer_color = (255, 0, 0) if pg.time.get_ticks() < wrong_flash_until else (0, 0, 0)
            stopwatch_text = f"{minutes:02}:{seconds:02}"
            #displays stop watch
            timer = font.render(stopwatch_text, True, timer_color)
            window.blit(timer, (50, 50))

            if gameEnded and winner:
                #stop sounds
                jumpSound.stop()
                #let rev land
                if rev_rect.centery < original_Y:
                    velocity_y += gravity
                    rev_rect.centery += velocity_y
                    disp_PopUp = True
                    window.blit(rev_img_jump, rev_rect)
                else:
                    rev_rect.centery = original_Y
                    velocity_y = 0
                    disp_PopUp = False
                    window.blit(rev_img, rev_rect)
                    #wait couple seconds
                    if 'endTime' not in locals():
                        endTime = pg.time.get_ticks() 

                    elapsed_since_end = pg.time.get_ticks() - endTime
                    if elapsed_since_end < 1000:
                        window.blit(rev_img, rev_rect)
                    else:
                        #end screen
                        window.fill((0,0,0))
                        pg.mixer.music.pause()
                        window.blit(ebg_img, (0,0))
                        window.blit(quitButton, quit_Button.topleft)
                        yay = pg.mixer.Sound("success.mp3")
                        yay.play()
                        window.blit(rev_img,rev_rect)
            elif gameEnded and not winner:
                break

        #if game has started
        if gameStarted and not gameEnded:
            move()
            displayHearts(5-collisionCount,info.current_w-100)
            for obstacle in obstacles:
                window.blit(obstacle.img, obstacle)
                if rev_rect.colliderect(obstacle):
                    collisionCount += 1
                    collision = pg.mixer.Sound('crash.mp3')
                    collision.play()

                    obstacles.remove(obstacle)
                    if collisionCount >= 5:
                        gameEnded = True
                        winner = False

            # ----- Trigger next quiz when we pass the next checkpoint -----
            if (not quiz_active) and (next_checkpoint_idx < len(CHECKPOINT_XS)):
                if distance >= CHECKPOINT_XS[next_checkpoint_idx]:
                    quiz_active = True
                    quiz_index = next_checkpoint_idx
                    next_checkpoint_idx += 1

            # ----- Draw quiz pop-up if active -----
            if quiz_active:
                
                # darken the scene
                window.blit(_OVERLAY, (0, 0))
                # show the current question image centered
                qimg = QUIZ_IMAGES[quiz_index]
                qx, qy = _center_xy(qimg)
                window.blit(qimg, (qx, qy))
                # small hint text under the scroll
                hint = font.render("Press A / B / C / D", True, (255, 255, 255))
                hint_rect = hint.get_rect(center=(info.current_w//2, qy + qimg.get_height() + 30))
                window.blit(hint, hint_rect)
                
        #continously update window
        pg.display.update()
        clock.tick(60)

#lose screen
def lose():
    pg.display.set_caption("Losing Screen")
    losing_img = pg.image.load("loser.png").convert()
    losing_img = pg.transform.scale(losing_img, (info.current_w, info.current_h))
    while True:
        window.blit(losing_img, (0,0))
        restart_button = pg.Rect(428,231,1377,393)
        quit_button = pg.Rect(671,864,292,120)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.collidepoint(event.pos):
                    return    
                elif quit_button.collidepoint(event.pos):
                    pg.quit()
                    exit()
        pg.display.update()



startScreen()
while True:
    game()
    lose()

