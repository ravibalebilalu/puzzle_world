from django.urls import path
from wordsearch import views

urlpatterns = [
    path("",views.home,name="home"),
]
