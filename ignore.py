import pygame as pg
from sys import exit
import math,random

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


#Obstacle class
obstacle_y = info.current_h*0.85 - 50
obstacle_height = 200
class Obstacle(pg.Rect):
        def __init__(self, img, obstacle_x, width):
            super().__init__(obstacle_x, obstacle_y, width, obstacle_height)
            self.img = img
            self.passed = False
            
            

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

    create_obstacle_timer = pg.USEREVENT + 0
    pg.time.set_timer(create_obstacle_timer,2000) #every 2 secs

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

    #obstacles
    obstacle_x = info.current_w #to be defined
    obstacle_y = info.current_h*0.85
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
    possObstacles.append(load_scaled_obstacles("scooter.png"))
    possObstacles.append(load_scaled_obstacles("person1.png"))

    #obstacle creations
    obstacles = []
    pipe_speed = -8

    def move():
        for obstacle in obstacles:
            obstacle.x += pipe_speed
            print(f"location {obstacle.x}")
            if obstacle.right < 0:
                obstacles.remove(obstacle)
            
    
    def create_obstacles():
        imageSurf = (possObstacles[random.randint(0,len(possObstacles)-1)])
        spawning = info.current_w
        imageWidth = imageSurf.get_width()
        specific_obs = Obstacle(imageSurf,spawning,imageWidth)
        obstacles.append(specific_obs)

        print(len(obstacles))

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
            if event.type == create_obstacle_timer:
                create_obstacles()
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
            
            # for obstacle in obstacles:
            #     window.blit(obstacle.img, obstacle)
            # move()
        
        #when game starts, scrolling
        else:
            #music plays
            pg.mixer.music.unpause()
            #scroll
            i = 0
            while(i < tiles):
                window.blit(bg_img, (bg_img.get_width()*i + scroll,0))
                i+= 1
            scroll -= 10
            #if reaches zach
            if abs(scroll) > bg_img.get_width()-1800:
                scroll =  -(bg_img.get_width() - 1800)
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
            
            for obstacle in obstacles:
                window.blit(obstacle.img, obstacle)
            move()
        #continously update window
        pg.display.update()
        clock.tick(60)

#calling both screens to run








#AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
#AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
#AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
#AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
#asbahs code:


# ===============================================================
# =============== QUIZ CHECKPOINT ADD-ON (DROP-IN) ==============
# Paste this whole block at the *bottom* of ignore.py.
# Then change your final call from:
#     startScreen(); game()
# to:
#     startScreen(); game_with_quiz()
#
# WHAT THIS DOES:
# - Shows q1.png, q2.png, ... at certain distance checkpoints.
# - Game "freezes" while a question is up (background stops, no jumping),
#   but your stopwatch keeps running.
# - Player presses A/B/C/D. If wrong, the stopwatch turns RED briefly.
# - When correct, pop-up closes and the run resumes to the next checkpoint.
# ===============================================================

# ---------- 1) CONFIGURE YOUR QUIZ HERE ----------
# distance checkpoints (in pixels traveled) where a question should appear
CHECKPOINT_XS = [2319, 4016, 7431, 10834, 17256, 19349, 24752, 30806, 33012, 34992]

# correct answers for each question image (A/B/C/D). Order must match q1.png, q2.png, ...
QUIZ_ANSWERS  = ['D','B','C','C','A','A','D','D','A', 'A']

# how long (ms) the timer should turn red after each wrong guess
WRONG_FLASH_MS = 700

# ---------- 2) LOAD YOUR QUESTION IMAGES ----------
# We expect q1.png, q2.png, ..., qN.png to exist next to this script.
# We scale each to 70% of screen height while preserving aspect ratio.
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

