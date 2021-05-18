import random

import pygame


class VirtualObstacle(pygame.sprite.Sprite):
    """Virtual parent class of obstacle that has all the same variables and functions
    except anything required with drawing to screen."""

    # constructor
    def __init__(self, DISPLAYSURF, speed, width, height, center):
        super().__init__()  # initialise from the parent class
        self.DISPLAYSURF = DISPLAYSURF

        # takes in the width and height of the game screen / scene
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.DISPLAYSURF.get_size()
        self.speed = speed  # determines the speed according to the parameter entered
        self.passed = False
        self.surf = pygame.Surface((width, height))  # determines the size of the surfable surface

        self.rect = self.surf.get_rect(center=center)

    # updates obstacle for exactly one tick
    def update(self):
        # determines the speed of vertical movement only, to "accompany" the background
        self.rect.move_ip(0, self.speed)
        if (self.rect.top > self.SCREEN_HEIGHT):  # Condition to determine the placement of the obstacle after every tick
            self.rect.top = 0  # determines the position of the top of the rectangle on the scene
            # determines the position of the center of the rectangle on the scene
            self.rect.center = (random.randint(40, self.SCREEN_WIDTH - 40), 0)
            self.passed = False

    # return virtualcopy of self for gamestate
    def get_virtual_copy(self):
        virtual_obstacle = VirtualObstacle(self.DISPLAYSURF, self.speed,
                                           self.surf.get_width(), self.surf.get_height(), self.rect.center)
        return virtual_obstacle


class Obstacle(VirtualObstacle):
    # initalisitation of an obstacle object with its width, height and height_position as parameters
    def __init__(self, DISPLAYSURF, speed, width, height, height_position):
        super().__init__(DISPLAYSURF, speed, width, height, (0, height_position))
        # Add appearence
        self.image = pygame.Surface([width, height])
        # self.image.fill((0,255,0))
        self.image.fill((255, 0, 0))  # red obstacles
        #self.image = pygame.image.load("picture.png")
        width_position = random.randint(40, self.SCREEN_WIDTH - 40)
        self.rect.centerx = width_position

    def update(self):
        self.draw()
        super().update()

    def draw(self):
        self.DISPLAYSURF.blit(self.image, self.rect)

    # return virtualcopy of self for gamestate
    def get_virtual_copy(self):
        virtual_obstacle = VirtualObstacle(self.DISPLAYSURF, self.speed,
                                           self.surf.get_width(), self.surf.get_height(), self.rect.center)
        return virtual_obstacle
