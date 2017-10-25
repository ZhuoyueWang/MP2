import read_Puzzle
import copy
from collections import deque
import math
import time
from random import shuffle

global counter
counter = 0
global checkcounter
checkcounter = 0
def freeFlowDumb1 (puzzle,rows,colums,left,variable, values, pos_now, idx):
    if not variable:
        return puzzle
    variable_temp = copy.deepcopy(variable)
    puzzle_temp = copy.deepcopy(puzzle)
    var = variable_temp.pop()
    for value in values:
        i = var[0]
        j = var[1]
        valid = check1(puzzle_temp,var,value)

        if valid:
            puzzle_temp[i][j] = value
            result = freeFlowDumb(puzzle_temp,rows,colums,left,variable_temp,values)
            if result[0][0] != '*':
                return result
            else:
                puzzle_temp[i][j] = puzzle[i][j]
    puzzle_temp[0][0] = '*'
    return puzzle_temp

def freeFlowDumb(puzzle,rows,columns,left, values,sourceA,sourceB,idx,frontier):
    if not frontier:
        return 0
    global counter
    pos_now = frontier.pop()
    counter += 1
    value = values[idx]

    puzzle_temp = copy.deepcopy(puzzle)
    if pos_now == sourceB[idx]:
        if check1(puzzle_temp,idx,values,sourceA[idx],sourceB[idx],rows,columns):
            if left == 1:
                print('done')
                print(counter)
                return puzzle
            pos_now = sourceA[idx+1]

            result = freeFlowDumb(puzzle_temp,rows,columns,left-1,values,sourceA,sourceB,idx+1,[pos_now])
            if result != 0 :
                return result
            return 0
        else:
            return 0
    else:
        if puzzle_temp[pos_now[0]][pos_now[1]] == '_':
            puzzle_temp[pos_now[0]][pos_now[1]] = value
        neighbors = getNeighbor(pos_now,rows,columns)
        shuffle(neighbors)
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            #print(neighbor)
            if puzzle_temp[neighbor[0]][neighbor[1]] == '_' or neighbor == sourceB[idx]:
                frontier.append(neighbor)
                result = freeFlowDumb(puzzle_temp,rows,columns,left,values,sourceA,sourceB,idx,frontier)
                if result != 0:
                    return result
        return 0


def freeFlowSmart(puzzle,rows,columns,left, values,sourceA,sourceB,idx,frontier):
    if not frontier:
        return 0
    pos_now = frontier.pop()
    value = values[idx]
    global counter
    counter += 1
    global checkcounter

    puzzle_temp = copy.deepcopy(puzzle)
    if pos_now == sourceB[idx]:
        #print(checkcounter)

        if check1(puzzle_temp,idx,values,sourceA[idx],sourceB[idx],rows,columns):
            if left == 1:
                print('done')
                print(counter)
                return puzzle

            pos_now = sourceA[idx+1]

            result = freeFlowSmart(puzzle_temp,rows,columns,left-1,values,sourceA,sourceB,idx+1,[pos_now])
            if result != 0 :
                return result
            return 0
        else:
            return 0
    else:
        if puzzle_temp[pos_now[0]][pos_now[1]] == '_' or  pos_now == sourceA[idx]:
            puzzle_temp[pos_now[0]][pos_now[1]] = value
            check_move = check2(puzzle_temp,idx,values,sourceA,sourceB,rows,columns)
            if not check_move:
                puzzle_temp[pos_now[0]][pos_now[1]] = '_'
            else:
                neighbors = getNeighbor(pos_now,rows,columns)
                for i in range(len(neighbors)):
                    neighbor = neighbors[i]
            #print(neighbor)
                    if puzzle_temp[neighbor[0]][neighbor[1]] == '_' or neighbor == sourceB[idx]:
                        frontier.append(neighbor)
                        result = freeFlowSmart(puzzle_temp,rows,columns,left,values,sourceA,sourceB,idx,frontier)
                        if result != 0:
                            return result
        return 0

