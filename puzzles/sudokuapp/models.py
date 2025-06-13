from django.db import models
from wordsearch.models import NonUser
from django.contrib.auth import get_user_model

User = get_user_model()


class Puzzle(models.Model):
    name = models.CharField(default="sudoku", max_length=10)
    challenge = models.JSONField()
    solution = models.JSONField()
    is_solved = models.BooleanField(default=False)
    initial_time = models.DateTimeField(null=True, blank=True)
    finished_time = models.DateTimeField(null=True, blank=True)
    inProgress = models.BooleanField(default=False, blank=True, null=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="sudoku_puzzles")
    nonuser = models.ForeignKey(NonUser, on_delete=models.CASCADE, null=True, blank=True,related_name="sudoku_puzzles")

    def __str__(self):
        return self.name


 
    