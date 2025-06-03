from django.shortcuts import render
from wordsearch.models import Puzzle,Word,Char
from wordsearch.utils import process_form_data,check_word,check_puzzle_copmleated

 


def home(request):
    puzzle = Puzzle.objects.filter(grid_checked = False)[1]
    words = puzzle.words.all()
    chars = puzzle.chars.all()
    start_game = False
    
    if request.method == "POST":
        
         
        
        form_data = request.POST.getlist("characters")
        if request.POST.getlist("start_puzzle"):
            puzzle_start_signal = request.POST.getlist("start_puzzle")
            if puzzle_start_signal[0] == "@#$" and  start_game == False:
                start_game =   True
         
         
        char_list ,index_list =  process_form_data(form_data)
        is_word = check_word(char_list,words,puzzle,chars)
        check_puzzle_copmleated(puzzle,words)

    print(start_game)
    
    context = {
        "words":words,
         "chars":chars,
         "start_game" : start_game
         
    }
     
 
     
    return render(request,"home.html",context)