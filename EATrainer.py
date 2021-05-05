# Imports
import pygame, sys
from pygame.locals import *
import time
import random

# Import other classes
from Background import Background
from Obstacle import Obstacle
from Player import Player
from Coin import Coin
from Gamestate import Gamestate
from EAPlayer import EAPlayer, Player

class EATrainer():
    def __init__(self, pop_size, generations):
        pygame.init()
        self.SCREEN_WIDTH = 500
        self.SCREEN_HEIGHT = 700
        self.DISPLAYSURF = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        
        self.speed = 5

        self.pop_size = pop_size
        self.generations = generations

        self.init_gamestates()
        self.init_players()

    def init_gamestates(self):
        self.gamestates = list()

        all_sprites = pygame.sprite.Group()
        P1 = Player(self.DISPLAYSURF)
        E1 = Obstacle(self.DISPLAYSURF, self.speed, 40, 70, 0)         
        E2 = Obstacle(self.DISPLAYSURF, self.speed, 405, 50, -350)
        C1 = Coin(self.DISPLAYSURF, self.speed, 20, 20, 700)
        all_sprites.add(P1, E1, E2, C1)
        state = Gamestate(self.DISPLAYSURF, self.speed, 0, 0, all_sprites)

        for i in range(self.pop_size):
            self.gamestates.append(state.copy())

    def init_players(self):
        self.players = list()

        for i in range(self.pop_size):
            self.players.append(EAPlayer(self.DISPLAYSURF))

    def run_game(self):
        players_living = [not state.is_gameover() for state in self.gamestates]#list of booleans where players_living[i] is True if player i is living
        any_living = any(players_living)

        while any_living:
            for i in range(self.pop_size):
                action = self.players[i].update(self.gamestates[i])
                self.gamestates[i].advance(action)
            players_living = [not state.is_gameover() for state in self.gamestates]
            any_living = any(players_living)

    def mutate_agents(self):
        for player in self.players:
            player.mutate(0.1, 0.2)
            print(player.get_child())
            break



trainer = EATrainer(10,100)
trainer.mutate_agents()