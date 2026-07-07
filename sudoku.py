#!/usr/bin/env python

from collections import deque

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

class cell:
    def __init__(self):
        self.value=None
        self.possibilities={1,2,3,4,5,6,7,8,9}

    # Cell's value has been determined
    def setCell(self, n: int) -> None:
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
        self.grid={}
        for y in range(0,9):
            for x in range(0,9):
                self.grid[x,y]=cell()

    def isComplete(self) -> bool:
        return self.count<81

    def display(self) -> None:
        print("~ "*16)
        for y in range(0,9):
            print('|',end=' ')
            for x in range(0,9):
                val = self.grid[x,y].value
                print(val if val else "?", end=(" | " if ((x+1)%3)==0 else "  "))
            print("\n"+"~ "*16 if ((y+1)%3)==0 else "")
        print(self.count,"/ 81\n")

    def splash(self,x:int,y:int,n:int) -> bool:
        for cx, cy in affectedOf(x,y):
            if self.grid[cx,cy].demark(n):
                self.splash(cx,cy,self.grid[cx,cy].value)
        return True

    def set(self, x:int, y:int, n:int) -> bool:
        for cx, cy in affectedOf(x,y):
            if self.grid[cx,cy].value==n:
                print("Cannot add", n)
                return False
        self.count+=1
        self.grid[x,y].setCell(n)
        self.splash(x,y,n)
        return True
    
    def strSet(self, s:str) -> None:
        for i, n in enumerate(s):
            print(n)
            self.display()
            if n=='0':
                continue
            self.set(i%9,int(i/9),int(n))

constEasyStr="900508007080302905054000080070680032100004008500219060000906001726001040001470056"
sud = sudoku()
sud.strSet(constEasyStr)
sud.display()
