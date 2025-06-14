from django.contrib import admin
from sudokuapp.models import Puzzle,Cell

admin.site.register([Puzzle,Cell])

# Register your models here.
