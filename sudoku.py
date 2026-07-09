#!/usr/bin/env python
import sys
from collections import deque

GIVENCOLOR = '\033[4m'
SOLVECOLOR = '\033[31m'
RESETCOLOR = '\033[0m'

inputStr=sys.argv[1]
if len(sys.argv[1])!=81:
    print("Incorrect size:",len(sys.argv[1]),"!=",81)
    sys.exit()
print("Input:", inputStr)

def groupOf(x:int, y:int) -> List[List[int]]:
    xl = list(range(int(x/3)*3, (int(x/3)*3)+3))
    yl = list(range(int(y/3)*3, (int(y/3)*3)+3))
    combs = [(xs, ys) for xs in xl for ys in yl]
    return combs
def rowOf(y:int) -> List[List[int]]:
    return [(x, y) for x in list(range(0,9))]
def colOf(x:int) -> List[List[int]]:
    return [(x, y) for y in list(range(0,9))]
def affectedOf(x:int,y:int) -> List[List[int]]:
    return list(set(groupOf(x,y)+rowOf(y)+colOf(x)))

# iterated for Hidden Single checking
allGroups=[groupOf(0,0),groupOf(3,0),groupOf(6,0),
           groupOf(0,3),groupOf(3,3),groupOf(6,3),
           groupOf(0,6),groupOf(3,6),groupOf(6,6)]
# iterated for Pointing Set checking
allCols=[colOf(i) for i in list(range(0,9))]
allRows=[rowOf(i) for i in list(range(0,9))]

class cell:
    def __init__(self):
        self.isGiven=False
        self.value=None
        self.possibilities={1,2,3,4,5,6,7,8,9}

    # Cell's value has been determined
    def setCell(self, n: int, isGiven=True) -> None:
        self.isGiven=True
        self.value=n
        self.possibilities=[]

    # Mark off a possibility
    # Return True if number has been found
    def demark(self, n: int) -> bool:
        # Value already found
        if self.value!=None or n not in self.possibilities:
            return False
        self.possibilities.discard(n)
        # Only one possibility left
        if len(self.possibilities)==1:
            self.value,=self.possibilities
            self.possibilities=[]
            return True
        # Several possibilities left
        return False

class sudoku:
    def __init__(self):
        self.count=0
        self.workGrid={}
        for y in range(0,9):
            for x in range(0,9):
                self.workGrid[x,y]=cell()

    def isComplete(self) -> bool:
        return self.count<81

    def display(self, grid, givenOnly=False) -> None:
        print("~ "*16)
        for y in range(0,9):
            print('|',end=' ')
            for x in range(0,9):
                val = grid[x,y].value
                giv = grid[x,y].isGiven
                content = str(val) if val and (not givenOnly or giv) else " "
                if giv:
                    print(f"{GIVENCOLOR}"+content+f"{RESETCOLOR}",end=" | " if ((x+1)%3)==0 else "  ")
                else:
                    print(f"{SOLVECOLOR}"+content+f"{RESETCOLOR}",end=" | " if ((x+1)%3)==0 else "  ")
            print("\n"+"~ "*16 if ((y+1)%3)==0 else "")
        print(self.count,"/ 81\n")

    # demark all nodes in shared group, column, and row
    # recursively apply demarking when new number is discovered
    def splash(self,x:int,y:int,n:int) -> None:
        for cx, cy in affectedOf(x,y):
            if self.workGrid[cx,cy].demark(n):
                self.count+=1
                self.splash(cx,cy,self.workGrid[cx,cy].value)
        return

    # force set from given input and use above "splash" on new number
    def set(self, x:int, y:int, n:int) -> bool:
        for cx, cy in affectedOf(x,y):
            if self.workGrid[cx,cy].value==n:
                return False
        self.count+=1
        self.workGrid[x,y].setCell(n)
        self.splash(x,y,n)
        self.HDScan()
        return True

    # Last remaining cell: only one cell in a group with a specific note, has to be that number
    # Given a group, find numbers that only have one potential cell
    # Return whether or not the cell is found to prevent infinite searching
    def HDSingles(self, group: List[List[int]]) -> bool:
        found=False
        cellsWith={i:[] for i in range(1,10)}
        for x,y in group:
            cell = self.workGrid[x,y]
            for n in cell.possibilities:
                cellsWith[n].append((x,y))
        for n, coords in cellsWith.items():
            if len(coords)==1:
                found=True
                self.count+=1
                self.workGrid[coords[0][0],coords[0][1]].setCell(n)
                self.splash(coords[0][0],coords[0][1],n)
        return found
    def HDScan(self, showOutput=False):
        change=True
        while change==True:
            change=False
            for group in allGroups:
                foundHDS=self.HDSingles(group)
                if showOutput:
                    print("Group", int(group[0][0]/3)+(group[0][1])+1,"F,",foundHDS)
                    self.display(self.workGrid)
                change=change or foundHDS

    # repeat usage of set using a long string
    def strSet(self, s:str, showOutput=False) -> None:
        for i, n in enumerate(s):
            if n=='0':
                continue
            if showOutput: print("Adding", n)
            self.set(i%9,int(i/9),int(n))
            if showOutput: self.display(self.workGrid)

        print("Complete.")
        self.display(self.workGrid, True)
        self.display(self.workGrid)

sud = sudoku()
sud.strSet(inputStr)
