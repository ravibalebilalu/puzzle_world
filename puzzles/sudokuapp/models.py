from django.db import models


class Puzzle(models.Model):
    name = models.CharField(default="sudoku",max_length=10)
    challenge = models.JSONField()
    solution = models.JSONField()
    is_solved =  models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    