from django.shortcuts import render
from sudokuapp.sudoku_creater import create_puzzle
from sudokuapp.models import Puzzle
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@csrf_exempt
def sudoku_view(request):
    puzzle = Puzzle.objects.all().first()
    puz_ch = puzzle.challenge
    if request.method == "POST":
        data = json.loads(request.body)
        row = int(data["row"])
        col = int(data["col"])
        val = int(data["val"])
        valid = True

        print(data)
        return JsonResponse({"valid": valid})

        

     


    context  ={
        "puz_ch":puz_ch
     }
     

    return render(request,"sudoku.html",context=context )