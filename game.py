from minimax import *
from board import *
from alphabeta import *
import sys, os, math
import time
import random
import pygame

exit = 0

class BreakthroughGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 560, 560
        self.sizeofcell = int(560/8)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill([255, 255, 255])
        # chessboard and workers
        self.board = 0
        self.blackchess = 0
        self.whitechess = 0
        self.outline = 0
        self.reset = 0
        self.winner = 0
        self.computer = None

        # status 0: origin;  1: ready to move; 2: end
        # turn 1: black 2: white
        self.status = 0
        self.turn = 1
        # Variable for moving
        self.ori_x = 0
        self.ori_y = 0
        self.new_x = 0
        self.new_y = 0

        # matrix for position of chess, 0 - empty, 1 - black, 2 - white
        self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]

        self.total_nodes_1 = 0
        self.total_nodes_2 = 0
        self.total_time_1 = 0
        self.total_time_2 = 0
        self.total_step_1 = 0
        self.total_step_2 = 0
        self.eat_piece = 0
        # Caption
        pygame.display.set_caption("Breakthrough CS 440")

        # initialize pygame clock
        self.clock = pygame.time.Clock()
        self.initgraphics()

    def run(self):
        self.clock.tick(60)

        # clear the screen
        self.screen.fill([255, 255, 255])
        self.status = 5


        if self.status == 5:
            # Black
            if self.turn == 1:
                start = time.clock()
                self.ai_move(1, 1)
                self.total_time_1 += (time.clock() - start)
                self.total_step_1 += 1
                print( 'Black: \n'
                    'total steps = ', self.total_step_1, '\n'
                      'total expaned nodes = ', self.total_nodes_1, '\n'
                      'average expaned nodes per move = ', self.total_nodes_1 / self.total_step_1, '\n'
                      'average time per move = ', self.total_time_1 / self.total_step_1, '\n'
                      'number of captured workers = ', self.eat_piece)
            elif self.turn == 2:
                start = time.clock()
                self.ai_move(1, 2)
                self.total_time_2 += (time.clock() - start)
                self.total_step_2 += 1
                print( 'White: \n'
                    'total steps = ', self.total_step_2, '\n'
                      'total expaned nodes = ', self.total_nodes_2, '\n'
                      'average expaned nodes per move = ', self.total_nodes_2 / self.total_step_2, '\n'
                      'average time per move = ', self.total_time_2 / self.total_step_2, '\n'
                      'number of captured workers = ', self.eat_piece)

        # Events accepting
        for event in pygame.event.get():
            # Quit if close the windows
            if event.type == pygame.QUIT:
                exit()
            # reset button pressed


            # ====================================================================================
            # select chess
            elif self.status == 0:
                x, y = event.pos
                coor_y = math.floor(x / self.sizeofcell)
                coor_x = math.floor(y / self.sizeofcell)
                if self.boardmatrix[coor_x][coor_y] == self.turn:
                    self.status = 1
                    self.ori_y = math.floor(x / self.sizeofcell)
                    self.ori_x = math.floor(y / self.sizeofcell)
            # check whether the selected chess can move, otherwise select other chess
            elif self.status == 1:
                x, y = event.pos
                self.new_y = math.floor(x / self.sizeofcell)
                self.new_x = math.floor(y / self.sizeofcell)
                if self.isabletomove():
                    self.movechess()
                    if (self.new_x == 7 and self.boardmatrix[self.new_x][self.new_y] == 1) \
                        or (self.new_x == 0 and self.boardmatrix[self.new_x][self.new_y] == 2):
                        self.status = 3
                elif self.boardmatrix[self.new_x][self.new_y] == self.boardmatrix[self.ori_x][self.ori_y]:
                    self.ori_x = self.new_x
                    self.ori_y = self.new_y
                    # display the board and chess
        self.display()
        # update the screen
        pygame.display.flip()

    # load the graphics and rescale them
    def initgraphics(self):
        self.board = pygame.image.load_extended('board.png')
        self.board = pygame.transform.scale(self.board, (560, 560))
        self.blackchess = pygame.image.load_extended('black.png')
        self.blackchess = pygame.transform.scale(self.blackchess, (self.sizeofcell- 20, self.sizeofcell - 20))
        self.whitechess = pygame.image.load_extended('white.png')
        self.whitechess = pygame.transform.scale(self.whitechess, (self.sizeofcell - 20, self.sizeofcell - 20))

    # display the graphics in the window
    def display(self):
        self.screen.blit(self.board, (0, 0))
        for i in range(8):
            for j in range(8):
                if self.boardmatrix[i][j] == 1:
                    self.screen.blit(self.blackchess, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
                elif self.boardmatrix[i][j] == 2:
                    self.screen.blit(self.whitechess, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
        if self.status == 1:
            # only downward is acceptable
            if self.boardmatrix[self.ori_x][self.ori_y] == 1:
                x1 = self.ori_x + 1
                y1 = self.ori_y - 1
                x2 = self.ori_x + 1
                y2 = self.ori_y + 1
                x3 = self.ori_x + 1
                y3 = self.ori_y
                # left down
                if y1 >= 0 and self.boardmatrix[x1][y1] != 1:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                # right down
                if y2 <= 7 and self.boardmatrix[x2][y2] != 1:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                # down
                if x3 <= 7 and self.boardmatrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y3, self.sizeofcell * x3))

            if self.boardmatrix[self.ori_x][self.ori_y] == 2:
                x1 = self.ori_x - 1
                y1 = self.ori_y - 1
                x2 = self.ori_x - 1
                y2 = self.ori_y + 1
                x3 = self.ori_x - 1
                y3 = self.ori_y
                # left up
                if y1 >= 0 and self.boardmatrix[x1][y1] != 2:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                # right up
                if y2 <= 7 and self.boardmatrix[x2][y2] != 2:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                # up
                if x3 >= 0 and self.boardmatrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y3, self.sizeofcell * x3))
        if self.status == 3:
            if self.turn == 1:
                print("Black Win!")
                print( 'Black: \n'
                    'total steps = ', self.total_step_1, '\n'
                      'total expaned nodes = ', self.total_nodes_1, '\n'
                      'average expaned nodes per move = ', self.total_nodes_1 / self.total_step_1, '\n'
                      'average time per move = ', self.total_time_1 / self.total_step_1, '\n'
                      'number of captured workers = ', self.eat_piece)
            else:
                print("White Win!")
                print( 'White: \n'
                    'total steps = ', self.total_step_2, '\n'
                      'total expaned nodes = ', self.total_nodes_2, '\n'
                      'average expaned nodes per move = ', self.total_nodes_2 / self.total_step_2, '\n'
                      'average time per move = ', self.total_time_2 / self.total_step_2, '\n'
                      'number of captured workers = ', self.eat_piece)

    def movechess(self):
        self.boardmatrix[self.new_x][self.new_y] = self.boardmatrix[self.ori_x][self.ori_y]
        self.boardmatrix[self.ori_x][self.ori_y] = 0
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.status = 0


