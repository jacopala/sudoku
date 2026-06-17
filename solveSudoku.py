#!/usr/bin/env python
import sys

size = int(input("Enter size of squares: "))
sizesqrt = int(size**(1/2))
if sizesqrt!=(size**(1/2)):
    print('not perfect square')
    sys.exit(1)

possiblenums = str(list(range(1,size+1)))

print(possiblenums)

sudoku=""

rowsAdded=0
while rowsAdded<size:
    row = input("Enter next row: ")
    if len(row)!=size:
        print("Try again.")
    else:
        newRow = ""
        validRow = True
        for c in row:
            if c not in possiblenums:
                validRow = False
                print("invalid row")
                break
            else:
                newRow+=c
        if validRow:
            sudoku+=newRow
            for i in range(len(sudoku)):
                print(sudoku[i],end='')
                if (i+1)%size==0:
                    print()
            rowsAdded+=1
            print()
def getRows(inp: str) -> List[str]:
    size = len(inp)
    rowSize = int(size**(1/2))
    rows = []
    for i in range(rowSize):
        rows.append(sudoku[rowSize*i:rowSize*i+rowSize])
    return rows
def getCols(inp:str) -> List[str]:
    size = len(inp)
    colSize = int(size**(1/2))
    cols = []
    for i in range(colSize):
        cols.append(sudoku[i:colSize*(colSize)+i:colSize])
    return cols
def getGroups(inp:str) -> List[str]:
    size = len(inp)
    groupSize = int(size**(1/2))
    groupLen = int(groupSize**(1/2))

    groups = [""]*groupSize

    for i,char in enumerate(inp):
        row = i//groupSize
        col = i % groupSize

        index=(row//groupLen)*groupLen+(col//groupLen)
        groups[index]+=char

    return groups


def _firstTest(inp: str):
    print("rows:", getRows(inp))
    print("cols:", getCols(inp))
    print("groups:", getGroups(inp))
    print(possiblenums)

_firstTest(sudoku)
