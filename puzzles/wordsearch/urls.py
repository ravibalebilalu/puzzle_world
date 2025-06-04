from django.urls import path
from wordsearch import views
app_name= "wordsearch"
urlpatterns = [
    path("",views.home,name="home"),
]
