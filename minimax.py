import numpy as np
from model import *


class MinimaxAgent:
    def __init__(self, boardmatrix, turn, depth, function, type=0):
        self.boardmatrix = boardmatrix
        self.turn = turn
        self.maxdepth = depth
        self.function = function
        self.type = type
        self.nodes = 0
        self.piece_num = 0

    def max_value(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            #print("utility", state.utility(self.turn))
            return state.utility(self.turn)
        v = MINNUM
        for action in state.available_actions():
            # print(state.transfer(action).getMatrix())
            v = max(v, self.min_value(state.transfer(action), depth + 1))
            self.nodes += 1
        return v

    def min_value(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            #print("utility", state.utility(self.turn))
            return state.utility(self.turn)
        v = MAXNUM
        for action in state.available_actions():
            v = min(v, self.max_value(state.transfer(action), depth + 1))
            self.nodes += 1

        return v
