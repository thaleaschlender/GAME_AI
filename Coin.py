import random

import pygame

class VirtualCoin(pygame.sprite.Sprite):
    """Virtual parent class of coin that has all the same variables and functions
    except anything required with drawing to screen."""
    def __init__(self, DISPLAYSURF, speed, width, height, center):
        super().__init__()
        self.DISPLAYSURF = DISPLAYSURF
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.DISPLAYSURF.get_size()
        self.speed = speed

        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_rect(center=center)

    #updates object exactly one tick
    def update(self):
        self.rect.move_ip(0, self.speed)
        if (self.rect.top > self.SCREEN_HEIGHT):
            self.resetToTop()

    def resetToTop(self):
        self.rect.top = 0
        self.rect.center = (random.randint(40, self.SCREEN_WIDTH - 40), 0)

        

class Coin(VirtualCoin):
    def __init__(self, DISPLAYSURF, speed, width, height, height_position): #initalisitation of an obstacle object with its width, height and height_position as parameters
        super().__init__(DISPLAYSURF, speed, width, height, (0, height_position))
        #Add appearence
        self.image = pygame.Surface([width, height])
        self.image.fill((255,255,0))

        width_position = random.randint(40, self.SCREEN_WIDTH - 40)
        self.rect.centerx = width_position

    def update(self):
        self.draw()
        super().update()  

    def draw(self):
        self.DISPLAYSURF.blit(self.image, self.rect)    

    #return virtualcopy of self for gamestate
    def get_virtual_copy():
        new_player = VirtualCoin(self.DISPLAYSURF, self.speed, 
                        self.surf.get_width(), self.surf.get_height(), self.rect.center)
        return new_player