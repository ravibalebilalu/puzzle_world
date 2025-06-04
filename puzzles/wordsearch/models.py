from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Puzzle(models.Model):
    row_length = models.PositiveSmallIntegerField(default=12)
    col_length = models.PositiveSmallIntegerField(default=12)
    grid_checked = models.BooleanField(default=False)
    inProgress = models.BooleanField(default=False,null=True,blank=True)
    initial_time = models.DateTimeField(null=True,blank=True)
    finished_time = models.DateTimeField(null=True,blank=True)

    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)


    def save(self, *args, **kwargs):
        if not (10 <= self.row_length <= 15):
            self.row_length = min(max(self.row_length, 10), 15)
        if not (10 <= self.col_length <= 15):
            self.col_length = min(max(self.col_length, 10), 15)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Puzzle {self.id} ({self.row_length}x{self.col_length})"


class Word(models.Model):
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name='words')
    word = models.CharField(max_length=50)
    word_checked = models.BooleanField(default=False)
    

    def __str__(self):
        return self.word


class Char(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE, related_name='chars',null=True,blank=True)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name='chars')
    character = models.CharField(max_length=1)
    index = models.PositiveSmallIntegerField()  # 0 to 143 max
    char_checked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.character} "
