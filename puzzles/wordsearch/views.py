from django.shortcuts import render
from wordsearch.models import Puzzle,Word,Char
from wordsearch.utils import process_form_data,check_word,check_puzzle_copmleated,initialize_puzzle
import time

 


def home(request):
    puzzle = Puzzle.objects.filter(grid_checked = False)[1]
    words = puzzle.words.all()
    chars = puzzle.chars.all()
     

    if request.method == "POST":
        #start puzzle signal
        if not puzzle.inProgress and not puzzle.grid_checked:
            initialize_puzzle(puzzle)
        #get form data and process
        form_data = request.POST.getlist("characters")
        if request.POST.getlist("start_puzzle"):
            puzzle_start_signal = request.POST.getlist("start_puzzle")
           
         
         
        char_list ,index_list =  process_form_data(form_data)
        is_word = check_word(char_list,words,puzzle,chars)
        check_puzzle_copmleated(puzzle,words)

  
    context = {
        "puzzle":puzzle,
        "words":words,
         "chars":chars,
        }
     
   
    return render(request,"home.html",context)