import pygame


class Background():

    def __init__(self, DISPLAYSURF):

        self.bgimage = pygame.image.load('background.png')
        self.rectBGimg = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = self.rectBGimg.height
        self.bgX2 = 0


        self.moving_speed = 5

        self.DISPLAYSURF = DISPLAYSURF

    def update(self):
        self.bgY1 -= self.moving_speed
        self.bgY2 -= self.moving_speed
        if self.bgY1 <= -self.rectBGimg.height:
            self.bgY1 = self.rectBGimg.height
        if self.bgY2 <= -self.rectBGimg.height:
            self.bgY2 = self.rectBGimg.height

    def render(self):
        self.DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
        self.DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))


