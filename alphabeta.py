from board import *



class alphabeta:
    def __init__(self, boardmatrix, turn, depth, function, type=0):
        self.boardmatrix = boardmatrix
        self.turn = turn
        self.maxdepth = depth
        self.function = function
        self.type = type
        self.nodes = 0
        self.piece_num = 0

    def MAX(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.choice(self.turn)
        result = -float("inf")
        actions = state.available_actions()
        actions = sorted(state.available_actions(), key=lambda action: self.orderaction(action, state), reverse=True)
        for action in actions:
            self.nodes += 1
            result = max(result, self.MIN(state.transfer(action), alpha, beta, depth + 1))
            if result >= beta:
                return result
            alpha = max(alpha, result)
        return result

    def MIN(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.choice(self.turn)
        result = float("inf")
        actions = state.available_actions()
        actions = sorted(state.available_actions(), key=lambda action: self.orderaction(action, state))
        for action in actions:
            self.nodes += 1

            result = min(result, self.MAX(state.transfer(action), alpha, beta, depth + 1))
            if result <= alpha:
                return result
            beta = min(beta, result)
        return result

    def alpha_beta_decision(self):
        final_action = None
        if self.type == 0:
            initialstate = State(boardmatrix=self.boardmatrix, turn=self.turn, function=self.function)
        else:
            initialstate = State(boardmatrix=self.boardmatrix, turn=self.turn, function=self.function, height=5, width=10)
        result = -float("inf")
        for action in initialstate.available_actions():
            self.nodes += 1
            new_state = initialstate.transfer(action)
            if new_state.isgoalstate():
                final_action = action
                break
            minresult = self.MIN(new_state, -float("inf"), float("inf"), 1)
            if minresult > result:
                final_action = action
                result = minresult
        print(result)
        if self.turn == 1:
            temp = initialstate.transfer(final_action)
            self.piece_num = temp.white_num
        elif self.turn == 2:
            temp = initialstate.transfer(final_action)
            self.piece_num = temp.black_num
        print(final_action.getString())
        return initialstate.transfer(final_action), self.nodes, self.piece_num

    def orderaction(self, action, state):
        return 0
