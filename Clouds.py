import pygame
from PCG import *


class Clouds():

    def __init__(self, DISPLAYSURF):

        noise = ds_algorithm(513, 128)
        pcg_clouds(noise)

        self.bgimage = pygame.image.load('pcg_clouds.png')
        self.bgimage = pygame.transform.scale(self.bgimage, DISPLAYSURF.get_size())
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0

        self.moving_speed = 5

        self.DISPLAYSURF = DISPLAYSURF

    def update(self):
        self.bgY1 += self.moving_speed * 0.5
        # self.bgY1 += 0
        self.bgY2 += self.moving_speed * 0.5
        # self.bgY2 += 0
        if self.bgY1 >= self.rectBGimg.height:
            self.bgY1 = -self.rectBGimg.height
        if self.bgY2 >= self.rectBGimg.height:
            self.bgY2 = -self.rectBGimg.height

        self.draw()

    def static(self):
        self.bgY1 += self.moving_speed
        self.bgY2 += self.moving_speed
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
