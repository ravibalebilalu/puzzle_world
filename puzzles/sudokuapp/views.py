from django.shortcuts import render, redirect
from sudokuapp.models import Puzzle
from sudokuapp.sudoku_creater import check_grid, create_puzzle, calculate_time
from datetime import datetime
from puzzles.logger import logging

def sudoku_view(request):
    time_taken = None

    # Start new puzzle (on button click)
    if request.method == "POST" and "start-new" in request.POST:
        create_puzzle()
        puzzle = Puzzle.objects.filter(is_solved=False, inProgress=False).first()
        if puzzle:
            puzzle.initial_time = datetime.now()
            puzzle.inProgress = True
            logging.info(f"Puzzle started at : {datetime.now()}")
            puzzle.save()
        return redirect("sudoku")

    # Get the active puzzle
    puzzle = Puzzle.objects.filter(is_solved=False, inProgress=True).first()

    # If not found, create one on first visit (GET or fallback)
    if not puzzle:
        create_puzzle()
        puzzle = Puzzle.objects.filter(is_solved=False, inProgress=False).first()
        if puzzle:
            puzzle.initial_time = datetime.now()
            puzzle.inProgress = True
             
            puzzle.save()
        return redirect("sudoku")

    # Handle number input
    if request.method == "POST":
        cell_index = request.POST.get("selected")
        number = request.POST.get("number")

        if cell_index and number:
            cell_index, number = int(cell_index), int(number)
            puzzle = check_grid(cell_index, number, puzzle)
            puzzle.refresh_from_db()

            if puzzle.is_solved:
                time_taken = calculate_time(puzzle)
                logging.info(f"finished in {time_taken} minuts")

    context = {
        "grid": puzzle.challenge,
        "cells": puzzle.cells.all(),
        "puzzle": puzzle,
        "time_taken": time_taken
    }

    return render(request, "sudoku.html", context)
