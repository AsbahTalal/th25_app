import pygame as pg
import sys
import time

# Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("kahoot.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.pause()


# Screen setup
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
alarmScreen = pygame.image.load('alarmScreen.png')
startScreen = pygame.image.load('startScreen.png').convert()

white = (230,230,255)
# Fonts


clock = pygame.time.Clock()

def show_message(text, y, font, color=[0,0,0]):
    """Helper to render centered text"""
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH//2, y))
    screen.blit(render, rect)

def start_sequence():
    
    screen.fill(white)

    # Step 1: Alarm screen
    screen.blit(alarmScreen,((0),(0)))
    pygame.display.flip()

    #music loading alarm sound
    alarm = pygame.mixer.Sound("alarmBeep.mp3")
    pygame.mixer.Sound.set_volume(alarm,1)
    alarm.play(0)
    time.sleep(4)

    #Message
    screen.fill(white)
    pygame.display.flip()
    time.sleep(1)
    screen.fill(white)
    screen.blit(startScreen,(0,0))
    pygame.display.flip()
    # Step 3: Start game screen
    waiting = True
    while waiting:
        screen.fill(white)
        screen.blit(startScreen,(0,0))
        pygame.display.flip()

        #start the music up
        pygame.mixer.music.unpause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def main_game():
    # Placeholder for your actual game loop
    running = True
    while running:
        screen.fill(white)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    start_sequence()
    main_game()


obstacle_height = 200
obstacles = []
def create_obstacles():
    #bench
    bench_img = pg.image.load('bench.png',)
    ogWidth, ogHeight = bench_img.get_size()
    obstacle_width = int(ogHeight * (ogWidth / ogHeight))
    bench_img = pg.transform.scale((obstacle_height,obstacle_width))
    obstacles.append(bench_img)
    #duck
    duck_img = pg.image.load('duck.png',)
    ogWidth, ogHeight = duck_img.get_size()
    obstacle_width = int(ogHeight * (ogWidth / ogHeight))
    duck_img = pg.transform.scale(obstacle_height)
    obstacles.append(duck_img)
    #scooter
    scooter_img = pg.image.load('scooter.png',)
    ogWidth, ogHeight = scooter_img.get_size()
    obstacle_width = int(ogHeight * (ogWidth / ogHeight))
    scooter_img = pg.transform.scale(obstacle_height)
    obstacles.append(scooter_img)
    #person
    person1_img = pg.image.load('person1.png',)
    ogWidth, ogHeight = person1_img.get_size()
    obstacle_width = int(ogHeight * (ogWidth / ogHeight))
    person1_img = pg.transform.scale(obstacle_height)
    obstacles.append(person1_img)


obstacle_x = WIDTH #to be defined
obstacle_y = 0
obstacle_width = 0 #to be defined
obstacle_height = 0 #to be defined

class obstacle(pg.Rect):
    def __init__(self, img):
        pg.Rect.__init__(self, obstacle_x, obstacle_y, obstacle_width, obstacle_height)
        self.img = img
        self.passed = False
