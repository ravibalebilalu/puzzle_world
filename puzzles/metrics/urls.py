from django.urls import path
from metrics import views

urlpatterns = [
    path("",views.metrics_view,name="metrics"),
]
