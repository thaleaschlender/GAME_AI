import pygame
from pygame.locals import *
#extends from the sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__()
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        #set appearence
        self.width = 50; self.height = 76
        #self.image = pygame.Surface([self.width, self.height])
        #self.image.fill((0,0,255))
        self.image = pygame.image.load("bird.png")
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH/2, (SCREEN_HEIGHT - 75)))

    def update(self):
        pressed_keys = pygame.key.get_pressed()



        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < self.SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)