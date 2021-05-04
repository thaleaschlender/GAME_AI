import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' #im not running it on gpu, i get it
from keras.layers import Dense
from keras.models import Sequential
import pygame
from Player import Player
from Obstacle import Obstacle
from Coin import Coin
from Gamestate import Gamestate

""" 
Input layer consists of following nodes
0: Player y
1-3: Obstacle1 height, leftside, rightside
4-6: Obstacle2 height, leftside, rightside 
7-8: Coin x, coin y
Output layer can predict any of the 3 actions:
0: Nothing
1: Left
2: Right
"""
class EAPlayer(Player):
	def __init__(self, DISPLAYSURF):
		super().__init__(DISPLAYSURF)

		self.brain = Sequential()
		self.brain.add(Dense(9, activation='relu', input_shape=(9,)))
		self.brain.add(Dense(8, activation='relu'))
		self.brain.add(Dense(3, activation='sigmoid'))
		self.brain.compile()


	def update(self, state):
		#get all necessary input variables
		player_x = self.rect.centerx

		wide_obstacle = state.get_wide_obstacle()
		wide_obstacle_height = wide_obstacle[0]
		wide_obstacle_left = wide_obstacle[1]
		wide_obstacle_right = wide_obstacle[2]
		
		tall_obstacle = state.get_tall_obstacle()
		tall_obstacle_height = tall_obstacle[0]
		tall_obstacle_left = tall_obstacle[1]
		tall_obstacle_right = tall_obstacle[2]
		
		coin = state.get_coins()[0] #assumes one coin, will not work otherwise
		coin_x = coin[0]
		coin_y = coin[1]

		state_array = np.array([[player_x,
					wide_obstacle_height, wide_obstacle_left, wide_obstacle_right,
					tall_obstacle_height, tall_obstacle_left, tall_obstacle_right,
					coin_x, coin_y]])
		prediction = np.argmax(self.brain(state_array)[0]) #select class with highest probability
		self.move(prediction)
		self.draw()