def game_with_quiz():
    """
    A copy of your game loop with quiz checkpoints added.
    NOTE: You don't need to delete your original `game()` — just call
    this function instead at the end of the file.
    """
    pg.display.set_caption("Rev Run")
    clock = pg.time.Clock()

    # ----- Background setup (kept same behavior as your file) -----
    bg_img = pg.image.load("background.jpg").convert()
    # Fit background image to screen height (keeps aspect ratio by only forcing height)
    bg_img = pg.transform.scale(bg_img, (bg_img.get_width(), info.current_h))
    scroll = 0
    tiles = math.ceil(info.current_w / bg_img.get_width()) + 1

    # ----- HUD images (clock & start button) -----
    clock_img = pg.image.load("clock.png").convert_alpha()
    clock_img = pg.transform.scale(clock_img, (406.2, 221.4))

    startButton = pg.image.load("startButton.png").convert_alpha()
    startButton = pg.transform.scale(startButton, (990, 342))
    start_btn_rect = startButton.get_rect(center=(info.current_w//2, int(info.current_h*0.48)))

    # ----- Stopwatch font -----
    font = pg.font.SysFont("Consolas", 60)

    # ----- Reveille sprites -----
    rev_img = pg.image.load("dog2.png").convert_alpha()
    rev_img = pg.transform.scale(rev_img, (495, 270))
    rev_img_jump = pg.image.load("dog1.png").convert_alpha()
    rev_img_jump = pg.transform.scale(rev_img_jump, (495, 270))

    # Jump/jog parameters
    jumps_left = 2          # allow double jump
    jump_height = 300       # pixels of vertical travel in the jump
    disp_PopUp = False      # whether the jump animation is active
    popUp_start = 0         # jump start time
    popUp_dur = 700         # jump duration (ms)

    # Reveille position (same as your original)
    rev_rect = rev_img.get_rect()
    rev_rect.center = (int(info.current_w*0.25), int(info.current_h*0.87))
    original_Y = rev_rect.centery

    # Sounds
    alarm = pg.mixer.Sound("alarmBeep.mp3")
    jumpSound = pg.mixer.Sound("jump.mp3")
    alarm.set_volume(1.0)
    jumpSound.set_volume(0.2)
    alarm.play(-1)  # loop alarm until the game starts

    # Base game state
    gameStarted = False
    gameEnded = False
    start_time = 0  # used by stopwatch

    # ----- NEW: Quiz state -----
    SPEED = 10        # your original scroll speed
    distance = 0       # how far we've progressed (rightward), derived from scroll
    quiz_active = False
    quiz_index = -1    # which question is currently shown
    next_checkpoint_idx = 0

    # WRONG-ANSWER FLASH: if nonzero, we keep the timer red until "now < wrong_flash_until"
    wrong_flash_until = 0

    while True:
        # ========== INPUT ==========
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(); exit()

            # If a quiz is up, we only listen for quiz answers (A/B/C/D)
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

            # Normal game input when quiz is NOT active
            if event.type == pg.KEYDOWN:
                # Space makes Reveille jump (only if game started)
                if event.key == pg.K_SPACE and gameStarted:
                    if jumps_left > 0:
                        disp_PopUp = True
                        popUp_start = pg.time.get_ticks()
                        jumpSound.play()
                        jumps_left -= 1

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # Click start button to begin the run
                if start_btn_rect.collidepoint(event.pos) and not gameStarted:
                    gameStarted = True
                    start_time = pg.time.get_ticks()
                    alarm.stop()
                    pg.mixer.music.unpause()

        # ========== UPDATE & RENDER ==========
        if not gameStarted:
            # Start screen: static background, rev, start button, clock image
            window.blit(bg_img, (0, 0))
            window.blit(rev_img, rev_rect)
            window.blit(startButton, start_btn_rect)
            window.blit(clock_img, (960, 450))

        else:
            # Background rendering:
            # - If no quiz and not ended, we move (scroll) the background.
            # - If a quiz is up or the game ended, we draw the background "frozen".
            if (not quiz_active) and (not gameEnded):
                i = 0
                while i < tiles:
                    window.blit(bg_img, (bg_img.get_width()*i + scroll, 0))
                    i += 1
                # move left by SPEED
                scroll -= SPEED

                # Track the total distance progressed (convert 'scroll' → positive distance)
                distance = -scroll
                # When a full tile has scrolled past, reset scroll but keep distance continuous
                if abs(scroll) > bg_img.get_width():
                    scroll = 0
                    distance += bg_img.get_width()
            else:
                # Frozen background
                i = 0
                while i < tiles:
                    window.blit(bg_img, (bg_img.get_width()*i + scroll, 0))
                    i += 1

            # End condition (your original "reaches Zach" logic)
            if (not gameEnded) and abs(scroll) > bg_img.get_width() - 1800:
                scroll = -(bg_img.get_width() - 1800)
                gameEnded = True

            # ----- Stopwatch (always runs while game is started) -----
            elapsed_sec = (pg.time.get_ticks() - start_time) // 1000
            minutes = elapsed_sec // 60
            seconds = elapsed_sec % 60
            # TIMER COLOR: red if we're within the wrong-flash window, else black
            timer_color = (255, 0, 0) if pg.time.get_ticks() < wrong_flash_until else (0, 0, 0)
            timer_surf = font.render(f"{minutes:02}:{seconds:02}", True, timer_color)
            window.blit(timer_surf, (50, 50))

            # ----- Jump animation (disabled while quiz is active) -----
            if (not quiz_active) and disp_PopUp:
                t = pg.time.get_ticks() - popUp_start
                if t > popUp_dur:
                    disp_PopUp = False
                    rev_rect.centery = original_Y
                    jumps_left = 2
                else:
                    half = popUp_dur/2
                    if t < half:
                        # going up
                        rev_rect.centery = original_Y - int(jump_height * (t / half))
                    else:
                        # coming down
                        rev_rect.centery = original_Y - int(jump_height * (1 - (t - half) / half))

            # draw Reveille (jump frame only when jumping & no quiz)
            window.blit(rev_img_jump if (disp_PopUp and not quiz_active) else rev_img, rev_rect)

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

        pg.display.update()
        clock.tick(60)

startScreen()
game_with_quiz()
