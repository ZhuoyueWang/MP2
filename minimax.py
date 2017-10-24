from board import *

class minimax:
    def __init__(self, matrix, turn, depth, function, type=0):
        self.matrix = matrix
        self.turn = turn
        self.maxdepth = depth
        self.function = function
        self.type = type
        self.nodes = 0
        self.piece_num = 0

    def MAX(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            #print("choice", state.choice(self.turn))
            return state.choice(self.turn)
        result= -float("inf")
        for action in state.available_actions():
            # print(state.transfer(action).getmatrix())
            result= max(result, self.MIN(state.transfer(action), depth + 1))
            self.nodes += 1
        return result

    def MIN(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            #print("choice", state.choice(self.turn))
            return state.choice(self.turn)
        result= float("inf")
        for action in state.available_actions():
            result= min(result, self.MAX(state.transfer(action), depth + 1))
            self.nodes += 1
        return result

    def minimax(self):
        final_action = None
        if self.type == 0:
            initialstate = State(matrix=self.matrix, turn=self.turn, function=self.function)
        else:
            initialstate = State(matrix=self.matrix, turn=self.turn, function=self.function, height=5, width=10)
        result= -float("inf")
        for action in initialstate.available_actions():
            self.nodes += 1
            new_state = initialstate.transfer(action)
            if new_state.isgoalstate():
                final_action = action
                break
            minresult = self.MIN(new_state, 1)
            if minresult > result:
                final_action = action
                result= minresult
        if self.turn == 1:
            temp = initialstate.transfer(final_action)
            self.piece_num = temp.white_num
        elif self.turn == 2:
            temp = initialstate.transfer(final_action)
            self.piece_num = temp.black_num
        return initialstate.transfer(final_action), self.nodes, self.piece_num
