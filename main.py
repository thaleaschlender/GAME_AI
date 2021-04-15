# Imports
import pygame, sys
from pygame.locals import *
import time

# Import other classes
from Background import Background
from Obstacle import Obstacle
from Player import Player

pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()


# Other Variables for use in the program
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
SPEED = 5
SCORE = 0

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, WHITE)

# Create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Group 15")


# Setting up Sprites
P1 = Player(SCREEN_WIDTH, SCREEN_HEIGHT)

E1 = Obstacle(SCREEN_WIDTH,SCREEN_HEIGHT,SPEED)

back_ground = Background(SCREEN_WIDTH,SCREEN_HEIGHT,DISPLAYSURF)

# Creating Sprites Groups
obstacles = pygame.sprite.Group()
obstacles.add(E1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# Adding a new User event: how often to look for user event?
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
while True:

    # Cycles through all occurring events
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    back_ground.update()
    back_ground.render()

    # DISPLAYSURF.blit(background, (0,0))
    #display a score
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # To be run if collision occurs between Player and Obstacle
    if pygame.sprite.spritecollideany(P1, obstacles):
        # a sound can be played
        #pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.8)

        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(game_over, (SCREEN_WIDTH/10, SCREEN_HEIGHT/4))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(1.5)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)