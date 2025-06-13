from django.shortcuts import render
from sudokuapp.sudoku_creater import create_puzzle,validate_puzzle
from sudokuapp.models import Puzzle
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def sudoku_view(request):
    puzzle = Puzzle.objects.filter(is_solved = False).first()
    
    if not puzzle or puzzle.is_solved:
        new_puzzle = create_puzzle()
        
        puzzle = Puzzle.objects.create(challenge=new_puzzle[0],solution=new_puzzle[1])
         
         
    
    puz_ch = puzzle.challenge
    
    if request.method == "POST":
        data = json.loads(request.body)
        row,col,val = int(data["row"]),int(data["col"]),int(data["val"])
        valid,is_completed = validate_puzzle(row,col,val, puzzle)
        print(f"is_compleated view--- json;{is_completed}")
        print(f"compleated in model json ; {puzzle.is_solved}")
        
        return JsonResponse({"valid": valid,"completed":is_completed})
    
    context  ={
        "puz_ch":puz_ch,
        
         "is_completed":puzzle.is_solved
     }
     
    print(f"compleated in model view ; {puzzle.is_solved}")
    return render(request,"sudoku.html",context=context )