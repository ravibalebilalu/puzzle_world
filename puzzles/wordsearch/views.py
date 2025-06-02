from django.shortcuts import render
from wordsearch.models import Puzzle,Word,Char

 


def home(request):
    puzzle = Puzzle.objects.get(id=190)
    words = puzzle.words.all()
    chars = puzzle.chars.all()

    if request.method == "POST":
        print(request.POST.getlist("characters"))

    context = {
        "words":words,
         "chars":chars
    }
     
 
   
    return render(request,"home.html",context)