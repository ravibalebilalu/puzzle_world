from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sudokuapp.sudoku_creater import create_puzzle, validate_puzzle, calculate_time
from sudokuapp.models import Puzzle
from datetime import datetime
from django.utils import timezone
import json

@csrf_exempt
def sudoku_view(request):
    user = request.user if request.user.is_authenticated else None

    if request.method == "POST":
        data = json.loads(request.body)
        row, col, val = int(data["row"]), int(data["col"]), int(data["val"])
        puzzle = Puzzle.objects.filter(user=user, inProgress=True, is_solved=False).last()

        if not puzzle:
            return JsonResponse({"error": "No active puzzle"}, status=400)

        valid, is_completed = validate_puzzle(row, col, val, puzzle)

        return JsonResponse({
            "valid": valid,
            "completed": is_completed,
            "time_taken": calculate_time(puzzle) if is_completed else None,
        })

    # If puzzle is solved or none exists, create new
    puzzle = Puzzle.objects.filter(user=user, inProgress=True, is_solved=False).last()

    if not puzzle:
        Puzzle.objects.filter(user=user, inProgress=True).update(inProgress=False)
        challenge, solution = create_puzzle()
        puzzle = Puzzle.objects.create(
            challenge=challenge,
            solution=solution,
            initial_time=datetime.now(),
            inProgress=True,
            user=user
        )

    elif puzzle.is_solved:
        puzzle.inProgress = False
        puzzle.save()
        challenge, solution = create_puzzle()
        puzzle = Puzzle.objects.create(
            challenge=challenge,
            solution=solution,
            initial_time=datetime.now(),
            inProgress=True,
            user=user
        )

    context = {
        "puz_ch": puzzle.challenge,
        "is_completed": puzzle.is_solved,
        "time_taken": calculate_time(puzzle) if puzzle.is_solved else None
    }

    return render(request, "sudoku.html", context)
