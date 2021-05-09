import random
from Player import Player
from Gamestate import Gamestate
from TreeNode import TreeNode

class MCTSPlayer(Player):
    """AI Player that uses MCTS for choosing action"""
    def __init__(self, DISPLAYSURF, actions, actionTime):
        super().__init__(DISPLAYSURF)
        self.actions = actions
        self.time = actionTime
        
        
    # Chooses next action
    def act(self, state):
        # Copy the game state
        rootState = state.copy()
        
        # Create tree root node
        rootNode = TreeNode(None, -1, self.actions, self.time)
        rootNode.setRootState(rootState)
        
        # Perform MCTS
        rootNode.mcts()
        
        # return the action with highest average score
        return rootNode.bestAction()
    
    def update(self, state):
        action = self.act(state)
        self.move(action)
        self.draw()