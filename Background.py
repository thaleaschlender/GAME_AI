import pygame
from PCG import *
import numpy as np


class Background():
    """Background class collecting the two layers of background and combining them. This class implements the dynamic moverment of the clouds layer."""
    def __init__(self, DISPLAYSURF):

        elevation = ds_algorithm(513, 128)
        moisture = ds_algorithm(513, 128)
        pcg_bg(elevation, moisture)

        #self.bgimage = pygame.image.load('background.png')
        self.bgimage = pygame.image.load('pcg_background.png')
        self.bgimage = pygame.transform.scale(self.bgimage, DISPLAYSURF.get_size())
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        self.moving_speed = 5

        self.DISPLAYSURF = DISPLAYSURF

    def update(self):

        # self.bgY1 += self.moving_speed
        # self.bgY2 += self.moving_speed
        self.bgY1 += 0
        self.bgY2 += 0
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

        self.draw()

    def draw(self):
        self.DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
        self.DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))

    def virtual_update(self):
        self.bgY1 += self.moving_speed
        self.bgY2 += self.moving_speed
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height
