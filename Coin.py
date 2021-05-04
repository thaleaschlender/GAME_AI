import random

import pygame

# Color of the coin (YELLOW)
COIN_COLOR = (255,255,0)

class VirtualCoin(pygame.sprite.Sprite):
    """Virtual parent class of coin that has all the same variables and functions
    except anything required with drawing to screen."""
    def __init__(self, DISPLAYSURF, speed, width, height, center):
        super().__init__()
        self.DISPLAYSURF = DISPLAYSURF
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.DISPLAYSURF.get_size()
        self.speed = speed
        self.visible = True
        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_rect(center=center)

    #updates object exactly one tick
    def update(self):
        self.rect.move_ip(0, self.speed)
        if (self.rect.top > self.SCREEN_HEIGHT):
            self.resetToTopOfScreen()

    # Check if coin overlaps with the obstacles
    def check_obstacle_overlap(self):
        # Check for collision with small cube obstacle
        if (self.rectangleObstacle.rect.colliderect(self.rect)):
            # Check if there is room on the left of obstacle
            if (self.rectangleObstacle.rect.left - 100 < 40):
                # Put the coin to the right
                self.rect.left = self.rectangleObstacle.rect.right + 40
            # Check if there is room on the right of obstacle
            elif (self.rectangleObstacle.rect.right + 100 > self.SCREEN_WIDTH - 40):
                # Put the coin to the left
                self.rect.right = self.rectangleObstacle.rect.left - 100
            # There is room on both sides of the obstacle, decide randomly on which side to put
            elif (random.random() < 0.5):
                self.rect.left = self.rectangleObstacle.rect.right + 100
            else:
                self.rect.right = self.rectangleObstacle.rect.left - 100
        
        # Check overlap with the vertical obstacle
        if (self.verticalObstacle.rect.top - 100 < self.rect.bottom):
            # Move coin above the obstacle
            self.rect.bottom = self.verticalObstacle.rect.top - 100

        
    def resetToTopOfScreen(self):
        self.rect.center = (random.randint(40, self.SCREEN_WIDTH - 40), 0)
        self.check_obstacle_overlap()
        self.visible = True
        
    # Set the obstacles of the game, needed for avoiding overlaps between the coins and obstacles.
    def setObstacles(self, verticalObstacle, rectangleObstacle):
        self.verticalObstacle = verticalObstacle
        self.rectangleObstacle = rectangleObstacle
    
    # Set if coin is visible. Related to avoiding overlaps with obstacles. This way the coin is always
    # reset to top only when reaching the bottom of the screen. And it avoids cases where coin is put to the
    # top of the screen, but obstacle is put on top of or near the coin. Preferred it over adding Coin dependency to
    # the obstacle class.
    def setVisible(self, isVisible):
        self.visible = isVisible

    def get_virtual_copy(self):
        new_coin = VirtualCoin(self.DISPLAYSURF, self.speed, 
                        self.surf.get_width(), self.surf.get_height(), self.rect.center)
        return new_coin

class Coin(VirtualCoin):
    def __init__(self, DISPLAYSURF, speed, width, height, height_position): #initalisitation of an obstacle object with its width, height and height_position as parameters
        super().__init__(DISPLAYSURF, speed, width, height, (0, height_position))
        #Add appearence
        self.image = pygame.Surface([width, height])
        self.image.fill(COIN_COLOR)

        width_position = random.randint(40, self.SCREEN_WIDTH - 40)
        self.rect.centerx = width_position

    def update(self):
        if self.visible:
            self.draw()
        super().update()  

    def draw(self):
        self.DISPLAYSURF.blit(self.image, self.rect)    

    #return virtualcopy of self for gamestate
