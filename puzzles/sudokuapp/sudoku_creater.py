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
    puzzle.inProgress = True
    puzzle.save()
    

     
         
def check_grid(cell_index,number,puzzle):
    pu_so = puzzle.solution
    one_d = [element for sublist in pu_so for element in sublist]
    if one_d[cell_index] == number:
         row,col = divmod(cell_index,9)
         puzzle.challenge[row][col] = number
         puzzle.save()

         cell = puzzle.cells.get(cell_index=cell_index)
         cell.cell_value = number
         cell.save()
    if puzzle.challenge == puzzle.solution:
    
        puzzle.is_solved = True
        puzzle.inProgress=False
        puzzle.save()
         
        
          
    return puzzle
     
     
    


  
     

 