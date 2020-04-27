#! /usr/bin/python3
import sys
import time

board = [0] * 81
Neighbors = [0] * 81

cliques = [[0,1,2,3,4,5,6,7,8],\
[9,10,11,12,13,14,15,16,17],\
[18,19,20,21,22,23,24,25,26],\
[27,28,29,30,31,32,33,34,35],\
[36,37,38,39,40,41,42,43,44],\
[45,46,47,48,49,50,51,52,53],\
[54,55,56,57,58,59,60,61,62],\
[63,64,65,66,67,68,69,70,71],\
[72,73,74,75,76,77,78,79,80],\
[0,9,18,27,36,45,54,63,72],\
[1,10,19,28,37,46,55,64,73],\
[2,11,20,29,38,47,56,65,74],\
[3,12,21,30,39,48,57,66,75],\
[4,13,22,31,40,49,58,67,76],\
[5,14,23,32,41,50,59,68,77],\
[6,15,24,33,42,51,60,69,78],\
[7,16,25,34,43,52,61,70,79],\
[8,17,26,35,44,53,62,71,80],\
[0,1,2,9,10,11,18,19,20],\
[3,4,5,12,13,14,21,22,23],\
[6,7,8,15,16,17,24,25,26],\
[27,28,29,36,37,38,45,46,47],\
[30,31,32,39,40,41,48,49,50],\
[33,34,35,42,43,44,51,52,53],\
[54,55,56,63,64,65,72,73,74],\
[57,58,59,66,67,68,75,76,77],\
[60,61,62,69,70,71,78,79,80]\
]

class MyStack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop()

def main():
    start = time.time()
    makeNeighbors()
    input = open(sys.argv[1], "r+")
    output = open(sys.argv[2], "w+")
    arg = sys.argv[3]
    inputs = input.read()
    boards = inputs.split("\n")
    for idx in range(len(boards)):
        boards[idx] = boards[idx].strip("\r")
    i = 0
    x = False
    for idx in range(len(boards)):
        if arg in boards[idx]:
            x = True
        if x == True:
            if len(boards[idx]) == 17:
                args = boards[idx].split(",")
                for j in range(9):
                    board[i] = args[j]
                    i += 1
            if i == 81:
                x = False
    solve()
    count = 0
    for idx in range(81):
        output.write(board[idx])
        count += 1
        if count % 9 != 0:
            output.write(",")
        else:
            output.write("\n")
    print(time.time() - start)

def solve():
    state = "NEW_CELL"
    nback = 0
    mystack = MyStack()
    num = 1
    cell = nextOpenCell()
    while True:
        if state == "NEW_CELL":
            worked = False
            num = 1
            while num < 10:
                board[cell] = str(num)
                if work(cell):
                    mystack.push(cell)
                    state = "FIND_NEXT_CELL"
                    worked = True
                    break
                else:
                    num += 1
            if not worked:
                board[cell] = "_"
                state = "BACKTRACK"
            continue
        if state == "FIND_NEXT_CELL":
            cell = nextOpenCell()
            if cell < 0:
                print(nback)
                break
            state = "NEW_CELL"
            continue
        if state == "BACKTRACK":
            worked = False
            nback += 1
            cell = mystack.pop()
            old_guess = board[cell]
            if int(old_guess) != 9:
                num = int(old_guess) + 1
            else:
                worked = False
            while num < 10:
                board[cell] = str(num)
                if work(cell):
                    mystack.push(cell)
                    state = "FIND_NEXT_CELL"
                    worked = True
                    break
                else:
                    num += 1
            if not worked:
                board[cell] = "_"
                state = "BACKTRACK"
            continue

def makeNeighbors():
    for cell in range(81):
        nb = set()
        for clique in cliques:
            if cell in clique:
                nb.update(clique)
        nb.discard(cell)
        Neighbors[cell] = nb

def nextOpenCell():
    idx = 0
    while idx < len(board):
        if board[idx] == "_":
            return idx
        idx += 1
    return -1

def work(cell):
    val = board[cell]
    for neighbor in Neighbors[cell]:
            if board[neighbor] == val:
                return False
    return True

main()
