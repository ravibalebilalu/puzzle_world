# https://pypi.org/project/py-sudoku/

 
from sudoku import Sudoku

def create_puzzle():
    puzzle = Sudoku(3).difficulty(.1)
    solution = puzzle.solve() 
    return [puzzle.board,solution.board]

 