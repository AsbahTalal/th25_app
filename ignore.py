import pygame as pg
from sys import exit
import math,random

#initiates app window
pg.init()
CREATE_OBSTACLE_EVENT = pg.USEREVENT + 1
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
            
#checkpoints for quiz questions
CHECKPOINT_XS = [2319, 4016, 7431, 10834, 17256, 19349, 24752, 30806, 33012, 34992]
#answers for questions
# correct answers for each question image (A/B/C/D). Order must match q1.png, q2.png, ...
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

# ---------- 3) SIMPLE HELPERS ----------
# A dark overlay so the question "pops" over the dimmed game
_OVERLAY = pg.Surface((info.current_w, info.current_h), pg.SRCALPHA)
_OVERLAY.fill((0, 0, 0, 140))

# center any surface on screen
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

    pg.time.set_timer(CREATE_OBSTACLE_EVENT, 2000)

    

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


    #QUIZ STUFF
    SPEED = 10        # your original scroll speed
    distance = 0       # how far we've progressed (rightward), derived from scroll
    quiz_active = False
    quiz_index = -1    # which question is currently shown
    next_checkpoint_idx = 0

    wrong_flash_until = 0


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

    #obstacles
    obstacle_x = info.current_w #to be defined
    obstacle_y = info.current_h*0.85 + 100
    obstacle_height = 200
    #possible obstacle images
    possObstacles = []
    
    def load_scaled_obstacles(path):
        img = pg.image.load(path)
        ogW,ogH = img.get_size()
        newW = int(ogW*(obstacle_height/ogH))
        return pg.transform.scale(img, (newW,obstacle_height))
    possObstacles.append(load_scaled_obstacles("bench.png"))
    possObstacles.append(load_scaled_obstacles("duck.png"))
    possObstacles.append(load_scaled_obstacles("bus.png"))
    possObstacles.append(load_scaled_obstacles("person1.png"))

    #obstacle creations
    obstacles = []
    

    def move():
        for obstacle in obstacles:
            obstacle.x += obs_speed
            
            if obstacle.right < 0:
                obstacles.remove(obstacle)
            
            
    
    def create_obstacles():
        imageSurf = (random.choice(possObstacles))
        spawning = info.current_w
        imageWidth = imageSurf.get_width()
        specific_obs = Obstacle(imageSurf,spawning,imageWidth)
        obstacles.append(specific_obs)

        

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
            if event.type == CREATE_OBSTACLE_EVENT:
                if gameStarted and (not quiz_active) and (not gameEnded):
                    print("TIMER EVENT FIRED")
                    create_obstacles()
            if quiz_active:
                if event.type == pg.KEYDOWN and event.key in _KEY2LETTER:
                    choice = _KEY2LETTER[event.key].upper()
                    correct = QUIZ_ANSWERS[quiz_index]
                    if choice == correct:
                        # Correct: close quiz and resume
                        quiz_active = False
                        quiz_index = -1
                        jumps_left = 2               # optional: reset jumps on resume
                        wrong_flash_until = 0        # clear any red flash
                    else:
                        # Wrong: briefly flash the stopwatch red
                        wrong_flash_until = pg.time.get_ticks() + WRONG_FLASH_MS
                # ignore all other input while quiz is up
                continue
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
            if not quiz_active and not gameEnded:
                #music plays
                pg.mixer.music.unpause()
                #scroll
                i = 0
                while(i < tiles):
                    window.blit(bg_img, (bg_img.get_width()*i + scroll,0))
                    i+= 1
                scroll -= 10
                obs_speed = -12
                #if reaches zach
                if (not gameEnded) and abs(scroll) > bg_img.get_width() - 1800:
                    scroll = -(bg_img.get_width() - 1800)
                    gameEnded = True
                distance += 10
            else:
                # Frozen background
                i = 0
                while i < tiles:
                    window.blit(bg_img, (bg_img.get_width()*i + scroll, 0))
                    i += 1
                obs_speed = 0
                

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
            move()
            for obstacle in obstacles:
                window.blit(obstacle.img, obstacle)
            
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


startScreen()
game()
