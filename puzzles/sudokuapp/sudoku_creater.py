# https://pypi.org/project/py-sudoku/

 
from sudoku import Sudoku

def create_puzzle():
    puzzle = Sudoku(3).difficulty(.1)
    solution = puzzle.solve() 
    return [puzzle.board,solution.board]

def validate_puzzle(row,col,val,puzzle):
    # compare cell value of puz_sol and puz_ch
    valid = val == puzzle.solution[row][col]
     
    if valid:
        puzzle.challenge[row][col] = val
        puzzle.save()
         
    # check all values are same in both grids
    puzzle_compleated = puzzle.challenge== puzzle.solution
    if puzzle_compleated:
        puzzle.is_solved = True
        
        puzzle.save()
        
    return [valid,puzzle.is_solved]
         
    
    
     

    

     