#    def isauto(self, pos):
    #    x, y = pos
#        if 590 <= x <= 670 and 340 <= y <= 420:
    #        return True
#        return False

    def isabletomove(self):
        if (self.boardmatrix[self.ori_x][self.ori_y] == 1
            and self.boardmatrix[self.new_x][self.new_y] != 1
            and self.new_x - self.ori_x == 1
            and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
            and not (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 2)) \
            or (self.boardmatrix[self.ori_x][self.ori_y] == 2
                and self.boardmatrix[self.new_x][self.new_y] != 2
                and self.ori_x - self.new_x == 1
                and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
                and not (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 1)):
            return 1
        return 0

    def ai_move(self, searchtype, evaluation):
        if searchtype == 1:
            return self.ai_move_minimax(evaluation)
        elif searchtype == 2:
            return self.ai_move_alphabeta(evaluation)

    def ai_move_minimax(self, function_type):
        board, nodes, piece = MinimaxAgent(self.boardmatrix, self.turn, 3, function_type).minimax_decision()
        self.boardmatrix = board.getMatrix()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.isgoalstate():
            self.status = 3
            #print(self.boardmatrix)

    def ai_move_alphabeta(self, function_type):
        board, nodes, piece = AlphaBetaAgent(self.boardmatrix, self.turn, 5, function_type).alpha_beta_decision()
        self.boardmatrix = board.getMatrix()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.isgoalstate():
            self.status = 3

    def isgoalstate(self, base=0):
        if base == 0:
            if 2 in self.boardmatrix[0] or 1 in self.boardmatrix[7]:
                return True
            else:
                for line in self.boardmatrix:
                    if 1 in line or 2 in line:
                        return False
            return True
        else:
            count = 0
            for i in self.boardmatrix[0]:
                if i == 2:
                    count += 1
            if count == 3:
                return True
            count = 0
            for i in self.boardmatrix[7]:
                if i == 1:
                    count += 1
            if count == 3:
                return True
            count1 = 0
            count2 = 0
            for line in self.boardmatrix:
                for i in line:
                    if i == 1:
                        count1 += 1
                    elif i == 2:
                        count2 += 1
            if count1 <= 2 or count2 <= 2:
                return True
        return False

def main():
    game = BreakthroughGame()
    while 1:
        game.run()


if __name__ == '__main__':
    main()
