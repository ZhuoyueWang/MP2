import random

class Action:
    def __init__(self, coordinate, direction, turn):
        self.coordinate = coordinate
        self.direction = direction
        self.turn = turn

class State:
    def __init__(self, matrix=None, black_position=None, white_position=None, black_num=0,
         white_num=0, turn=1, function=0, width=8, height=8):
        self.width = width
        self.height = height
        if black_position is None:
            self.black_positions = []
        else:
            self.black_positions = black_position
        if white_position is None:
            self.white_positions = []
        else:
            self.white_positions = white_position
        self.black_num = black_num
        self.white_num = white_num
        self.turn = turn
        self.function = function
        if matrix is not None:
            for i in range(self.height):
                for j in range(self.width):
                    if matrix[i][j] == 1:
                        self.black_positions.append((i, j))
                        self.black_num += 1
                    if matrix[i][j] == 2:
                        self.white_positions.append((i, j))
                        self.white_num += 1

    def transfer(self, action):
        black_pos = list(self.black_positions)
        white_pos = list(self.white_positions)
        # black turn
        if action.turn == 1:
            if action.coordinate in self.black_positions:
                index = black_pos.index(action.coordinate)
                new_pos = self.singleMove(action.coordinate, action.direction, action.turn)
                black_pos[index] = new_pos
                if new_pos in self.white_positions:
                    white_pos.remove(new_pos)
        # white turn
        elif action.turn == 2:
            if action.coordinate in self.white_positions:
                index = white_pos.index(action.coordinate)
                new_pos = self.singleMove(action.coordinate, action.direction, action.turn)
                white_pos[index] = new_pos
                if new_pos in self.black_positions:
                    black_pos.remove(new_pos)

        state = State(black_position=black_pos, white_position=white_pos, black_num=self.black_num,
        white_num=self.white_num, turn=self.switchTurn(action.turn), function=self.function,
        height=self.height, width=self.width)
        return state

    def switchTurn(self,turn):
        if turn == 1:
            return 2
        if turn == 2:
            return 1

    def singleMove(self,initial_pos, direction, turn):
        if turn == 1:
            if direction == 1:
                return initial_pos[0] + 1, initial_pos[1] - 1
            elif direction == 2:
                return initial_pos[0] + 1, initial_pos[1]
            elif direction == 3:
                return initial_pos[0] + 1, initial_pos[1] + 1
        elif turn == 2:
            if direction == 1:
                return initial_pos[0] - 1, initial_pos[1] - 1
            elif direction == 2:
                return initial_pos[0] - 1, initial_pos[1]
            elif direction == 3:
                return initial_pos[0] - 1, initial_pos[1] + 1

    def available_actions(self):
        available_actions = []
        if self.turn == 1:
            for i in sorted(self.black_positions, key=lambda p: (p[0], -p[1]), reverse=True):
                if i[0] != self.height - 1 and i[1] != 0 and (i[0] + 1, i[1] - 1) not in self.black_positions:
                    available_actions.append(Action(i, 1, 1))
                if i[0] != self.height - 1 and (i[0] + 1, i[1]) not in self.black_positions and (i[0] + 1, i[1]) not in self.white_positions:
                    available_actions.append(Action(i, 2, 1))
                if i[0] != self.height - 1 and i[1] != self.width - 1 and (i[0] + 1, i[1] + 1) not in self.black_positions:
                    available_actions.append(Action(i, 3, 1))
        elif self.turn == 2:
            for i in sorted(self.white_positions, key=lambda p: (p[0], p[1])):
                if i[0] != 0 and i[1] != 0 and (i[0] - 1, i[1] - 1) not in self.white_positions:
                    available_actions.append(Action(i, 1, 2))
                if i[0] != 0 and (i[0] - 1, i[1]) not in self.black_positions and (i[0] - 1, i[1]) not in self.white_positions:
                    available_actions.append(Action(i, 2, 2))
                if i[0] != 0 and i[1] != self.width - 1 and (i[0] - 1, i[1] + 1) not in self.white_positions:
                    available_actions.append(Action(i, 3, 2))
        return available_actions

    def getmatrix(self):
        matrix = [[0 for i in range(self.width)] for i in range(self.height)]
        for item in self.black_positions:
            matrix[item[0]][item[1]] = 1
        for item in self.white_positions:
            matrix[item[0]][item[1]] = 2
        return matrix

    def isgoalstate(self):
        if 0 in [item[0] for item in self.white_positions] or len(self.black_positions) == 0:
            return 2
        if self.height - 1 in [item[0] for item in self.black_positions] or len(self.white_positions) == 0:
            return 1
        return 0

    def myscore(self, turn):
        if turn == 1:
            return len(self.black_positions)
        elif turn == 2:
            return len(self.white_positions)

    def enemyscore(self, turn):
        if turn == 1:
            return len(self.white_positions)
        elif turn == 2:
            return len(self.black_positions)

    def offensive(self, turn):
        return 6*(30-self.enemyscore(turn)) +random.random()

    def defensive(self, turn):
        return 6*self.myscore(turn) + random.random()

    def offensive2(self, turn):
        return 2*self.myscore(turn) - 6*self.enemyscore(turn)+ random.random()

    def defensive2(self, turn):
        return 6*self.myscore(turn) - 2*self.enemyscore(turn)+ random.random()

    def choice(self, turn):
        if self.function == 0:
            return 0
        elif self.function == 1:
            return self.offensive(turn)
        elif self.function == 2:
            return self.defensive(turn)
        elif self.function == 3:
            return self.offensive2(turn)
        elif self.function == 4:
            return self.defensive2(turn)



