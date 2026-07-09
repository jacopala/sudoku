# sudoku
## Usage:
cat hard.txt | xargs ./sudoku.py  
Alternatively,  
./sudoku.py (long number)  
The number represents every sudoku cell from the top-left to the right then to the next row (reading order), with gaps replaced with 0's  

## Strategy:
Each cell begins with a set of all the nubmers from 1-9, representing possibilities  
When cells are set manually, all the other cells in the same column, row, and group have the possibility removed from their own data.  

From the list of sudoku methods at https://sudoku.com/sudoku-rules/, only several strategies need to be established in order to complete each puzzle  
### Currently implemented:  

### Last Possible Cell: If there is only one possibility left for a cell, it will set its own value and recursively trigger itself and other checks

### Hidden Singles: If there is only one mark for a number within an entire group/row/column, then that cell must be the number

^ These two strategies can complete a large majority of Easy-Medium puzzles
Other strategies to implement

### Pointing pair/triples: If the only marks for a number in a group line up, it can be used as a hint for the next row/column
e.g.  
1 x x | x x x | x x x  
x x x | ? ? ? | x x x  <- Any possible placement of 1...
x x x | 2 3 4 | 5 6( ) <- means this spot will be a 1  

### Hidden pair/triples: If marks match up exactly, the cells cannot be any other number  
e.g.  
1 2 3 | 4 5 6 | 7 x x  <- One has to be 8, the other 9  
x x x | x x x | 4 5 6  
x x x | x x x | 1 2( ) <- Only number left is 3  
