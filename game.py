from minimax import *
from board import *
from alphabeta import *
import sys
import math
import time
import random
import pygame

class game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 560, 560
        self.sizeofcell = int(560/8)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill([255, 255, 255])
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
        self.matrix = [[1, 1, 1, 1, 1, 1, 1, 1],
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
        self.clock = pygame.time.Clock()
        self.initgraphics()

    def initgraphics(self):
        self.board = pygame.image.load_extended('board.png')
        self.board = pygame.transform.scale(self.board, (560, 560))
        self.blackchess = pygame.image.load_extended('black.png')
        self.blackchess = pygame.transform.scale(self.blackchess, (self.sizeofcell- 20, self.sizeofcell - 20))
        self.whitechess = pygame.image.load_extended('white.png')
        self.whitechess = pygame.transform.scale(self.whitechess, (self.sizeofcell - 20, self.sizeofcell - 20))

    def run(self):
        self.clock.tick(60)

        # clear the screen
        self.screen.fill([255, 255, 255])
        self.status = 5


        if self.status == 5:
            # Black
            if self.turn == 1:
                start = time.clock()
                self.move(1, 1)
                self.total_time_1 += (time.clock() - start)
                self.total_step_1 += 1
                print( 'Black: \n'
                    'total steps =', self.total_step_1, '\n'
                      'total expaned nodes =', self.total_nodes_1, '\n'
                      'average expaned nodes per move =', self.total_nodes_1 / self.total_step_1, '\n'
                      'average time per move =', self.total_time_1 / self.total_step_1, '\n'
                      'number of captured workers =', self.eat_piece)
            elif self.turn == 2:
                start = time.clock()
                self.move(1, 2)
                self.total_time_2 += (time.clock() - start)
                self.total_step_2 += 1
                print( 'White: \n'
                    'total steps =', self.total_step_2, '\n'
                      'total expaned nodes =', self.total_nodes_2, '\n'
                      'average expaned nodes per move =', self.total_nodes_2 / self.total_step_2, '\n'
                      'average time per move =', self.total_time_2 / self.total_step_2, '\n'
                      'number of captured workers =', self.eat_piece)

        for event in pygame.event.get():
            # Quit if close the windows
            if event.type == pygame.QUIT:
                exit()

            elif self.status == 0:
                x, y = event.pos
                coor_y = math.floor(x / self.sizeofcell)
                coor_x = math.floor(y / self.sizeofcell)
                if self.matrix[coor_x][coor_y] == self.turn:
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
                    if (self.new_x == 7 and self.matrix[self.new_x][self.new_y] == 1) \
                        or (self.new_x == 0 and self.matrix[self.new_x][self.new_y] == 2):
                        self.status = 3
                elif self.matrix[self.new_x][self.new_y] == self.matrix[self.ori_x][self.ori_y]:
                    self.ori_x = self.new_x
                    self.ori_y = self.new_y
        self.display()
        pygame.display.flip()


    # display the graphics in the window
    def display(self):
        self.screen.blit(self.board, (0, 0))
        for i in range(8):
            for j in range(8):
                if self.matrix[i][j] == 1:
                    self.screen.blit(self.blackchess, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
                elif self.matrix[i][j] == 2:
                    self.screen.blit(self.whitechess, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
        if self.status == 1:
            # only downward is acceptable
            if self.matrix[self.ori_x][self.ori_y] == 1:
                x1 = self.ori_x + 1
                y1 = self.ori_y - 1
                x2 = self.ori_x + 1
                y2 = self.ori_y + 1
                x3 = self.ori_x + 1
                y3 = self.ori_y
                # left down
                if y1 >= 0 and self.matrix[x1][y1] != 1:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                # right down
                if y2 <= 7 and self.matrix[x2][y2] != 1:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                # down
                if x3 <= 7 and self.matrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y3, self.sizeofcell * x3))

            if self.matrix[self.ori_x][self.ori_y] == 2:
                x1 = self.ori_x - 1
                y1 = self.ori_y - 1
                x2 = self.ori_x - 1
                y2 = self.ori_y + 1
                x3 = self.ori_x - 1
                y3 = self.ori_y
                if y1 >= 0 and self.matrix[x1][y1] != 2:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                if y2 <= 7 and self.matrix[x2][y2] != 2:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                if x3 >= 0 and self.matrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y3, self.sizeofcell * x3))
        if self.status == 3:
            if self.turn == 1:
                print("Black Win!")
                print( 'Black: \n'
                    'total steps =', self.total_step_1, '\n'
                      'total expaned nodes =', self.total_nodes_1, '\n'
                      'average expaned nodes per move =', self.total_nodes_1 / self.total_step_1, '\n'
                      'average time per move =', self.total_time_1 / self.total_step_1, '\n'
                      'number of captured workers =', self.eat_piece)
            else:
                print("White Win!")
                print( 'White: \n'
                    'total steps =', self.total_step_2, '\n'
                      'total expaned nodes =', self.total_nodes_2, '\n'
                      'average expaned nodes per move =', self.total_nodes_2 / self.total_step_2, '\n'
                      'average time per move =', self.total_time_2 / self.total_step_2, '\n'
                      'number of captured workers =', self.eat_piece)
            rect = pygame.Rect(0, 0, 560, 560)
            sub = self.screen.subsurface(rect)
            pygame.image.save(sub, "screenshot.jpg")
            sys.exit()


    def movechess(self):
        self.matrix[self.new_x][self.new_y] = self.matrix[self.ori_x][self.ori_y]
        self.matrix[self.ori_x][self.ori_y] = 0
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.status = 0


    def isabletomove(self):
        if (self.matrix[self.ori_x][self.ori_y] == 1
            and self.matrix[self.new_x][self.new_y] != 1
            and self.new_x - self.ori_x == 1
            and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
            and not (self.ori_y == self.new_y and self.matrix[self.new_x][self.new_y] == 2)) \
            or (self.matrix[self.ori_x][self.ori_y] == 2
                and self.matrix[self.new_x][self.new_y] != 2
                and self.ori_x - self.new_x == 1
                and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
                and not (self.ori_y == self.new_y and self.matrix[self.new_x][self.new_y] == 1)):
            return 1
        return 0

    def move(self, searchtype, evaluation):
        if searchtype == 1:
            return self.move_minimax(evaluation)
        elif searchtype == 2:
            return self.move_alphabeta(evaluation)

    def move_minimax(self, function_type):
        board, nodes, piece = minimax(self.matrix, self.turn, 3, function_type).minimax()
        self.moveNode(board,nodes,piece)
    def move_alphabeta(self, function_type):
        board, nodes, piece = alphabeta(self.matrix, self.turn, 5, function_type).alphabet()
        self.moveNode(board,nodes,piece)

    def moveNode(self,board,nodes,piece):
        self.matrix = board.getmatrix()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.isgoalstate():
            self.status = 3

    def isgoalstate(self):
        if 2 in self.matrix[0] or 1 in self.matrix[7]:
            return True
        else:
            for line in self.matrix:
                if 1 in line or 2 in line:
                    return False
        return True

def main():
    Game = game()
    while True:
        Game.run()


if __name__ == '__main__':
    main()
