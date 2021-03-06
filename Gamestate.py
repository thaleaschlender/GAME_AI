import pygame
from Obstacle import Obstacle, VirtualObstacle
from Player import Player, VirtualPlayer
from Coin import Coin, VirtualCoin
import random

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

        self.fill_spritegroups(sprite_group)

    def fill_spritegroups(self, sprite_group):
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
                    
                    #save obstacle and orientation to set for coin
                    if virtual_sprite.surf.get_width() > virtual_sprite.surf.get_height(): 
                        self.wide_obstacle = virtual_sprite
                    else:
                        self.tall_obstacle = virtual_sprite
                elif isinstance(virtual_sprite, VirtualCoin):
                    self.coins.add(virtual_sprite)

        for coin in self.coins:
            coin.setObstacles(self.tall_obstacle, self.wide_obstacle)
            #coin.rect.centerx = 250

    def check_coin_collision(self):
        collided_coin = pygame.sprite.spritecollideany(self.player, self.coins)
        if collided_coin != None and collided_coin.visible:
            self.score += 5
            collided_coin.setVisible(False)
            
    
    # Check if the player has passed an obstacle and increases the score if it has.
    # Returns the score of the game
    def check_obstacle_pass(self):
        for obstacle in self.obstacles :
            if (not obstacle.passed and obstacle.rect.top > self.player.rect.center[1]):
                self.score+=1
                obstacle.passed = True

    def end_game(self):
        for sprite in self.environment_sprites:
            sprite.kill()
        self.player.kill()

    def is_gameover(self):
        return self.gameover

    def get_score(self):
        return self.score

    #returns list with centers (x, y) of all obstacles
    def get_obstacles(self):
        obstacle_list = []
        for obstacle in self.obstacles:
            obstacle_list.append(obstacle.rect.center)
        return obstacle_list

    #return height, left and right of wide obstacle
    def get_wide_obstacle(self):
        return [self.wide_obstacle.rect.bottom, self.wide_obstacle.rect.left, self.wide_obstacle.rect.right]

    #return height, left and right of tall obstacle
    def get_tall_obstacle(self):
        return [self.tall_obstacle.rect.bottom, self.tall_obstacle.rect.left, self.tall_obstacle.rect.right]

    #returns list with centers (x, y) of all coins
    def get_coins(self):
        coin_list = []
        for coin in self.coins:
            coin_list.append(coin.rect.center)
        return coin_list

    #returns center (x, y) of player
    def get_player(self):
        return self.player.rect.center
    
    def set_player(self, virtualplayer):
        self.player = virtualplayer

    def copy(self):
        all_sprites = pygame.sprite.Group()
        all_sprites.add(self.player)
        for obstacle in self.obstacles:
            all_sprites.add(obstacle)
        for coin in self.coins:
            all_sprites.add(coin)

        return Gamestate(self.DISPLAYSURF, self.speed, self.score, self.time, all_sprites)

    """
    Advances gamestate exactly one tick, assumes 60 FPS for events
    action == 0: Nothing
    action == 1: Left
    action == 2: Right
    """
    def advance(self, action):
        if not self.gameover:
            #if self.time > 1000:
            #    self.speed += 0.5
            #    self.time = self.time%1000 
            

                

            self.environment_sprites.update()
            self.player.winds()
            self.player.move(action)
            self.check_coin_collision()
            self.check_obstacle_pass()
            
            # To be run if collision occurs between Player and Obstacle
            if pygame.sprite.spritecollideany(self.player, self.obstacles):
                self.gameover = True
                self.end_game()

            self.time += (1000/60) #1000ms/FPS
        else:
            print("Gamestate already in gameover")