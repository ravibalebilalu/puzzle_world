# https://pypi.org/project/py-sudoku/

 
from sudoku import Sudoku
from datetime import datetime
from django.utils import timezone
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
        puzzle.finished_time = datetime.today()
        puzzle.inProgress = False
        puzzle.save() 
    return [valid,puzzle.is_solved]
         
    
def calculate_time(puzzle):
    
    if puzzle.is_solved and puzzle.initial_time and puzzle.finished_time:
            initial_time = timezone.make_aware(puzzle.initial_time) if timezone.is_naive(puzzle.initial_time) else puzzle.initial_time
            finished_time = timezone.make_aware(puzzle.finished_time) if timezone.is_naive(puzzle.finished_time) else puzzle.finished_time
            time_taken = finished_time - initial_time
            time_taken = round(time_taken.total_seconds())
    else:
        time_taken=0
    return time_taken
     

    

     

