# https://pypi.org/project/py-sudoku/

 
from sudoku import Sudoku
from sudokuapp.models import Puzzle,Cell
from datetime import datetime
from django.utils import timezone
import random
from django.utils import timezone
from puzzles.logger import logging

def create_puzzle()-> None:
    seed = random.choice([100,200,300,400,500,600])
    puzzle_pack = Sudoku(width=3,seed=seed).difficulty(difficulty=.1) 
    challenge = puzzle_pack.board
    solution = puzzle_pack.solve().board
    

    puzzle = Puzzle.objects.create(challenge=challenge,solution=solution)
    cell_index = 0
    for row in challenge:
        for val in row:
            Cell.objects.create(puzzle=puzzle,cell_index=cell_index,cell_value = val)
            cell_index += 1
    puzzle.inProgress = False
     
    
    puzzle.save()
    

     
         
def check_grid(cell_index:int,number:int,puzzle:Puzzle) -> Puzzle:
    """_summary_

    Args:
        cell_index (int): 0 to 80
        number (int): 1 to 9
        puzzle (Puzzle):  Puzzle.challenge 

    Returns:
        Puzzle:  Puzzle
    """
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
        puzzle.finished_time = datetime.now()
        puzzle.save()
        logging.info(f"puzzle finished at : {datetime.now()}")

    return puzzle

def calculate_time(puzzle:Puzzle)-> float:
    """_summary_

    Args:
        puzzle (Puzzle): solved puzzle

    Returns:
        float: difference in finished_time and initial_time in minuts
    """
    if puzzle.initial_time and puzzle.finished_time:
        initial_time = timezone.make_aware(puzzle.initial_time) if timezone.is_naive(puzzle.initial_time) else puzzle.initial_time
        finished_time = timezone.make_aware(puzzle.finished_time) if timezone.is_naive(puzzle.finished_time) else puzzle.finished_time
        time_taken = finished_time - initial_time
        time_taken = round(time_taken.total_seconds()/60,2)
        return time_taken
    return 0
     
     
    


  
     

 