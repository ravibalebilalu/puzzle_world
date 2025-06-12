from django.urls import path
from sudoku import views
 
urlpatterns = [
    path("",views.sudoku_view,name="sudoku"),
]