def freeFlowEcSmart(puzzle,rows,columns,left, values,sourceA,sourceB,idx,frontier):
    if not frontier:
        return 0
    pos_now = frontier.pop()
    #print(puzzle)
    value = values[idx]
    global counter
    counter += 1
    global checkcounter
    #print(puzzle)
    #print(frontier)
    #puzzle_temp = copy.deepcopy(puzzle)
    if pos_now == sourceB[idx]:
        #print(checkcounter)
        check_move3 = check3(puzzle, rows, columns, value)
        check_move4 = check4(puzzle, rows, columns, sourceA, sourceB,idx,values)

        if check1(puzzle,idx,values,sourceA[idx],sourceB[idx],rows,columns) and check_move3 and check_move4:
            if left == 1:
                print('done')
                print(counter)
                return puzzle
            #ordered_values,ordered_A,ordered_B = ordering (idx,values,sourceA,sourceB,puzzle,rows,columns)
            # pos_now = ordered_A[idx+1]
            # result = freeFlowEcSmart(puzzle,rows,columns,left-1,ordered_values,ordered_A,ordered_B,idx+1,[pos_now])
            pos_now = sourceA[idx + 1]
            result = freeFlowEcSmart(puzzle, rows, columns, left - 1, values, sourceA, sourceB, idx + 1,[pos_now])
            if result != 0 :
                return result
            return 0
        else:
            return 0
    else:
        if puzzle[pos_now[0]][pos_now[1]] == '_' or  pos_now == sourceA[idx]:
            puzzle[pos_now[0]][pos_now[1]] = value
            check_move2 = check2(puzzle,idx,values,sourceA,sourceB,rows,columns)
            #check_move4 = check4(puzzle, rows, columns, sourceA, sourceB,idx,values)

            #print(check_move3)
            if (not check_move2) :
                puzzle[pos_now[0]][pos_now[1]] = '_'
            else:
                neighbors = getNeighbor(pos_now,rows,columns)
                for i in range(len(neighbors)):
                    neighbor = neighbors[i]
            #print(neighbor)
                    if puzzle[neighbor[0]][neighbor[1]] == '_' or neighbor == sourceB[idx]:
                        frontier.append(neighbor)
                        result = freeFlowEcSmart(puzzle,rows,columns,left,values,sourceA,sourceB,idx,frontier)
                        if result != 0:
                            return result
            if pos_now != sourceA[idx]:
                puzzle[pos_now[0]][pos_now[1]] = '_'
        return 0


def freeFlowSmart1(puzzle,rows,columns,left, values,sourceA,sourceB,idx,frontier):
    if not frontier:
        return 0
    pos_now = frontier.pop()
    value = values[idx]
    global counter
    counter += 1
    puzzle_temp = copy.deepcopy(puzzle)
    if pos_now == sourceB[idx]:

        if check1(puzzle_temp,idx,values,sourceA[idx],sourceB[idx],rows,columns) and check2(puzzle_temp,idx,values,sourceA,sourceB,rows,columns):
            if left == 1:
                print('done')
                print(counter)
                return puzzle
            pos_now = sourceA[idx+1]

            result = freeFlowSmart1(puzzle_temp,rows,columns,left-1,values,sourceA,sourceB,idx+1,[pos_now])
            if result != 0 :
                return result
            return 0
        else:
            return 0
    else:
        if puzzle_temp[pos_now[0]][pos_now[1]] == '_' or  pos_now == sourceA[idx]:
            puzzle_temp[pos_now[0]][pos_now[1]] = value
            #print(check2(puzzle_temp,idx,values,sourceA,sourceB,rows,columns))
        neighbors = getNeighbor_ordered(pos_now,rows,columns)
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            #print(neighbor)
            if puzzle_temp[neighbor[0]][neighbor[1]] == '_' or neighbor == sourceB[idx]:
                frontier.append(neighbor)
                result = freeFlowSmart1(puzzle_temp,rows,columns,left,values,sourceA,sourceB,idx,frontier)
                if result != 0:
                    return result
        return 0

