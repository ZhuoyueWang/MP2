from search_4pt import *
import sys
import math
import time
import random
import pygame

class game:
    def __init__(self):
        pygame.init()
        self.size = int(560/8)
        self.board = 0
        self.clock = pygame.time.Clock()
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
        self.matrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

    def run(self):
        self.clock.tick(60)
        # clear the screen
        self.status = 5
        if self.status == 5:
            # Black
            if self.turn == 1:
                start = time.clock()
                self.move(2, 4)
                self.totalTime1 += (time.clock() - start)
                self.totalStep1 += 1
                for i in self.matrix:
                    print(i)
                print('\n')
            elif self.turn == 2:
                start = time.clock()
                self.move(2, 2)
                self.totalTime2 += (time.clock() - start)
                self.totalStep2 += 1
                for i in self.matrix:
                    print(i)
                print('\n')

        for event in pygame.event.get():
            # Quit if close the windows
            if event.type == pygame.QUIT:
                exit()
            elif self.status == 0:
                x, y = event.pos
                coor_y = math.floor(x / self.size)
                coor_x = math.floor(y / self.size)
                if self.matrix[coor_x][coor_y] == self.turn:
                    self.status = 1
                    self.y = math.floor(x / self.size)
                    self.x = math.floor(y / self.size)
            # check whether the selected chess can move, otherwise select other chess
            elif self.status == 1:
                x, y = event.pos
                self.newY = math.floor(x / self.size)
                self.newX = math.floor(y / self.size)
                if self.isabletomove():
                    self.movechess()
                    if (self.newX == 4 and self.matrix[self.newX][self.newY] == 1) or (self.newX == 0 and self.matrix[self.newX][self.newY] == 2):
                        self.status = 3
                elif self.matrix[self.newX][self.newY] == self.matrix[self.x][self.y]:
                    self.x = self.newX
                    self.y = self.newY
        self.display()

    def display(self):
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
                for i in self.matrix:
                    print(i)
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
                for i in self.matrix:
                    print(i)
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

            if self.matrix[self.x][self.y] == 2:
                x1 = self.x - 1
                y1 = self.y - 1
                x2 = self.x - 1
                y2 = self.y + 1
                x3 = self.x - 1
                y3 = self.y

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
        board, nodes, piece = search(self.matrix, self.turn, 5, function_type).alphabet()
        self.moveNode(board,nodes,piece)

    def moveNode(self,board,nodes,piece):
        self.matrix = board.getmatrix()
        if self.turn == 1:
            self.totalNode1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.totalNode2 += nodes
            self.turn = 1
        self.eaten = 20-piece
        if self.done():
            self.status = 3

    def done(self):
        count = 0
        for i in self.matrix[0]:
            if i == 2:
                count += 1
        if count == 3:
            return True
        count = 0
        for i in self.matrix[4]:
            if i == 1:
                count += 1
        if count == 3:
            return True
        count1 = 0
        count2 = 0
        for line in self.matrix:
            for i in line:
                if i == 1:
                    count1 += 1
                elif i == 2:
                    count2 += 1
        if count1 <= 2 or count2 <= 2:
            return True
        return False

def main():
    Game = game()
    while True:
        Game.run()


if __name__ == '__main__':
    main()
