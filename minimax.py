import numpy as np
from board import *


class minimax:
    def __init__(self, boardmatrix, turn, depth, function, type=0):
        self.boardmatrix = boardmatrix
        self.turn = turn
        self.maxdepth = depth
        self.function = function
        self.type = type
        self.nodes = 0
        self.piece_num = 0

    def MAX(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            #print("utility", state.utility(self.turn))
            return state.utility(self.turn)
        v = MINNUM
        for action in state.available_actions():
            # print(state.transfer(action).getMatrix())
            v = max(v, self.MIN(state.transfer(action), depth + 1))
            self.nodes += 1
        return v

    def MIN(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            #print("utility", state.utility(self.turn))
            return state.utility(self.turn)
        v = MAXNUM
        for action in state.available_actions():
            v = min(v, self.MAX(state.transfer(action), depth + 1))
            self.nodes += 1

        return v

    def minimax_decision(self):
        final_action = None
        if self.type == 0:
            initialstate = State(boardmatrix=self.boardmatrix, turn=self.turn, function=self.function)
        else:
            initialstate = State(boardmatrix=self.boardmatrix, turn=self.turn, function=self.function, height=5, width=10)
        v = MINNUM
        for action in initialstate.available_actions():
            self.nodes += 1
            new_state = initialstate.transfer(action)
            if new_state.isgoalstate():
                final_action = action
                break
            minresult = self.MIN(new_state, 1)
            if minresult > v:
                final_action = action
                v = minresult
        if self.turn == 1:
            temp = initialstate.transfer(final_action)
            self.piece_num = temp.white_num
        elif self.turn == 2:
            temp = initialstate.transfer(final_action)
            self.piece_num = temp.black_num
        print(final_action.getString())
        return initialstate.transfer(final_action), self.nodes, self.piece_num