def check1(puzzle,idx,values,sourceA,sourceB,rows,columns):
    value = values[idx]
    # first check if the sourceA has only one same color source
    neighbors = getNeighbor(sourceA,rows,columns)
    count = 0
    for i in range(len(neighbors)):
        if puzzle[neighbors[i][0]][neighbors[i][1]] == value:
            count += 1
    if count != 1:
        return False

    # first check if the sourceB has only one same color source
    neighbors = getNeighbor(sourceB,rows,columns)
    count = 0
    for i in range(len(neighbors)):
        if puzzle[neighbors[i][0]][neighbors[i][1]] == value:
            count += 1
    if count != 1:
        return False

    # check non-source node
    for row in range(rows):
        for column in range(columns):
            if [row,column] != sourceA and [row,column] != sourceB:
                if puzzle[row][column] == value:
                    count = 0
                    neighbors = getNeighbor([row,column],rows,columns)
                    for i in range(len(neighbors)):

                        if puzzle[neighbors[i][0]][neighbors[i][1]] == value:
                            count += 1
                    if count != 2:
                        return False
    return True

def check2(puzzle,idx,values,sourceA,sourceB,rows,columns):
    # check if there still are paths for other colors
    global checkcounter
    checkcounter += 1
    #print(checkcounter)
    #puzzle_temp = copy.deepcopy(puzzle)
    for i in range(idx+1,len(values)):
        A = sourceA[i]
        B = sourceB[i]
        value = values[i]
        # using BFS to determine whether there is still path between A and B
        frontier = deque([A])
        if not pathAvailable(puzzle,frontier,B,rows,columns,value):
            return False

    return True

def check3(puzzle,rows,columns,value):
    #print(puzzle)
    for i in range(rows):
        for j in range(columns):
            node_now = puzzle[i][j]
            if node_now == "_":
                neighbors = getNeighbor([i,j],rows,columns)
                count = 0
                for k in range(len(neighbors)):
                    neighborx = neighbors[k][0]
                    neighbory = neighbors[k][1]
                    if  puzzle[neighborx][neighbory] == value:
                        count += 1
                if count >= len(neighbors) - 1:
                    #print(i,j)
                    #print(puzzle)
                    return False
    return True

def check4(puzzle,rows,columns,sourceA,sourceB,idx,values):
    # check if there is isolated blank area
    modified = []
    for i in range (rows):
        for j in range(columns):
            node_now = puzzle[i][j]
            # start from a blank
            if node_now == "_":
                # using BFS to determine whether there is still path to source node
                A = [i,j]
                frontier = deque([A])
                indicator = False
                block_sourceA_neighbor = []
                block_sourceB_neighbor = []
                block_neighbor = []
                while not (not frontier):

                    A = frontier.popleft()
                    #print(A)
                    x = A[0]
                    y = A[1]
                    puzzle[x][y] = 'X'
                    modified.append([x, y])
                            # print(puzzle)
                    neighbors = getNeighbor(A, rows, columns)
                    for m in range(len(neighbors)):
                        neighbor = neighbors[m]
                            # print(neighbor)
                        # if indicator == False:
                        #     value_neighbor = puzzle[neighbor[0]][neighbor[1]]
                        #     if value_neighbor in values[idx:]:
                        #         if value_neighbor in block_neighbor:
                        #             indicator = True
                        #         else:
                        #             block_neighbor.append(value_neighbor)
                        #     if puzzle[neighbor[0]][neighbor[1]] == values[idx]:
                        #         indicator = True
                        #     else:
                        if neighbor in sourceA[idx+1:]:
                            block_sourceA_neighbor.append(sourceA.index(neighbor))

                        elif neighbor in sourceB[idx+1:]:
                            block_sourceB_neighbor.append(sourceB.index(neighbor))
                        #       if neighbor in sourceA[idx:] or neighbor in sourceB[idx:]:
                        #          indicator = True
                        elif puzzle[neighbor[0]][neighbor[1]] == '_':
                            frontier.append(neighbor)
                # if not indicator:
                indicator = bool(set(block_sourceA_neighbor) & set(block_sourceB_neighbor))
                #print(indicator)
                #print(puzzle)
                if not indicator:
                    #print(puzzle)
                    for k in range(len(modified)):
                        x = modified[k][0]
                        y = modified[k][1]
                        puzzle[x][y] = '_'
                    #print(False)
                    return False

    for k in range(len(modified)):
        x = modified[k][0]
        y = modified[k][1]
        puzzle[x][y] = '_'
    #print(True)
    return True




