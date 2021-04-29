import pygame
from Obstacle import Obstacle, VirtualObstacle
from Player import Player, VirtualPlayer
from Coin import Coin, VirtualCoin

LOSS_SCORE = -1000000

class Gamestate():
	"""docstring for Gamestate"""
	def __init__(self, DISPLAYSURF, speed, score, time, sprite_group):
		self.DISPLAYSURF = DISPLAYSURF
		self.speed = speed
		self.score = score
		self.time = time%1000 #time since last speed increase in milliseconds
		self.environment_sprites = pygame.sprite.Group()
		self.obstacles = pygame.sprite.Group()
		self.coins = pygame.sprite.Group()
		self.gameover = False

		for sprite in sprite_group:
			virtual_sprite = sprite.get_virtual_copy()
			
			#if it is the player object save it for player use
			if isinstance(virtual_sprite, VirtualPlayer):
				self.player = virtual_sprite
			#otherwise add to environment sprites and specific spritegroup
			else:
				self.environment_sprites.add(virtual_sprite)
				if isinstance(virtual_sprite, VirtualObstacle):
					self.obstacles.add(virtual_sprite)
				elif isinstance(virtual_sprite, VirtualCoin):
					self.coins.add(virtual_sprite)


	def check_coin_collision(self):
		collided_coin = pygame.sprite.spritecollideany(self.player, self.coins)
		if collided_coin != None and collided_coin.visible:
			self.score += 1
			collided_coin.setVisible(False)

	def end_game(self):
		for sprite in self.environment_sprites:
			sprite.kill()
		self.player.kill()

	def get_score(self):
		return self.score

	#returns list with centers (x, y) of all obstacles
	def get_obstacles(self):
		obstacle_list = []
		for obstacle in self.obstacles:
			obstacle_list.append(obstacle.rect.center)
		return obstacle_list

	#returns list with centers (x, y) of all coins
	def get_coins(self):
		coin_list = []
		for coin in self.coins:
			coin_list.append(coin.rect.center)
		return coin_list

	#returns center (x, y) of player
	def get_player(self):
		return self.player.rect.center

	"""
	Advances gamestate exactly one tick, assumes 60 FPS for events
	action == 0: Nothing
	action == 1: Left
	action == 2: Right
	"""
	def advance(self, action):
		if not self.gameover:
			if self.time > 1000:
				self.speed += 0.5
				self.time = self.time%1000 
			
			# To be run if collision occurs between Player and Obstacle
			if pygame.sprite.spritecollideany(self.player, self.obstacles):
				self.gameover = True
				self.end_game()
				
			score = self.check_coin_collision()
			
			# Moves and Re-draws all Sprites
			self.environment_sprites.update()
			self.player.move(action)

			self.time += (1000/60) #1000ms/FPS
		else:
			print("Gamestate already in gameover")

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

state = Gamestate(DISPLAYSURF, speed, score, 975, all_sprites)

player = state.get_player()
obstacles = state.get_obstacles()
coins = state.get_coins()
print("Time: {}".format(state.time))
print("Speed: {}".format(state.speed))
print("Player:{} \nObstacles: {} \nCoins:{} \n".format(player, obstacles, coins))

state.advance(1)
player = state.get_player()
obstacles = state.get_obstacles()
coins = state.get_coins()
print("Time: {}".format(state.time))
print("Speed: {}".format(state.speed))
print("Player:{} \nObstacles: {} \nCoins:{} \n".format(player, obstacles, coins))

state.advance(2)
player = state.get_player()
obstacles = state.get_obstacles()
coins = state.get_coins()
print("Time: {}".format(state.time))
print("Speed: {}".format(state.speed))
print("Player:{} \nObstacles: {} \nCoins:{} \n".format(player, obstacles, coins))

state.advance(0)
player = state.get_player()
obstacles = state.get_obstacles()
coins = state.get_coins()
print("Time: {}".format(state.time))
print("Speed: {}".format(state.speed))
print("Player:{} \nObstacles: {} \nCoins:{} \n".format(player, obstacles, coins))

state.advance(1)
player = state.get_player()
obstacles = state.get_obstacles()
coins = state.get_coins()
print("Time: {}".format(state.time))
print("Speed: {}".format(state.speed))
print("Player:{} \nObstacles: {} \nCoins:{} \n".format(player, obstacles, coins))

state.advance(1)
player = state.get_player()
obstacles = state.get_obstacles()
coins = state.get_coins()
print("Time: {}".format(state.time))
print("Speed: {}".format(state.speed))
print("Player:{} \nObstacles: {} \nCoins:{} \n".format(player, obstacles, coins))