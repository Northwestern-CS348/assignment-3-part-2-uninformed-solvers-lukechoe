
from solver import *
import copy

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here

        
        if self.currentState.state == self.victoryCondition:
            return True

        movables = self.gm.getMovables()
    

        if movables:
            for movable in movables:
                self.gm.makeMove(movable)
                self.child_state = GameState(self.gm.getGameState(), self.currentState.depth + 1, movable)
                self.child_state.parent = self.currentState
                self.currentState = self.child_state
                
                if self.currentState in self.visited: 
                    self.gm.reverseMove(movable)
                    self.currentState = self.currentState.parent  
                else:
                    self.visited[self.currentState] = True
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)

        return False

class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

        self.queue = []
        self.steps = dict()
    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        

        if self.currentState.depth == 0:
            self.steps[self.currentState] = []

        if self.currentState.state == self.victoryCondition:
            return True
        
        movables = self.gm.getMovables()
        
        if movables:
            for move in movables:
                self.gm.makeMove(move)
                child = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
                if child in self.visited:
                    self.gm.reverseMove(move)
                else:
                    self.queue.append(child)
                    self.visited[child] = True
                    self.steps[child] = self.steps[self.currentState].copy()
                    self.steps[child].append(child)
                    self.gm.reverseMove(move)
        prev_moves = self.steps[self.currentState]
        prev_moves.reverse()
        self.currentState = self.queue.pop(0) # pop from queue
        self.visited[self.currentState] = True    
        for move in prev_moves:
            self.gm.reverseMove(move.requiredMovable)
        next_moves = self.steps[self.currentState] 
        for move in next_moves:
            self.gm.makeMove(move.requiredMovable)



        return False