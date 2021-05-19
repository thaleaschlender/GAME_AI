# Imports
import pygame, sys
from pygame.locals import *
import time
import random
import numpy as np

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
        living = self.pop_size

        while living > 0:
            #Advance any living players
            for i in range(self.pop_size):
                if not self.gamestates[i].is_gameover():
                    action = self.players[i].update(self.gamestates[i])
                    self.gamestates[i].advance(action)
                    if self.gamestates[i].is_gameover():
                        living -= 1
                        if living%25 == 0:
                            print('Players left: {}'.format(living))

                        self.players[i].fitness += self.gamestates[i].get_score()

    def normalize_fitness(self):
        scores = list()
        for player in self.players:
            scores.append(player.fitness)

        normalized_scores = scores/np.linalg.norm(scores)
        for i in range(self.pop_size):
            self.players[i].fitness = normalized_scores[i]

    #Select one player and return its index, higher fitness means higher chance of getting picked
    #Assumes a reversely sorted playerlist
    def select_one(self):
        index = 0
        total = 0

        random = np.random.random()
        while total < random and index <= self.pop_size:
            total += self.players[index].fitness
            index += 1

        return index-1

    def evolve(self, mutation_rate_child=0.5, mutation_rate_weights=0.1, scale=0.2):
        self.players.sort(key=lambda x: x.fitness, reverse=True)
        print('Best performing player has fitness: {}'.format(self.players[0].fitness))
        self.normalize_fitness()

        
        new_players = list()
        for _ in range(self.pop_size):
            #Selecte a player and get its child
            selected_player = self.players[self.select_one()]
            child = selected_player.get_child()

            #Mutate child based on child mutation rate, then add it to the new players
            if np.random.random() < mutation_rate_child:
                child.mutate(mutation_rate_weights, scale)
            new_players.append(child)

        self.players = new_players

    def train(self, mutation_rate_child=0.5, mutation_rate_weights=0.1, scale=0.2):
        self.init_players()

        #generate new games, let players play and then evolve
        for i in range(self.generations):
            print('================== Gen: {} =================='.format(i+1))
            self.init_gamestates()
            self.run_game()
            self.evolve(mutation_rate_child=mutation_rate_child, 
                        mutation_rate_weights=mutation_rate_weights, 
                        scale=scale)

        #Play games one more time to find the best
        self.init_gamestates()
        self.run_game()
        self.players.sort(key=lambda x: x.fitness, reverse=True)
        self.players[0].save('best_fit{}_pop{}_gens{}_mrc{}_mrw{}_ms{}'
                            .format(np.round(self.players[0].fitness, decimals=1),
                                    self.pop_size, 
                                    self.generations,
                                    mutation_rate_child,
                                    mutation_rate_weights,
                                    scale))


trainer = EATrainer(250,15)
trainer.train(mutation_rate_child=0.9, mutation_rate_weights=0.3, scale=0.7)
# trainer.init_players()
# trainer.init_gamestates()
# trainer.run_game()
# trainer.select_one()