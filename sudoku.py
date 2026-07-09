#!/usr/bin/env python

from collections import deque

GIVENCOLOR = '\033[35m'
RESETCOLOR = '\033[0m'

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

allGroups=[groupOf(0,0),groupOf(3,0),groupOf(6,0),
           groupOf(0,3),groupOf(3,3),groupOf(6,3),
           groupOf(0,6),groupOf(3,6),groupOf(6,6)]

class cell:
    def __init__(self):
        self.isGiven=False
        self.value=None
        self.possibilities={1,2,3,4,5,6,7,8,9}

    # Cell's value has been determined
    def setCell(self, n: int) -> None:
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

    def display(self, grid, showCount=True) -> None:
        print("~ "*16)
        for y in range(0,9):
            print('|',end=' ')
            for x in range(0,9):
                val = grid[x,y].value
                giv = grid[x,y].isGiven
                content = str(val) if val else " "
                if giv:
                    print(f"{GIVENCOLOR}"+content+f"{RESETCOLOR}",end=" | " if ((x+1)%3)==0 else "  ")
                else:
                    print(content,end=" | " if ((x+1)%3)==0 else "  ")
            print("\n"+"~ "*16 if ((y+1)%3)==0 else "")
        if showCount: print(self.count,"/ 81\n")
        else: print()

    # demark all nodes in shared group, column, and row
    # recursively apply demarking when new number is discovered
    def splash(self,x:int,y:int,n:int) -> bool:
        for cx, cy in affectedOf(x,y):
            if self.workGrid[cx,cy].demark(n):
                self.count+=1
                self.splash(cx,cy,self.workGrid[cx,cy].value)
        return True

    # force set from given input and use above "splash" on new number
    def set(self, x:int, y:int, n:int) -> bool:
        for cx, cy in affectedOf(x,y):
            if self.workGrid[cx,cy].value==n:
                return False
        self.count+=1
        self.workGrid[x,y].setCell(n)
        self.splash(x,y,n)
        return True

    # Last remaining cell:
    def LRC(self) -> bool:
        found=False

    # repeat usage of set using a long string
    def strSet(self, s:str, showOutput=False) -> None:
        for i, n in enumerate(s):
            if n=='0':
                continue
            if showOutput: self.display(self.workGrid)
            if not self.set(i%9,int(i/9),int(n)):
                if showOutput:
                    print("Complete.")
                else:
                    self.display(self.workGrid)
                return
            if showOutput: print("Adding", n)
        if showOutput: print("Not enough clues.")
        return

constEasyStr="300049000000600501752001000001000700500396000008150096003010060004000100000028000"
sud = sudoku()
sud.strSet(constEasyStr)
