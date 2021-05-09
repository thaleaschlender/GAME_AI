import random
import math
from Player import Player
from Gamestate import Gamestate

# Defines how deep the tree is searched
ROLLOUT_DEPTH = 50

# UCT formula parameter
K = math.sqrt(2)

REPEAT_ACTIONS = 10

HUGE_NEGATIVE = -100000
HUGE_POSITIVE = 100000


EPSILON = 1e-6
GREEDYEPSILON = 0.05

class TreeNode():
    def __init__(self, parent, childIndex, actions, time):
        self.actions = actions
        self.index = childIndex
        self.parent = parent
        self.time = time
        self.childs = [None] * len(actions)
        self.totValue = 0.0
        self.childIdx = childIndex
        self.depth = 0 if parent == None else parent.depth + 1
        self.visits = 0
        self.bounds = [HUGE_POSITIVE, HUGE_NEGATIVE]
        
    def setRootState(self, gameState):
        self.rootState = gameState
    
    # Perform MCTS
    # If possible change to time limitation instead of fixed number of iterations.
    def mcts(self):
        i = 0
        while (i < 100):
            state = self.rootState.copy()
            
            # Select next node
            selected = self.treePolicy(state)
            
            # Rollout from the selected node
            delta = selected.rollOut(state)
            
            # Back up the score
            self.backUp(selected, delta)
            i+=1
    
    # Find the child that was most visited
    def mostVisited(self):
        mostVisited = 0
        mostVisitedChildIndex = 0
        for childIndex ,child in enumerate(self.childs):
            if (child == None) :
                continue
            
            if (child.visits > mostVisited):
                mostVisited = child.visits
                mostVisitedChildIndex = childIndex
                
        return self.actions[mostVisitedChildIndex]
    
    # Find the child that has highest average score
    def bestAction(self):
        bestAction = HUGE_NEGATIVE * 10
        bestActionChildIndex = 0
        
        for childIndex ,child in enumerate(self.childs):
            if (child == None) :
                continue
            childValue = child.totValue / (child.visits + EPSILON)
            
            if (childValue > bestAction):
                bestAction = childValue
                bestActionChildIndex = childIndex
                
        return self.actions[bestActionChildIndex]
        
    # Expand next node in the tree
    def treePolicy(self, state):
        cur = self
        
        while (not state.gameover and cur.depth < ROLLOUT_DEPTH):
            if (cur.notFullyExpanded()):
                return cur.expand(state)
            else:
                nextNode = cur.uct(state)
                cur = nextNode
                
        
        return cur
    
    # Rollout by choosing random actions until maximum depth has been reached or game is over
    def rollOut(self, state):
        currentDepth = self.depth
        
        while (not self.finishRollout(state, currentDepth)):
            action = random.choice(self.actions)
            for i in range(REPEAT_ACTIONS):
                if (state.gameover):
                    break
                
                state.advance(self.actions[action])
                
            currentDepth+=1
        
        delta = self.value(state)
        
        if (delta < self.bounds[0]):
            self.bounds[0] = delta
        if (delta > self.bounds[1]):
            self.bounds[1] = delta
            
        return delta
    
    # Save the score back up the tree
    def backUp(self, selectedNode, score):
        node = selectedNode
        
        while (node != None):
            node.visits += 1
            node.totValue += score
            if (score < node.bounds[0]):
                node.bounds[0] = score
            if (score > node.bounds[1]):
                node.bounds[1] = score
            node = node.parent
        
    # Find next node to explore
    def uct(self, state):
        selectedNode = None
        bestValue = HUGE_NEGATIVE * 10
        
        for child in self.childs:
            childValue = child.totValue
            averageChildValue = childValue / (child.visits + EPSILON)
            
            normalisedValue = self.normalise(averageChildValue)
            
            uctValue = normalisedValue + K * math.sqrt(math.log(self.visits + 1) / (child.visits + EPSILON))
            
            uctValue += EPSILON * random.random()
            
            if (uctValue > bestValue):
                selectedNode = child
                bestValue = uctValue
                
        

        state.advance(self.actions[selectedNode.childIdx])
        
        
        return selectedNode
    
    # Choose the next action to perform from unvisited nodes.
    def expand(self, state):
        bestAction = 1
        bestValue = -1
        
        for i in range(len(self.actions)):
            x = random.random()
            if (x > bestValue and self.childs[i] == None):
                bestAction = i
                bestValue = x
            

        state.advance(self.actions[bestAction])
        tn = TreeNode(self, bestAction, self.actions, self.time)
        self.childs[bestAction] = tn
        return tn
        
    # Check if current node has been fully expanded
    def notFullyExpanded(self):
        for child in self.childs:
            if (child == None):
                return True
        return False
    
    # Check if tree has reached maximum depth
    def finishRollout(self, state, depth):
        if (depth >= ROLLOUT_DEPTH):
            return True
        if (state.gameover):
            return True
        return False
    
    # Get the value of the current state
    def value(self, state):
        if state.gameover:
            return HUGE_NEGATIVE + state.get_score()
        return state.get_score()
    
    # Normalise the given value
    def normalise(self, score):
        if (self.bounds[1] > self.bounds[0]):
            return (score - self.bounds[0]) / (self.bounds[1] - self.bounds[0])
        else:
            return score
        
        