# https://pypi.org/project/py-sudoku/

 
from sudoku import Sudoku
from sudokuapp.models import Puzzle,Cell
from datetime import datetime
from django.utils import timezone
import random
from django.utils import timezone
from puzzles.logger import logging

def create_puzzle():
    seed = random.choice([100, 200, 300, 400, 500, 600])
    puzzle_pack = Sudoku(width=3, seed=seed).difficulty(difficulty=.1)
    challenge = puzzle_pack.board
    solution = puzzle_pack.solve().board

    puzzle = Puzzle.objects.create(challenge=challenge, solution=solution)
    cell_index = 0
    for row in challenge:
        for val in row:
            Cell.objects.create(puzzle=puzzle, cell_index=cell_index, cell_value=val)
            cell_index += 1
    puzzle.inProgress = False
    puzzle.save()

def check_grid(cell_index: int, number: int, puzzle: Puzzle) -> Puzzle:
    one_d = [val for row in puzzle.solution for val in row]
    if one_d[cell_index] == number:
        row, col = divmod(cell_index, 9)
        puzzle.challenge[row][col] = number
        puzzle.save()
        cell = puzzle.cells.get(cell_index=cell_index)
        cell.cell_value = number
        cell.save()

    if puzzle.challenge == puzzle.solution:
        puzzle.is_solved = True
        puzzle.inProgress = False
        puzzle.finished_time = datetime.now()
        puzzle.save()
        logging.info(f"Puzzle finished at: {datetime.now()}")

    return puzzle

def calculate_time(puzzle: Puzzle) -> float:
    if puzzle.initial_time and puzzle.finished_time:
        i = timezone.make_aware(puzzle.initial_time) if timezone.is_naive(puzzle.initial_time) else puzzle.initial_time
        f = timezone.make_aware(puzzle.finished_time) if timezone.is_naive(puzzle.finished_time) else puzzle.finished_time
        return round((f - i).total_seconds() / 60, 2)
    return 0

