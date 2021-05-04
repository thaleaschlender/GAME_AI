import random
from Player import Player

class RandomPlayer(Player):
    """AI Player that chooses the next action randomly."""
    def __init__(self, DISPLAYSURF, actions):
        super().__init__(DISPLAYSURF)
        self.actions = actions
    
    # Chooses next action
    def act(self):
        return random.choice(self.actions)
    
    def update(self, state):
        action = self.act()
        self.move(action)
        self.draw()