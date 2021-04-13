import random

import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self,SCREEN_WIDTH,SCREEN_HEIGHT,SPEED ):
        super().__init__()
        #Add appearence
        self.image = pygame.Surface([42, 70])
        self.image.fill((0,255,0))
        #self.image = pygame.image.load("picture.png")
        self.surf = pygame.Surface((42, 70))
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.SPEED = SPEED
        self.rect = self.surf.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40)
                                               , 0))

    def move(self):
        self.rect.move_ip(0, self.SPEED)
        if (self.rect.top > self.SCREEN_HEIGHT):
            self.rect.top = 0
            self.rect.center = (random.randint(40, self.SCREEN_WIDTH - 40), 0)



