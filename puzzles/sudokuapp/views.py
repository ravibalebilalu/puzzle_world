from django.shortcuts import render, redirect
from sudokuapp.models import Puzzle,NonUser
from sudokuapp.sudoku_creater import check_grid, create_puzzle, calculate_time
from datetime import datetime
from puzzles.logger import logging

def sudoku_view(request):
    time_taken = None
    

    # Identify user or nonuser
    user = request.user if request.user.is_authenticated else None
    
    if not user:
        session_id = request.session.session_key or request.session.create()
        nonuser, _ = NonUser.objects.get_or_create(session_id=request.session.session_key)
    else:
        nonuser = None

    # Start new puzzle
    if request.method == "POST" and "start-new" in request.POST:
        create_puzzle()
        puzzle = Puzzle.objects.filter(is_solved=False, inProgress=False, user=None, nonuser=None).first()
        if puzzle:
            puzzle.initial_time = datetime.now()
            puzzle.inProgress = True
            puzzle.user = user
            puzzle.nonuser = nonuser
            puzzle.save()
        return redirect("sudoku")

    # Get current active puzzle
    puzzle = Puzzle.objects.filter(is_solved=False, inProgress=True, user=user if user else None, nonuser=nonuser if not user else None).first()

    # No puzzle found: create one
    if not puzzle:
        create_puzzle()
        puzzle = Puzzle.objects.filter(is_solved=False, inProgress=False, user=None, nonuser=None).first()
        if puzzle:
            puzzle.initial_time = datetime.now()
            puzzle.inProgress = True
            puzzle.user = user
            puzzle.nonuser = nonuser
            puzzle.save()
        return redirect("sudoku")

    # Handle cell input
    if request.method == "POST" and "start-new" not in request.POST:
        cell_index = request.POST.get("selected")
        number = request.POST.get("number")

        if cell_index and number:
            cell_index, number = int(cell_index), int(number)
            puzzle = check_grid(cell_index, number, puzzle)
            puzzle.refresh_from_db()

            if puzzle.is_solved:
                time_taken = calculate_time(puzzle)
                logging.info(f"Puzzle completed in {time_taken} minutes")

    context = {
        "grid": puzzle.challenge,
        "cells": puzzle.cells.all(),
        "puzzle": puzzle,
        "time_taken": time_taken
    }

    return render(request, "sudoku.html", context)