from django.shortcuts import render,redirect
from sudokuapp.models import Puzzle,Cell
from sudokuapp.sudoku_creater import create_puzzle,check_grid
 
 

 
def sudoku_view(request):
    if request.method == "POST":
        puzzle = Puzzle.objects.filter(is_solved=False, inProgress=True).first()
        cell_index = request.POST.get("selected")
        number = request.POST.get("number")

        if puzzle and cell_index and number:
            cell_index, number = int(cell_index), int(number)
            puzzle = check_grid(cell_index, number, puzzle)
            puzzle.refresh_from_db()

            if puzzle and puzzle.is_solved:
                # ✅ Avoid stale object, trigger fresh reload
                return redirect("sudoku")

    # 📦 Get or create puzzle (ALWAYS)
    puzzle = Puzzle.objects.filter(is_solved=False, inProgress=True).first()
    if not puzzle:
        create_puzzle()
        puzzle = Puzzle.objects.filter(is_solved=False, inProgress=True).first()

    
    

    context = {
        "grid": puzzle.challenge,
        "cells": puzzle.cells.all(),
        "puzzle": puzzle
    }

    return render(request, "sudoku.html", context)