def pathAvailable(puzzle,frontier,B,rows,columns,value):
    modified = []
    while not (not frontier):
        A = frontier.popleft()
        if A == B :
            for k in range(len(modified)):
                x = modified[k][0]
                y = modified[k][1]
                puzzle[x][y] = '_'
            return True
        x = A[0]
        y = A[1]
        if puzzle[x][y] == '_':
            puzzle[x][y] = 'X'
            modified.append([x,y])
            #print(puzzle)
        neighbors = getNeighbor(A,rows,columns)
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
        #print(neighbor)
            if puzzle[neighbor[0]][neighbor[1]] == '_' or neighbor == B:
                frontier.append(neighbor)

    for k in range(len(modified)):
        x = modified[k][0]
        y = modified[k][1]
        puzzle[x][y] = '_'
    return False

def getNeighbor(pos,rows,columns):
    neighbors = []
    i_lower = max(0,pos[0] - 1)
    i_upper = min(columns-1,pos[0]+1)
    j_lower = max(0,pos[1] - 1)
    j_upper = min(rows-1,pos[1] + 1)


    if (j_upper != pos[1]):
        neighbors.append([pos[0],j_upper])
    if (j_lower != pos[1]):
        neighbors.append([pos[0],j_lower])
    if (i_lower != pos[0]):
        neighbors.append([i_lower,pos[1]])
    if (i_upper != pos[0]):
        neighbors.append([i_upper,pos[1]])
    return neighbors

def getNeighbor_new(pos,rows,columns):
    neighbors = []
    i_lower = max(0,pos[0] - 1)
    i_upper = min(columns-1,pos[0]+1)
    j_lower = max(0,pos[1] - 1)
    j_upper = min(rows-1,pos[1] + 1)
    #print(i_lower,i_upper,j_upper,j_lower)
    if (0 == pos[1]) or (rows-1 == pos[1]):
        if (i_lower != pos[0]):
            neighbors.append([i_lower,pos[1]])
        if (i_upper != pos[0]):
            neighbors.append([i_upper,pos[1]])
        if (j_upper != pos[1]):
            neighbors.append([pos[0],j_upper])
        if (j_lower != pos[1]):
            neighbors.append([pos[0],j_lower])
    else:
        if (j_upper != pos[1]):
            neighbors.append([pos[0],j_upper])
        if (j_lower != pos[1]):
            neighbors.append([pos[0],j_lower])
        if (i_lower != pos[0]):
            neighbors.append([i_lower,pos[1]])
        if (i_upper != pos[0]):
            neighbors.append([i_upper,pos[1]])
    return neighbors


def getNeighbor_ordered(pos,rows,columns):
    neighbors = []
    i_lower = max(0,pos[0] - 1)
    i_upper = min(columns-1,pos[0]+1)
    j_lower = max(0,pos[1] - 1)
    j_upper = min(rows-1,pos[1] + 1)
    #print(i_lower,i_upper,j_upper,j_lower)

    if (j_upper != pos[1]):
        neighbors.append([pos[0],j_upper])
    if (j_lower != pos[1]):
        neighbors.append([pos[0],j_lower])
    if (i_lower != pos[0]):
        neighbors.append([i_lower,pos[1]])
    if (i_upper != pos[0]):
        neighbors.append([i_upper,pos[1]])
    # order them with respect to the distance to the wall
    distance = []
    neighborsNew = []
    for i in range(len(neighbors)):
        A = neighbors[i]
        dist = abs(A[0] - 0) * abs(A[0] - (rows - 1)) * abs(A[1] - 0) * abs(A[1] - (columns - 1))
        distance.append([dist, i])
    distance = (sorted(distance, key = lambda length:length[0]))
    for i in range(len(distance)):
        idx = distance[i][1]
        neighborsNew.append(neighbors[idx])
    return(neighborsNew)

