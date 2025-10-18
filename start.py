import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
alarmScreen = pygame.image.load('alarm.png')
startScreen = pygame.image.load('start.png').convert()
white = (230,230,255)
# Fonts
font_large = pygame.font.SysFont("Arial", 100)


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
    time.sleep(1)
    #TODO alarm Sound

    #Message
    screen.fill(white)
    show_message("You have to get to class on time", 500, font_large, [0,0,0])
    pygame.display.flip()
    time.sleep(.8)
    screen.fill(white)
    screen.blit(startScreen,(0,0))
    pygame.display.flip()
    # Step 3: Start game screen
    waiting = True
    while waiting:
        screen.fill(white)
        screen.blit(startScreen,(0,0))
        pygame.display.flip()

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
        show_message("Game Running... (replace with your dino logic)", HEIGHT//2, font_small)
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