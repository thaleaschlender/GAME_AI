import pygame
from pygame.locals import *
#extends from the sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self, DISPLAYSURF):
        super().__init__()
        self.DISPLAYSURF = DISPLAYSURF
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.DISPLAYSURF.get_size()
        #set appearence
        self.width = 50; self.height = 76
        #self.image = pygame.Surface([self.width, self.height])
        #self.image.fill((0,0,255))
        self.image = pygame.image.load("bird.png")
        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect(center=(self.SCREEN_WIDTH/2, (self.SCREEN_HEIGHT - 75)))

    def update(self):
        self.draw()

        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < self.SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def draw(self):
        self.DISPLAYSURF.blit(self.image, self.rect)
