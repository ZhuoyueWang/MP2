import random

class Status:
    #check the specific information for every action
    def __init__(self, coordinate, direction, turn):
        self.coordinate = coordinate
        self.direction = direction
        self.turn = turn
#the spefic information for the pieces
class State:
    #initialize
    def __init__(self, matrix=None, black=None, white=None, black_num=0,
         white_num=0, turn=1, function=0, width=8, height=8):
        self.width = width
        self.height = height
        if black is None:
            self.black = []
        else:
            self.black = black
        if white is None:
            self.white = []
        else:
            self.white = white
        self.black_num = black_num
        self.white_num = white_num
        self.turn = turn
        self.function = function
        if matrix is not None:
            for i in range(self.height):
                for j in range(self.width):
                    if matrix[i][j] == 1:
                        self.black.append((i, j))
                        self.black_num += 1
                    if matrix[i][j] == 2:
                        self.white.append((i, j))
                        self.white_num += 1

    #simulate the actions
    def transfer(self, action):
        black_pos = list(self.black)
        white_pos = list(self.white)
        # black turn
        if action.turn == 1:
            if action.coordinate in self.black:
                index = black_pos.index(action.coordinate)
                new_pos = self.singleMove(action.coordinate, action.direction, action.turn)
                black_pos[index] = new_pos
                if new_pos in self.white:
                    white_pos.remove(new_pos)
        # white turn
        elif action.turn == 2:
            if action.coordinate in self.white:
                index = white_pos.index(action.coordinate)
                new_pos = self.singleMove(action.coordinate, action.direction, action.turn)
                white_pos[index] = new_pos
                if new_pos in self.black:
                    black_pos.remove(new_pos)

        state = State(black=black_pos, white=white_pos, black_num=self.black_num,
        white_num=self.white_num, turn=self.switchTurn(action.turn), function=self.function,
        height=self.height, width=self.width)
        return state

    #change the turn
    def switchTurn(self,turn):
        if turn == 1:
            return 2
        if turn == 2:
            return 1

            #the component in transfer state, to move one step
    def singleMove(self,initial, direction, turn):
        if turn == 1:
            if direction == 1:
                return initial[0] + 1, initial[1] - 1
            elif direction == 2:
                return initial[0] + 1, initial[1]
            elif direction == 3:
                return initial[0] + 1, initial[1] + 1
        elif turn == 2:
            if direction == 1:
                return initial[0] - 1, initial[1] - 1
            elif direction == 2:
                return initial[0] - 1, initial[1]
            elif direction == 3:
                return initial[0] - 1, initial[1] + 1


    #to check what actions are available right now
    def available_actions(self):
        available_actions = []
        if self.turn == 1:
            for i in sorted(self.black, key=lambda p: (p[0], -p[1]), reverse=True):
                if i[0] != self.height - 1 and i[1] != 0 and (i[0] + 1, i[1] - 1) not in self.black:
                    available_actions.append(Status(i, 1, 1))
                if i[0] != self.height - 1 and (i[0] + 1, i[1]) not in self.black and (i[0] + 1, i[1]) not in self.white:
                    available_actions.append(Status(i, 2, 1))
                if i[0] != self.height - 1 and i[1] != self.width - 1 and (i[0] + 1, i[1] + 1) not in self.black:
                    available_actions.append(Status(i, 3, 1))
        elif self.turn == 2:
            for i in sorted(self.white, key=lambda p: (p[0], p[1])):
                if i[0] != 0 and i[1] != 0 and (i[0] - 1, i[1] - 1) not in self.white:
                    available_actions.append(Status(i, 1, 2))
                if i[0] != 0 and (i[0] - 1, i[1]) not in self.black and (i[0] - 1, i[1]) not in self.white:
                    available_actions.append(Status(i, 2, 2))
                if i[0] != 0 and i[1] != self.width - 1 and (i[0] - 1, i[1] + 1) not in self.white:
                    available_actions.append(Status(i, 3, 2))
        return available_actions

        #get the board
    def getmatrix(self):
        matrix = [[0 for i in range(self.width)] for i in range(self.height)]
        for item in self.black:
            matrix[item[0]][item[1]] = 1
        for item in self.white:
            matrix[item[0]][item[1]] = 2
        return matrix

        #check whether somebody wins
    def done(self):
        if 0 in [item[0] for item in self.white] or len(self.black) == 0:
            return 2
        if self.height - 1 in [item[0] for item in self.black] or len(self.white) == 0:
            return 1
        return 0

        #check the current remaining pieces
    def myscore(self, turn):
        if turn == 1:
            return len(self.black)
        elif turn == 2:
            return len(self.white)

    def enemyscore(self, turn):
        if turn == 1:
            return len(self.white)
        elif turn == 2:
            return len(self.black)

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

        #max component
    def minimax_MAX(self, state, depth):
        if depth == self.maxdepth or state.done() != 0:
            return state.choice(self.turn)
        result= -float("inf")
        for action in state.available_actions():
            result= max(result, self.minimax_MIN(state.transfer(action), depth + 1))
            self.nodes += 1
        return result
        #min component
    def minimax_MIN(self, state, depth):
        if depth == self.maxdepth or state.done() != 0:
            return state.choice(self.turn)
        result= float("inf")
        for action in state.available_actions():
            result= min(result, self.minimax_MAX(state.transfer(action), depth + 1))
            self.nodes += 1
        return result
        #the implementation
    def minimax(self):
        final_action = None
        if self.type == 0:
            initial = State(matrix=self.matrix, turn=self.turn, function=self.function)
        else:
            initial = State(matrix=self.matrix, turn=self.turn, function=self.function, height=5, width=10)
        result= -float("inf")
        for action in initial.available_actions():
            self.nodes += 1
            new_state = initial.transfer(action)
            if new_state.done():
                final_action = action
                break
            minresult = self.minimax_MIN(new_state, 1)
            if minresult > result:
                final_action = action
                result= minresult
        if self.turn == 1:
            temp = initial.transfer(final_action)
            self.piece_num = temp.white_num
        elif self.turn == 2:
            temp = initial.transfer(final_action)
            self.piece_num = temp.black_num
        return initial.transfer(final_action), self.nodes, self.piece_num


    def alphabeta_MAX(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.done() != 0:
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
        if depth == self.maxdepth or state.done() != 0:
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
            initial = State(matrix=self.matrix, turn=self.turn, function=self.function)
        else:
            initial = State(matrix=self.matrix, turn=self.turn, function=self.function, height=5, width=10)
        result = -float("inf")
        for action in initial.available_actions():
            self.nodes += 1
            new_state = initial.transfer(action)
            if new_state.done():
                final_action = action
                break
            minresult = self.alphabeta_MIN(new_state, -float("inf"), float("inf"), 1)
            if minresult > result:
                final_action = action
                result = minresult
        if self.turn == 1:
            temp = initial.transfer(final_action)
            self.piece_num = temp.white_num
        elif self.turn == 2:
            temp = initial.transfer(final_action)
            self.piece_num = temp.black_num
        return initial.transfer(final_action), self.nodes, self.piece_num

    def none(self, action, state):
        return 0
