import pygame as pg
from sys import exit
import math, random

pg.init()
pg.mixer.init()

# audio
pg.mixer.music.load("kahoot.mp3")
pg.mixer.music.play(-1)
pg.mixer.music.pause()

# display
info = pg.display.Info()
WINDOW_W, WINDOW_H = info.current_w, info.current_h
window = pg.display.set_mode((WINDOW_W, WINDOW_H))

# ---------- obstacle / layout constants ----------
OBSTACLE_HEIGHT = 200
OBSTACLE_Y = int(WINDOW_H * 0.85) - 50  # bottom y for obstacles
SPAWN_OFFSET = 50  # spawn off-screen offset

class Obstacle(pg.Rect):
    def __init__(self, img_surface, obstacle_x, width):
        # position top so bottom aligns at OBSTACLE_Y
        super().__init__(int(obstacle_x), OBSTACLE_Y - OBSTACLE_HEIGHT, int(width), OBSTACLE_HEIGHT)
        self.img = img_surface
        self.passed = False

# ---------- start screen ----------
def startScreen():
    pg.display.set_caption("Start Menu")
    bg_img = pg.image.load("start.png").convert()
    bg_img = pg.transform.scale(bg_img, (WINDOW_W, WINDOW_H))

    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(); exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return

        window.blit(bg_img, (0, 0))
        pg.display.update()
        clock.tick(60)

# ---------- quiz config (drop-in block) ----------
CHECKPOINT_XS = [2319, 4016, 7431, 10834, 17256, 19349, 24752, 30806, 33012, 34992]
QUIZ_ANSWERS  = ['D','B','C','C','A','A','D','D','A','A']
WRONG_FLASH_MS = 700

QUIZ_IMAGES = []
for i in range(len(CHECKPOINT_XS)):
    qimg = pg.image.load(f"q{i+1}.png").convert_alpha()
    target_h = int(WINDOW_H * 0.7)
    target_w = int(qimg.get_width() * (target_h / qimg.get_height()))
    qimg = pg.transform.smoothscale(qimg, (target_w, target_h))
    QUIZ_IMAGES.append(qimg)

_OVERLAY = pg.Surface((WINDOW_W, WINDOW_H), pg.SRCALPHA)
_OVERLAY.fill((0, 0, 0, 140))

def _center_xy(surf):
    r = surf.get_rect()
    return (WINDOW_W - r.width)//2, (WINDOW_H - r.height)//2

_KEY2LETTER = {pg.K_a: 'A', pg.K_b: 'B', pg.K_c: 'C', pg.K_d: 'D'}

