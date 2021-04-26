import pygame
from Obstacle import Obstacle, VirtualObject
from Player import Player
from Coin import Coin

class Gamestate():
	"""docstring for Gamestate"""
	def __init__(self, DISPLAYSURF, speed, score, sprite_group):
		self.DISPLAYSURF = DISPLAYSURF
		self.speed = speed
		self.score = score
		self.all_sprites = pygame.sprite.Group()

		for sprite in sprite_group:
			if isinstance(sprite, Obstacle):
				self.all_sprites.add(sprite.get_virtual_copy())
			elif isinstance(sprite, Player):
				print("Its a player")
			elif isinstance(sprite, Coin):
				print("Its a coin")

DISPLAYSURF = pygame.display.set_mode((500, 700))
score = 0
speed = 5

P1 = Player(DISPLAYSURF) #defines the player object
E1 = Obstacle(DISPLAYSURF, speed, 40, 70, 0) #defines the original obstacles object spawing when we enter a new "screen scene" in the game
#E2 = Obstacle(SCREEN_WIDTH,SCREEN_HEIGHT/2,SPEED) #obstacle that could be used for spawning random obstacles (e.g. vortex)
E3 = Obstacle(DISPLAYSURF, speed, 405, 50, -350)
C1 = Coin(DISPLAYSURF, speed, 20, 20, 0)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
#all_sprites.add(E2)
all_sprites.add(E3)
all_sprites.add(C1)

Gamestate(DISPLAYSURF, speed, score, all_sprites)