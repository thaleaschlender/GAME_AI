import random

import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self,SCREEN_WIDTH,SCREEN_HEIGHT,SPEED, width, height, height_position): #initalisitation of an obstacle object with its width, height and height_position as parameters
        super().__init__()
        #Add appearence
        self.image = pygame.Surface([width, height])
        self.image.fill((255,255,0))
        self.surf = pygame.Surface((width, height))
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SPEED = SPEED
        self.rect = self.surf.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40)
                                               , height_position))



    def move(self):
        self.rect.move_ip(0, self.SPEED)
        if (self.rect.top > self.SCREEN_HEIGHT):
            self.resetToTop()

    def resetToTop(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, self.SCREEN_WIDTH - 40), 0)