class search:
    def __init__(self, matrix, turn, depth, function, type=0):
        self.matrix = matrix
        self.turn = turn
        self.maxdepth = depth
        self.function = function
        self.type = type
        self.nodes = 0
        self.piece_num = 0

    def minimax_MAX(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            #print("choice", state.choice(self.turn))
            return state.choice(self.turn)
        result= -float("inf")
        for action in state.available_actions():
            # print(state.transfer(action).getmatrix())
            result= max(result, self.minimax_MIN(state.transfer(action), depth + 1))
            self.nodes += 1
        return result

    def minimax_MIN(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            #print("choice", state.choice(self.turn))
            return state.choice(self.turn)
        result= float("inf")
        for action in state.available_actions():
            result= min(result, self.minimax_MAX(state.transfer(action), depth + 1))
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
            minresult = self.minimax_MIN(new_state, 1)
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


    def alphabeta_MAX(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.choice(self.turn)
        result = -float("inf")
        actions = state.available_actions()
        actions = sorted(state.available_actions(), key=lambda action: self.none(action, state), reverse=True)
        for action in actions:
            self.nodes += 1
            result = max(result, self.alphabeta_MIN(state.transfer(action), alpha, beta, depth + 1))
            if result >= beta:
                return result
            alpha = max(alpha, result)
        return result

    def alphabeta_MIN(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.choice(self.turn)
        result = float("inf")
        actions = state.available_actions()
        actions = sorted(state.available_actions(), key=lambda action: self.none(action, state))
        for action in actions:
            self.nodes += 1

            result = min(result, self.alphabeta_MAX(state.transfer(action), alpha, beta, depth + 1))
            if result <= alpha:
                return result
            beta = min(beta, result)
        return result

    def alphabet(self):
        final_action = None
        if self.type == 0:
            initialstate = State(matrix=self.matrix, turn=self.turn, function=self.function)
        else:
            initialstate = State(matrix=self.matrix, turn=self.turn, function=self.function, height=5, width=10)
        result = -float("inf")
        for action in initialstate.available_actions():
            self.nodes += 1
            new_state = initialstate.transfer(action)
            if new_state.isgoalstate():
                final_action = action
                break
            minresult = self.alphabeta_MIN(new_state, -float("inf"), float("inf"), 1)
            if minresult > result:
                final_action = action
                result = minresult
        if self.turn == 1:
            temp = initialstate.transfer(final_action)
            self.piece_num = temp.white_num
        elif self.turn == 2:
            temp = initialstate.transfer(final_action)
            self.piece_num = temp.black_num
        return initialstate.transfer(final_action), self.nodes, self.piece_num

    def none(self, action, state):
        return 0
