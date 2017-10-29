import numpy as np
import mpmath as math
import matplotlib as mpl
import matplotlib.pyplot as plt


def puzzleInput (puzzle,filename):
    puzzleFile = open(filename, "r")
    columns = puzzleFile.readlines()
    for column in columns:
        column = column.strip()
        row = [i for i in column]
        puzzle.append(row)


def generatePuzzle():
    puzzle =[]
    puzzleInput(puzzle,"input991.txt")
    [rows,columns] = np.shape(puzzle)

    sourceA = []
    sourceB = []
    values = []
    for i in range(rows):
        for j in range(columns):
            value = puzzle[i][j]
            if value !=  '_':
                if value not in values:
                    values.append(value)
                    sourceA.append([i,j])
                    sourceB.append([0,0])
                else:
                    idx = values.index(value)
                    sourceB[idx] = [i,j]
    return puzzle, rows, columns, len(values), values , sourceA, sourceB

