from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from wordsearch.models import Puzzle, Word, Char, NonUser
from wordsearch.utils import process_form_data, check_word, check_puzzle_completed, initialize_puzzle, build_puzzle
import json

def home(request):
    puzzle = None

    if request.user.is_authenticated:
        user = request.user
        puzzle = Puzzle.objects.filter(user=user, grid_checked=False).first()
        if not puzzle:
            build_puzzle()
            puzzle = Puzzle.objects.filter(grid_checked=False, user=None, nonuser=None).first()
            if puzzle:
                puzzle.user = user
                puzzle.save()
    else:
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

    if not puzzle:
        return render(request, "home.html", {"message": "No puzzles available. Please try later."})

    words = puzzle.words.all()
    chars = puzzle.chars.all()

    if request.method == "POST":
        if not puzzle.inProgress and not puzzle.grid_checked:
            initialize_puzzle(puzzle)
        form_data = request.POST.getlist("characters")
        if form_data:  # Old form submission
            char_list, index_list = process_form_data(form_data)
            check_word(char_list, words, puzzle, chars)
            check_puzzle_completed(puzzle, words)

    context = {
        "puzzle": puzzle,
        "words": words,
        "chars": chars,
    }
    return render(request, "home.html", context)

@csrf_exempt
def check_word_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        word = data.get('word', '').upper()

        # Get puzzle based on user or session
        puzzle = None
        if request.user.is_authenticated:
            puzzle = Puzzle.objects.filter(user=request.user, grid_checked=False).first()
        else:
            session_id = request.session.session_key
            if session_id:
                nonuser = NonUser.objects.filter(session_id=session_id).first()
                if nonuser:
                    puzzle = Puzzle.objects.filter(nonuser=nonuser, grid_checked=False).first()

        if not puzzle:
            return JsonResponse({'error': 'No active puzzle found'}, status=400)

        words = puzzle.words.all()
        chars = puzzle.chars.all()

        # Check if word is valid
        char_list = list(word.lower())  # Convert to list for check_word
        is_correct = check_word(char_list, words, puzzle, chars)
        if is_correct:
            check_puzzle_completed(puzzle, words)

        return JsonResponse({'correct': is_correct})
    return JsonResponse({'error': 'Invalid request'}, status=400)