 

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
     
    path("wordsearch/",include("wordsearch.urls",namespace="wordsearch")),
    path("",include("users.urls")),
    path("sudoku/",include("sudokuapp.urls" )),
]
