import pygame
import random
from pygame.locals import *

wind_timer = 300 #variables used to determine the value of the wind timer

class VirtualPlayer(pygame.sprite.Sprite):
    """Virtual parent class of player that has all the same variables and functions
    except anything required with drawing to screen."""
    def __init__(self, DISPLAYSURF, center):
        super().__init__()
        self.DISPLAYSURF = DISPLAYSURF
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.DISPLAYSURF.get_size()
        self.width = 50 #defines the width of the player
        self.height = 76 #defines the height of the player
        self.surf = pygame.Surface((self.width, self.height)) #defines the player as a surface element in the game
        self.timing = wind_timer  # timing variable is used to let each wind occur for the amount of time defined by wind_timer
        self.random_winds = random.randint(-2,
                                           2)  # creates a random wind variable representing the strength of the wind and the direction
        self.rect = self.surf.get_rect(center=center)


    #updates obstacle for exactly one tick
    def update(self):
        pressed_keys = pygame.key.get_pressed()
        
        self.winds()
        
        if pressed_keys[K_LEFT]:
            self.move(1)
        if pressed_keys[K_RIGHT]:
            self.move(2)

    """ 
    action == 0: Nothing
    action == 1: Left
    action == 2: Right
    """
    def move(self, action):
        if action == 1:
            if self.rect.left > 0: 
                self.rect.move_ip(-5, 0)
        elif action == 2:
            if self.rect.right < self.SCREEN_WIDTH:
                if self.rect.right > 0:
                    self.rect.move_ip(5, 0)
                
    # Return virtualcopy of self for gamestate
    def get_virtual_copy(self):
        new_player = VirtualPlayer(self.DISPLAYSURF, self.rect.center)
        # Set current active winds for the virtual player
        new_player.setWinds(self.timing, self.random_winds)
        return new_player
    
    # Set wind variables
    def setWinds(self, timing, random_winds):
        self.timing = timing
        self.random_winds = random_winds

    # Handle The winds applied to the player
    # Should be called from update method of the child classes.
    def winds(self):
        # print(self.timing) #used to print the value of the wind timer for troubleshooting purposes
        
        # Check if wind timer is at the start
        if self.timing == wind_timer:
            # Create a new wind only 50% of the time
            # Note that additionally, randomInt can return 0 20% of the time,
            # which also means that no wind is created
            if random.random() < 0.5:
                self.random_winds = random.randint(-2, 2)
            
        
        # Apply wind to the player
        self.applyWind(self.random_winds)

        # Update wind timer
        self.timing = self.timing - 1

        # if the timer used for the wind reaches 0 go back to the value defined by wind_timer
        # Also resets applied wind
        if self.timing == 0:  
            self.timing = wind_timer
            self.random_winds = 0

    
    
    # Apply wind to the player
    def applyWind(self, windPower):
        # No active wind
        if (windPower == 0):
            return
        # Wind pushes to the left
        if (windPower < 0):
            if self.rect.left > 0: 
                self.rect.move_ip(windPower, 0)
                
        # Wind pushes to the right
        else:
            if self.rect.right < self.SCREEN_WIDTH:
                self.rect.move_ip(windPower, 0)
        

#extends from the sprite class
class Player(VirtualPlayer):
    def __init__(self, DISPLAYSURF):
        super().__init__(DISPLAYSURF, (0, 0))

        self.image = pygame.image.load("bird.png")  # determines what sprite is used as the player
        self.rect = self.surf.get_rect(center=(self.SCREEN_WIDTH / 2, (self.SCREEN_HEIGHT - 75)))  # determines the position of the player according to its center

    def update(self, state):
        super().update() #updates the position of the player on the scene
        self.draw()

    def draw(self):
        self.DISPLAYSURF.blit(self.image, self.rect)        