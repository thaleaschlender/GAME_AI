import pygame
from pygame.locals import *

class VirtualPlayer(pygame.sprite.Sprite):
    """Virtual parent class of player that has all the same variables and functions
    except anything required with drawing to screen."""
    def __init__(self, DISPLAYSURF, center):
        super().__init__()
        self.DISPLAYSURF = DISPLAYSURF
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.DISPLAYSURF.get_size()

        self.width = 50
        self.height = 76
        self.surf = pygame.Surface((self.width, self.height))

    #updates obstacle for exactly one tick
    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < self.SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)
        

#extends from the sprite class
class Player(VirtualPlayer):
    def __init__(self, DISPLAYSURF):
        super().__init__(DISPLAYSURF, (0, 0))
        self.image = pygame.image.load("bird.png")
        self.rect = self.surf.get_rect(center=(self.SCREEN_WIDTH/2, (self.SCREEN_HEIGHT - 75)))

    def update(self):
        self.draw()
        super().update()

    def draw(self):
        self.DISPLAYSURF.blit(self.image, self.rect)        

    #return virtualcopy of self for gamestate
    def get_virtual_copy():
        new_player = VirtualPlayer(self.DISPLAYSURF, self.rect.center)
        return new_player