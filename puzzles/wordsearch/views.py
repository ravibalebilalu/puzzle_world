from django.shortcuts import render
from wordsearch.models import Puzzle, Word, Char, NonUser
from wordsearch.utils import process_form_data, check_word, check_puzzle_copmleated, initialize_puzzle,build_puzzle
import random

def home(request):
    puzzle = None

    if request.user.is_authenticated:
        # Logged-in user
        user = request.user
        puzzle = Puzzle.objects.filter(user=user, grid_checked=False).first()

        if not puzzle:
            build_puzzle()
            puzzle = Puzzle.objects.filter(grid_checked=False, user=None, nonuser=None).first()
            if puzzle:
                puzzle.user = user
                puzzle.save()

    else:
        # Guest user → use session to track nonuser
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        nonuser, created = NonUser.objects.get_or_create(session_id=session_id)

        puzzle = Puzzle.objects.filter(nonuser=nonuser, grid_checked=False).first()

        if not puzzle:
            build_puzzle()
            puzzle = Puzzle.objects.filter(grid_checked=False, user=None, nonuser=None).first()
            if puzzle:
                puzzle.nonuser = nonuser
                puzzle.save()

    # Safety check (if no puzzle found at all)
    if not puzzle:
        return render(request, "home.html", {"message": "No puzzles available. Please try later."})

    # Words and chars
    words = puzzle.words.all()
    chars = puzzle.chars.all()

    # POST request → process puzzle actions
    if request.method == "POST":
        if not puzzle.inProgress and not puzzle.grid_checked:
            initialize_puzzle(puzzle)

        form_data = request.POST.getlist("characters")

        if request.POST.getlist("start_puzzle"):
            puzzle_start_signal = request.POST.getlist("start_puzzle")

        char_list, index_list = process_form_data(form_data)
        check_word(char_list, words, puzzle, chars)
        check_puzzle_copmleated(puzzle, words)

    # Context
    context = {
        "puzzle": puzzle,
        "words": words,
        "chars": chars,
    }
    print(puzzle)
    return render(request, "home.html", context)