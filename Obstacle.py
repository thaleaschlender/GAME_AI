import random

import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SPEED, gap_center, position):
        super().__init__()
        #Add appearence
        self.width = 400
        self.height = 70
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((0,255,0))
        #self.image = pygame.image.load("picture.png")
        self.surf = pygame.Surface((self.width, self.height))
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SPEED = SPEED

        if position == 'left':
            x = gap_center-75-(self.width/2)
        elif position == 'right':
            x = gap_center+75+(self.width/2)
        y = -65
        self.rect = self.surf.get_rect(center=(x, y))
        self.out_of_bounds = False

    def update(self):
        self.rect.move_ip(0, self.SPEED)
        if (self.rect.top > self.SCREEN_HEIGHT):
            self.out_of_bounds = True



