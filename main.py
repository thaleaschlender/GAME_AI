# Imports
import pygame
import sys
from pygame.locals import *
import time
import random

# Import other classes
from Background import Background
from Clouds import Clouds
from Obstacle import Obstacle
from Player import Player
from Coin import Coin
from Gamestate import Gamestate
from RandomPlayer import RandomPlayer
from EAPlayer import EAPlayer
from MCTSPlayer import MCTSPlayer

pygame.init()

# Setting up FPS
FPS = 60
FramePerSec = pygame.time.Clock()


# Other Variables for use in the program
BLACK = (0, 0, 0)  # defines the colour black in a variable
WHITE = (255, 255, 255)  # defines the colour white in a variable
SCREEN_WIDTH = 512  # defines the width of the game screen
SCREEN_HEIGHT = 512  # defines the height of the game screen

speed = 5  # defines the general speed of movement
score = 0  # Variable representing the score (initialised at 0 for the beginning of the game)

# Setting up Fonts
FONT = pygame.font.SysFont("Verdana", 60)
FONT_SMALL = pygame.font.SysFont("Verdana", 20)
GAME_OVER = FONT.render("Game Over", True, WHITE)

# Create a white screen
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Group 15")

# Display the current game score


def display_score(score):
    # defines the font properties of the score
    scoreText = FONT_SMALL.render(str(score), True, BLACK)
    # displays the score in the top left corner of the screen
    DISPLAYSURF.blit(scoreText, (10, 10))

# End game
# Delete all existing sprites and close window.


def end_game(sprites, score):
    # a sound can be played
    # pygame.mixer.Sound('crash.wav').play()

    finalScore = FONT.render(str(score), True, WHITE)
    print(score)

    time.sleep(0.8)
    # Fills screen with black, shows a black screen
    DISPLAYSURF.fill(BLACK)
    # Writes game over on the screen on top of the black screen
    DISPLAYSURF.blit(GAME_OVER, (SCREEN_WIDTH/10, SCREEN_HEIGHT/4))

    # Show the final score
    DISPLAYSURF.blit(finalScore, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    pygame.display.update()
    for entity in sprites:
        entity.kill()

    # wait one and a half second
    time.sleep(1.5)
    pygame.quit()  # quit pygame
    sys.exit()  # close the demo window

# Check if the player has collided with a coin
# Returns the score of the game


def check_coin_collision(player, coins, score):
    # Find the collided coin
    collidedCoin = pygame.sprite.spritecollideany(P1, coins)
    # Check if collided with any coins
    if collidedCoin != None and collidedCoin.visible:
        # Increase the score and reset coin to the top
        score += 5
        # score += 1
        # this was 1 un the background but apparently was changed
        collidedCoin.setVisible(False)

    return score

# Check if the player has passed an obstacle and increases the score if it has.
# Returns the score of the game


def check_obstacle_pass(player, obstacles, score):
    for obstacle in obstacles:
        if (not obstacle.passed and obstacle.rect.top > player.rect.center[1]):
            score += 1
            obstacle.passed = True

    return score


# Setting up Sprites

# Create the player
# P1 = Player(DISPLAYSURF) # Human player
# P1 = RandomPlayer(DISPLAYSURF, [1,2]) # Random player
# P1 = EAPlayer(DISPLAYSURF) # EA player
# P1.load_brain('./models/bestmodel_fit10.5_pop100_gens10_mrc1_mrw0.05_ms0.3')
P1 = MCTSPlayer(DISPLAYSURF, [1, 2], 40)  # MCTS Player

# defines the original obstacles object spawing when we enter a new "screen scene" in the game
E1 = Obstacle(DISPLAYSURF, speed, 40, 70, 0)

# Setting up Sprites
P1 = Player(DISPLAYSURF)  # defines the player object

# defines the original obstacles object spawing when we enter a new "screen scene" in the game
E1 = Obstacle(DISPLAYSURF, speed, 40, 70, 0)

# E2 = Obstacle(SCREEN_WIDTH,SCREEN_HEIGHT/2,SPEED) #obstacle that could be used for spawning random obstacles (e.g. vortex)

# defines the wall obstacles object spawing when we enter a new "screen scene" in the game
E3 = Obstacle(DISPLAYSURF, speed, 405, 50, -350)

# Create coins
C1 = Coin(DISPLAYSURF, speed, 20, 20, 700)
C1 = Coin(DISPLAYSURF, speed, 20, 20, 700)  # defines the coins objects
#C2 = Coin(DISPLAYSURF, speed, 20, 20, -200)
#C3 = Coin(DISPLAYSURF, speed, 20, 20, -400)
#C4 = Coin(DISPLAYSURF, speed, 20, 20, -600)

C1.setObstacles(E3, E1)

back_ground = Background(DISPLAYSURF)  # defines the background object
clouds = Clouds(DISPLAYSURF)

# Creating Sprites Groups
obstacles = pygame.sprite.Group()
obstacles.add(E1)
# obstacles.add(E2)
obstacles.add(E3)

coins = pygame.sprite.Group()
coins.add(C1)


# coins.add(C2)
# coins.add(C3)
# coins.add(C4)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
# all_sprites.add(E2)
all_sprites.add(E3)
all_sprites.add(C1)
# all_sprites.add(C2)
# all_sprites.add(C3)
# all_sprites.add(C4)

# Adding a new User event: how often to look for user event?
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
while True:
    # Cycles through all occurring events
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            speed += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    back_ground.update()
    clouds.update()

    score = check_coin_collision(P1, coins, score)
    score = check_obstacle_pass(P1, obstacles, score)

    # The State has to be created here before updating the sprites, otherwise there is mismatch by one tick
    # when simulating players
    state = Gamestate(DISPLAYSURF, speed, score, pygame.time.get_ticks(), all_sprites)
    state.set_player(P1.get_virtual_copy())

    # Moves and Re-draws all Sprites
    # all_sprites.update()
    # P1.update(state)

    # Display the score
    display_score(score)

    # To be run if collision occurs between Player and Obstacle
    if pygame.sprite.spritecollideany(P1, obstacles):
        end_game(all_sprites, score)

    score = check_coin_collision(P1, coins, score)

    # Moves and Re-draws all Sprites
    all_sprites.update()
    P1.update(state)

    pygame.display.update()
    FramePerSec.tick(FPS)
