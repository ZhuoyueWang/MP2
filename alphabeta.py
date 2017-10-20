from board import *



class AlphaBetaAgent:
    def __init__(self, boardmatrix, turn, depth, function, type=0):
        self.boardmatrix = boardmatrix
        self.turn = turn
        self.maxdepth = depth
        self.function = function
        self.type = type

        self.nodes = 0
        self.piece_num = 0

    def max_value(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.utility(self.turn)
        v = MINNUM
        actions = state.available_actions()

        #if self.turn == 1:
        actions = sorted(state.available_actions(), key=lambda action: self.orderaction(action, state), reverse=True)
        #else:
        #    actions = sorted(state.available_actions(), key=lambda action: self.orderaction(action, state))

        for action in actions:
            self.nodes += 1

            v = max(v, self.min_value(state.transfer(action), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

   def min_value(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.utility(self.turn)
        v = MAXNUM
        actions = state.available_actions()

        #if self.turn == 1:
        actions = sorted(state.available_actions(), key=lambda action: self.orderaction(action, state))
        #else:
        #    actions = sorted(state.available_actions(), key=lambda action: self.orderaction(action, state), reverse=True)

        for action in actions:
            self.nodes += 1

            v = min(v, self.max_value(state.transfer(action), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v    
