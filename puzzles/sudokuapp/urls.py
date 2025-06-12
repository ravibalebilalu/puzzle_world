from django.urls import path
from sudokuapp import views
 
urlpatterns = [
    path("",views.sudoku_view,name="sudoku"),
]
