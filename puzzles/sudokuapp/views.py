from django.shortcuts import render
from sudokuapp.models import Puzzle,Cell
from sudokuapp.sudoku_creater import create_puzzle
 
 

 
def sudoku_view(request):
    #create_puzzle()  
    puzzle = Puzzle.objects.filter(is_solved=False) .first()
    
    if request.POST.getlist("selected"):
        selected_cell = request.POST.get("selected")
        print(selected_cell)
         
    if request.POST.getlist("number"):
        selected_num = request.POST.get("number")
        print(selected_num)
        
    context = {
       "grid"  :puzzle.challenge,
       "cells":puzzle.cells.all(),
       "puzzle":puzzle
        
    }

   
    return render(request,"sudoku.html"   ,context) 