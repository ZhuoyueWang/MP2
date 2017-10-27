from search import *
import sys
import math
import time
import random
import pygame

class game:
    def __init__(self):
        pygame.init()
        self.sizeofcell = int(560/8)
        self.screen = pygame.display.set_mode((560, 560))
        self.screen.fill([255, 255, 255])
        self.board = 0
        self.blackchess = 0
        self.whitechess = 0
        self.clock = pygame.time.Clock()
        self.board = pygame.image.load_extended('board.png')
        self.board = pygame.transform.scale(self.board, (560, 560))
        self.blackchess = pygame.image.load_extended('black.png')
        self.blackchess = pygame.transform.scale(self.blackchess, (self.sizeofcell- 20, self.sizeofcell - 20))
        self.whitechess = pygame.image.load_extended('white.png')
        self.whitechess = pygame.transform.scale(self.whitechess, (self.sizeofcell - 20, self.sizeofcell - 20))
        self.outline = 0
        self.winner = 0
        self.status = 0
        self.turn = 1
        self.x = 0
        self.y = 0
        self.newX = 0
        self.newY = 0
        self.totalNode1 = 0
        self.totalNode2 = 0
        self.totalTime1 = 0
        self.totalTime2 = 0
        self.totalStep1 = 0
        self.totalStep2 = 0
        self.eaten = 0
        # matrix for position of chess, 0 - empty, 1 - black, 2 - white
        self.matrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]

    def run(self):
        self.clock.tick(60)
        # clear the screen
        self.screen.fill([255, 255, 255])
        self.status = 5
        if self.status == 5:
            # Black
            if self.turn == 1:
                start = time.clock()
                self.move(1, 3)
                self.totalTime1 += (time.clock() - start)
                self.totalStep1 += 1
            elif self.turn == 2:
                start = time.clock()
                self.move(1, 4)
                self.totalTime2 += (time.clock() - start)
                self.totalStep2 += 1
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
                    self.y = math.floor(x / self.sizeofcell)
                    self.x = math.floor(y / self.sizeofcell)
            # check whether the selected chess can move, otherwise select other chess
            elif self.status == 1:
                x, y = event.pos
                self.newY = math.floor(x / self.sizeofcell)
                self.newX = math.floor(y / self.sizeofcell)
                if self.isabletomove():
                    self.movechess()
                    if (self.newX == 7 and self.matrix[self.newX][self.newY] == 1) or (self.newX == 0 and self.matrix[self.newX][self.newY] == 2):
                        self.status = 3
                elif self.matrix[self.newX][self.newY] == self.matrix[self.x][self.y]:
                    self.x = self.newX
                    self.y = self.newY
        self.display()
        pygame.display.flip()

    def display(self):
        self.screen.blit(self.board, (0, 0))
        for i in range(8):
            for j in range(8):
                if self.matrix[i][j] == 1:
                    self.screen.blit(self.blackchess, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
                elif self.matrix[i][j] == 2:
                    self.screen.blit(self.whitechess, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
        if self.status == 3:
            if self.turn == 1:
                print("White Win!")
                print( 'Black: \n'
                    'total steps =', self.totalStep1, '\n'
                      'total expaned nodes =', self.totalNode1, '\n'
                      'average expaned nodes per move =', self.totalNode1 / self.totalStep1, '\n'
                      'average time per move =', self.totalTime1 / self.totalStep1, '\n'
                      'number of captured workers =', self.eaten)
                print( 'White: \n'
                    'total steps =', self.totalStep2, '\n'
                      'total expaned nodes =', self.totalNode2, '\n'
                      'average expaned nodes per move =', self.totalNode2 / self.totalStep2, '\n'
                      'average time per move =', self.totalTime2 / self.totalStep2, '\n'
                      'number of captured workers =', self.eaten)
            else:
                print("Black Win!")
                print( 'White: \n'
                    'total steps =', self.totalStep2, '\n'
                      'total expaned nodes =', self.totalNode2, '\n'
                      'average expaned nodes per move =', self.totalNode2 / self.totalStep2, '\n'
                      'average time per move =', self.totalTime2 / self.totalStep2, '\n'
                      'number of captured workers =', self.eaten)
                print( 'Black: \n'
                    'total steps =', self.totalStep1, '\n'
                      'total expaned nodes =', self.totalNode1, '\n'
                      'average expaned nodes per move =', self.totalNode1 / self.totalStep1, '\n'
                      'average time per move =', self.totalTime1 / self.totalStep1, '\n'
                      'number of captured workers =', self.eaten)
            rect = pygame.Rect(0, 0, 560, 560)
            sub = self.screen.subsurface(rect)
            pygame.image.save(sub, "screenshot.jpg")
            sys.exit()

        if self.status == 1:
            # only downward is acceptable
            if self.matrix[self.x][self.y] == 1:
                x1 = self.x + 1
                y1 = self.y - 1
                x2 = self.x + 1
                y2 = self.y + 1
                x3 = self.x + 1
                y3 = self.y
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

            if self.matrix[self.x][self.y] == 2:
                x1 = self.x - 1
                y1 = self.y - 1
                x2 = self.x - 1
                y2 = self.y + 1
                x3 = self.x - 1
                y3 = self.y
                if y1 >= 0 and self.matrix[x1][y1] != 2:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y1, self.sizeofcell * x1))
                if y2 <= 7 and self.matrix[x2][y2] != 2:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y2, self.sizeofcell * x2))
                if x3 >= 0 and self.matrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (self.sizeofcell * y3, self.sizeofcell * x3))


    def isgoalstate(self):
        if 2 in self.matrix[0] or 1 in self.matrix[7]:
            return True
        else:
            for line in self.matrix:
                if 1 in line or 2 in line:
                    return False
        return True

    def movechess(self):
        self.matrix[self.newX][self.newY] = self.matrix[self.x][self.y]
        self.matrix[self.x][self.y] = 0
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.status = 0

    def isabletomove(self):
        if checkMove == True:
            return 1
        return 0

    def checkMove(self):
        if (self.matrix[self.x][self.y] == 1
            and self.matrix[self.newX][self.newY] != 1
            and self.newX - self.x == 1
            and self.y - 1 <= self.newY <= self.y + 1
            and not (self.y == self.newY and self.matrix[self.newX][self.newY] == 2)) \
            or (self.matrix[self.x][self.y] == 2
                and self.matrix[self.newX][self.newY] != 2
                and self.x - self.newX == 1
                and self.y - 1 <= self.newY <= self.y + 1
                and not (self.y == self.newY and self.matrix[self.newX][self.newY] == 1)):
            return True
        return False


    def move(self, searchtype, evaluation):
        if searchtype == 1:
            return self.move_minimax(evaluation)
        elif searchtype == 2:
            return self.move_alphabeta(evaluation)

    def move_minimax(self, function_type):
        board, nodes, piece = search(self.matrix, self.turn, 3, function_type).minimax()
        self.moveNode(board,nodes,piece)
    def move_alphabeta(self, function_type):
        board, nodes, piece = searchState(self.matrix, self.turn, 5, function_type).alphabet()
        self.moveNode(board,nodes,piece)

    def moveNode(self,board,nodes,piece):
        self.matrix = board.getmatrix()
        if self.turn == 1:
            self.totalNode1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.totalNode2 += nodes
            self.turn = 1
        self.eaten = 16 - piece
        if self.isgoalstate():
            self.status = 3

def main():
    Game = game()
    while True:
        Game.run()


if __name__ == '__main__':
    main()