# ---------- game with quiz (merged) ----------
def game_with_quiz():
    pg.display.set_caption("Rev Run")
    clock = pg.time.Clock()

    # obstacle timer (we still set it; spawn only when appropriate)
    CREATE_OBSTACLE_TIMER = pg.USEREVENT + 0
    pg.time.set_timer(CREATE_OBSTACLE_TIMER, 2000)  # every 2s

    # background
    bg_img = pg.image.load("background.jpg").convert()
    bg_img = pg.transform.scale(bg_img, (bg_img.get_width(), WINDOW_H))
    scroll = 0
    tiles = math.ceil(WINDOW_W / bg_img.get_width()) + 1

    # HUD / assets
    clock_img = pg.image.load("clock.png").convert_alpha()
    clock_img = pg.transform.scale(clock_img, (int(406.2), int(221.4)))

    startButton = pg.image.load("startButton.png").convert_alpha()
    startButton = pg.transform.scale(startButton, (990, 342))
    start_btn_rect = startButton.get_rect(center=(WINDOW_W//2, int(WINDOW_H*0.48)))

    font = pg.font.SysFont("Consolas", 60)

    rev_img = pg.image.load("dog2.png").convert_alpha()
    rev_img = pg.transform.scale(rev_img, (495, 270))
    rev_img_jump = pg.image.load("dog1.png").convert_alpha()
    rev_img_jump = pg.transform.scale(rev_img_jump, (495, 270))

    rev_rect = rev_img.get_rect()
    rev_rect.center = (int(WINDOW_W * 0.25), int(WINDOW_H * 0.87))
    original_Y = rev_rect.centery

    # jump params
    jumps_left = 2
    jump_height = 300
    disp_PopUp = False
    popUp_start = 0
    popUp_dur = 700

    # load & scale obstacle helper
    def load_scaled_obstacle(path):
        surf = pg.image.load(path).convert_alpha()
        og_w, og_h = surf.get_size()
        new_w = int(og_w * (OBSTACLE_HEIGHT / og_h))
        return pg.transform.smoothscale(surf, (new_w, OBSTACLE_HEIGHT))

    possObstacles = [
        load_scaled_obstacle("bench.png"),
        load_scaled_obstacle("duck.png"),
        load_scaled_obstacle("scooter.png"),
        load_scaled_obstacle("person1.png")
    ]

    obstacles = []
    PIPE_SPEED = -10  # negative -> move left

    def move_obstacles(active=True):
        # only move/remove when active
        if not active:
            return
        for obs in obstacles[:]:
            obs.x += PIPE_SPEED
            # debug: uncomment if you want terminal feedback
            # print(f"obs.x = {obs.x}")
            if obs.right < 0:
                obstacles.remove(obs)

    def create_obstacle_instance():
        surf = possObstacles[random.randint(0, len(possObstacles)-1)]
        spawn_x = WINDOW_W + SPAWN_OFFSET
        width = surf.get_width()
        new_obs = Obstacle(surf, spawn_x, width)
        obstacles.append(new_obs)
        # print("spawned, total:", len(obstacles))

    # sounds
    alarm = pg.mixer.Sound("alarmBeep.mp3")
    jumpSound = pg.mixer.Sound("jump.mp3")
    alarm.set_volume(1.0)
    jumpSound.set_volume(0.2)
    alarm.play(-1)

    # game / quiz state
    gameStarted = False
    gameEnded = False
    start_time = 0
    timer_surf = None

    # quiz variables
    SPEED = 10
    distance = 0
    quiz_active = False
    quiz_index = -1
    next_checkpoint_idx = 0
    wrong_flash_until = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit(); exit()

            # obstacle spawn event -> only spawn when running and not quiz and not ended
            if event.type == CREATE_OBSTACLE_TIMER:
                if gameStarted and (not quiz_active) and (not gameEnded):
                    create_obstacle_instance()

            # If quiz active: only accept quiz keys A/B/C/D
            if quiz_active:
                if event.type == pg.KEYDOWN and event.key in _KEY2LETTER:
                    choice = _KEY2LETTER[event.key].upper()
                    correct = QUIZ_ANSWERS[quiz_index]
                    if choice == correct:
                        quiz_active = False
                        quiz_index = -1
                        jumps_left = 2
                        wrong_flash_until = 0
                    else:
                        wrong_flash_until = pg.time.get_ticks() + WRONG_FLASH_MS
                # ignore other inputs while quiz is active
                continue

            # normal game input (when quiz not active)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and gameStarted and (not gameEnded):
                    if jumps_left > 0:
                        disp_PopUp = True
                        popUp_start = pg.time.get_ticks()
                        jumpSound.play()
                        jumps_left -= 1

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn_rect.collidepoint(event.pos) and not gameStarted:
                    gameStarted = True
                    start_time = pg.time.get_ticks()
                    alarm.stop()
                    pg.mixer.music.unpause()

        # ---------- RENDER ----------
        if not gameStarted:
            window.blit(bg_img, (0, 0))
            window.blit(rev_img, rev_rect)
            window.blit(startButton, start_btn_rect)
            window.blit(clock_img, (960, 450))

            # optionally show obstacles on start screen (they won't move)
            for obs in obstacles:
                window.blit(obs.img, obs)

        else:
            # When quiz_active we "freeze" movement: no scrolling and obstacles don't move.
            if (not quiz_active) and (not gameEnded):
                # scrolling background
                for i in range(tiles):
                    window.blit(bg_img, (bg_img.get_width()*i + scroll, 0))
                scroll -= SPEED

                # distance progressed (positive)
                distance = -scroll
                # keep scroll bounded (wrap/reset logic to avoid overflow)
                if abs(scroll) > bg_img.get_width():
                    scroll = 0
                    # keep distance continuous by not losing the accumulated value
            else:
                # frozen background (still draw it where it is)
                for i in range(tiles):
                    window.blit(bg_img, (bg_img.get_width()*i + scroll, 0))

            # end condition (your original "reaches zach" logic)
            if (not gameEnded) and abs(scroll) > bg_img.get_width() - 1800:
                scroll = -(bg_img.get_width() - 1800)
                gameEnded = True

            # Stopwatch (always updates while game is started)
            elapsed_sec = (pg.time.get_ticks() - start_time) // 1000
            minutes = elapsed_sec // 60
            seconds = elapsed_sec % 60
            timer_color = (255, 0, 0) if pg.time.get_ticks() < wrong_flash_until else (0, 0, 0)
            timer_surf = font.render(f"{minutes:02}:{seconds:02}", True, timer_color)
            window.blit(timer_surf, (50, 50))

            # Jump animation (only when not quiz_active)
            if (not quiz_active) and disp_PopUp:
                t = pg.time.get_ticks() - popUp_start
                if t > popUp_dur:
                    disp_PopUp = False
                    rev_rect.centery = original_Y
                    jumps_left = 2
                else:
                    half = popUp_dur / 2
                    if t < half:
                        rev_rect.centery = original_Y - int(jump_height * (t / half))
                    else:
                        rev_rect.centery = original_Y - int(jump_height * (1 - (t - half) / half))

            # Draw player
            window.blit(rev_img_jump if (disp_PopUp and not quiz_active) else rev_img, rev_rect)

            # Draw & move obstacles: they move only when no quiz and not ended
            for obs in obstacles:
                window.blit(obs.img, obs)
            move_obstacles(active=(not quiz_active) and (not gameEnded))

            # trigger quiz when we pass the next checkpoint (distance must be >= checkpoint)
            if (not quiz_active) and (next_checkpoint_idx < len(CHECKPOINT_XS)):
                if distance >= CHECKPOINT_XS[next_checkpoint_idx]:
                    quiz_active = True
                    quiz_index = next_checkpoint_idx
                    next_checkpoint_idx += 1

            # Draw quiz overlay if active
            if quiz_active:
                window.blit(_OVERLAY, (0, 0))
                qimg = QUIZ_IMAGES[quiz_index]
                qx, qy = _center_xy(qimg)
                window.blit(qimg, (qx, qy))
                hint = font.render("Press A / B / C / D", True, (255, 255, 255))
                hint_rect = hint.get_rect(center=(WINDOW_W//2, qy + qimg.get_height() + 30))
                window.blit(hint, hint_rect)

        pg.display.update()
        clock.tick(60)

# ---------- run ----------
startScreen()
game_with_quiz()