def heuristic(A,B,rows,columns):
    distance = []
    for i in range(len(A)):
        dist = abs(A[i][0] - 0) * abs(A[i][0] - (rows-1)) * abs(A[i][1] - 0) * abs(A[i][1]- (columns - 1))
        distance.append([dist,i])
    return(sorted(distance, key = lambda length:length[0]))

def ordering (idx,values,sourceA,sourceB,puzzle,rows,columns):
    order =  []
    for i in range(idx+1,len(values)):
        A = sourceA[i]
        B = sourceB[i]
        neighborA = getNeighbor(A,rows,columns)
        neighborB = getNeighbor(B,rows,columns)
        count = 0
        for j in range(len(neighborA)):
            neighborAx = neighborA[j][0]
            neighborAy = neighborA[j][1]
            if puzzle[neighborAx][neighborAy] == "_":
                count += 1
        for j in range(len(neighborB)):
            neighborBx = neighborB[j][0]
            neighborBy = neighborB[j][1]
            if puzzle[neighborBx][neighborBy] == "_":
                count += 1
        order.append([count,i])
    order = sorted(order, key = lambda length:length[0])
    ordered_values = []
    ordered_sourceA = []
    ordered_sourceB = []
    for i in range(idx+1):
        ordered_values.append(values[i])
        ordered_sourceA.append(sourceA[i])
        ordered_sourceB.append(sourceB[i])
    for i in range(idx+1,len(values)):
        index = order[i - idx - 1][1]
        ordered_values.append(values[index])
        ordered_sourceA.append(sourceA[index])
        ordered_sourceB.append(sourceB[index])
    return ordered_values,ordered_sourceA,ordered_sourceB



def main():
    [puzzle, rows, columns, left,  values,sourceA, sourceB] = read_Puzzle.generatePuzzle()
    print(puzzle)
    print(values)
    center = [math.floor(rows/2),math.floor(columns/2)]
    #order = heuristic(sourceA,sourceB,rows,columns)
    #order = order[::-1]
    idx = 0
    # for i in range(20000):
    #     check2(puzzle,idx,values,sourceA,sourceB,rows,columns)
    # print("done")
    Fordumb = []
    for i in range(len(values)):
        Fordumb.append([values[i],sourceA[i],sourceB[i]])
    shuffle(Fordumb)
    values_for_dumb = []
    sourceA_for_dumb = []
    sourceB_for_dumb = []
    for i in range(len(values)):
        values_for_dumb.append(Fordumb[i][0])
        sourceA_for_dumb.append(Fordumb[i][1])
        sourceB_for_dumb.append((Fordumb[i][2]))
    order = [[0,0],[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]]
    pos_now = sourceA[order[idx][1]]
    #pos_now = sourceA[0]
    # global count
    # count = 0
    #result = freeFlowSmart(puzzle,rows,columns,left, values,sourceA,sourceB,idx, [pos_now],order)
    ordered_values,ordered_A,ordered_B = ordering(-1, values, sourceA, sourceB, puzzle, rows, columns)
    #pos_now = ordered_A[idx]
    start = time.time()
    #result = freeFlowEcSmart(puzzle, rows, columns, left, ordered_values, ordered_A, ordered_B, idx, [pos_now])
    result = freeFlowEcSmart(puzzle, rows, columns, left, values, sourceA, sourceB, idx, [pos_now])
    #result = freeFlowDumb(puzzle, rows, columns, left, values_for_dumb, sourceA_for_dumb, sourceB_for_dumb, idx, [sourceA_for_dumb[idx]])
    end = time.time()
    print(end-start)
    print(result)
if __name__ == "__main__":
    main()