from django.shortcuts import render

def sudoku_view(request):
    return render(request,"sudoku.html")