# https://pypi.org/project/py-sudoku/

 
from sudoku import Sudoku
from sudokuapp.models import Puzzle,Cell
from datetime import datetime
from django.utils import timezone

def create_puzzle():

    puzzle_pack = Sudoku(3).difficulty(.1) 
    challenge = puzzle_pack.board
    solution = puzzle_pack.solve().board

    puzzle = Puzzle.objects.create(challenge=challenge,solution=solution)
    cell_index = 0
    for row in challenge:
        for val in row:
            Cell.objects.create(puzzle=puzzle,cell_index=cell_index,cell_value = val)
            cell_index += 1
    

     
         

    


  
     

 