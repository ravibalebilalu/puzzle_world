from django.shortcuts import render
from sudokuapp.models import Puzzle,Cell
from sudokuapp.sudoku_creater import create_puzzle
 
 

 
def sudoku_view(request):
    #create_puzzle()  
    puzzle = Puzzle.objects.filter(is_solved=False) .first()
    
    
    context = {
       "grid"  :puzzle.challenge,
       "cells":puzzle.cells.all(),
       "puzzle":puzzle
        
    }

   
    return render(request,"sudoku.html"   ,context) 